from petfit_agent.setup import query_db, get_table
from google.adk.agents.callback_context import CallbackContext
import matplotlib.pyplot as plt
import os
import glob
import smtplib, ssl, certifi
import ssl
from email.message import EmailMessage
import reportlab
from google.adk.tools import ToolContext
from email.utils import formataddr

GAPP_PASS = os.getenv("GAPP_PASS")

def create_and_save_graph(x, y, graph_title, file_name, graph_type="line"):
    """
    Create and save a graph as PNG.
    Args:
        x (list/Series): x-axis values
        y (list/Series): y-axis values
        graph_title (str): Title of the graph
        file_name (str): Name of the file (saved as .png)
        graph_type (str): "line" or "bar"
    """
    plt.figure(figsize=(8, 5))

    if graph_type == "line":
        plt.plot(x, y, marker="o", linestyle="-")
    elif graph_type == "bar":
        plt.bar(x, y)
    else:
        raise ValueError("graph_type must be 'line' or 'bar'")

    plt.title(graph_title)
    plt.xlabel("Day")
    plt.ylabel(graph_title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{file_name}.png")
    plt.close()


def before_agent_callback_method(callback_context: CallbackContext):
    pet_id = callback_context.state["pet_information"]["pet_id"]

    data_collection = query_db(f"""
    SELECT
        DATE(`created_at`) AS `day`,
        ROUND(AVG(`heart_rate`),2) AS `avg_heart_rate`,
        ROUND(AVG(`miles_travelled`),2) AS `avg_miles_travelled`,
        ROUND(AVG(`calories_burned`),2) AS `avg_calories_burned`,
        ROUND(SUM(`sleep_hours`),2) AS `total_sleep_hours`
    FROM
        `pet_data`
    WHERE
        `pet_id` = '{pet_id}'
        AND `created_at` >= DATE_SUB(CURDATE(), INTERVAL 15 DAY)
    GROUP BY
        `day`;
    """)

    data_collection = data_collection.to_pandas()

    print(data_collection)

    callback_context.state["pet_weekly_vitals_data"] = data_collection.to_dict()

    # Ensure day is sorted
    data_collection = data_collection.sort_values("day")

    # Generate graphs
    create_and_save_graph(
        data_collection["day"], data_collection["avg_heart_rate"],
        "Average Heart Rate", "avg_heart_rate", "line"
    )

    create_and_save_graph(
        data_collection["day"], data_collection["total_sleep_hours"],
        "Total Sleep Hours", "total_sleep_hours", "line"
    )

    create_and_save_graph(
        data_collection["day"], data_collection["avg_miles_travelled"],
        "Average Miles Travelled", "avg_miles_travelled", "bar"
    )

    create_and_save_graph(
        data_collection["day"], data_collection["avg_calories_burned"],
        "Average Calories Burned", "avg_calories_burned", "bar"
    )

    table = get_table("pet_weekly_history_cache")
    history_data = table.get(pet_id).information

    callback_context.state["pet_conversation_history_cache"] = history_data

    return None


def after_agent_callback_method(callback_context: CallbackContext):
    for f in ["avg_miles_travelled.png", "avg_calories_burned.png", "total_sleep_hours.png", "avg_heart_rate.png"]:
        if os.path.exists(f):
            os.remove(f)
    # pet_id = callback_context.state["pet_information"]["pet_id"]
    # query_db(f"UPDATE `pet_weekly_history_cache` SET `information` = '' WHERE `pet_id` = '{pet_id}'; ")

    return None

def send_report_mail(tool_context, pdf_file_name, pet_info):
    pet_name = pet_info["name"]
    pet_owner_id = pet_info["owner_id"]
    table = get_table("auth_user")
    owner_data = table.get(pet_owner_id)
    owner_email = owner_data.email

    matches = glob.glob(pdf_file_name)
    if matches:
        print("Match Found")
        report_file_name = matches[0]
        weekly_date = "-".join(report_file_name.split(".")[0].split("-")[1:])
        subject = f"{pet_name} Weekly Report for {weekly_date}"
        body = f"""
Dear {pet_name}'s Owner,

Please find attached the weekly report for your loving pet {pet_name}.

Please reach out to us if you need any further help.

With ❤️ from PetFit Team
        """

        # Sender details
        sender_email = "nikhilsmankani@gmail.com"
        app_password = GAPP_PASS

        # Create email
        msg = EmailMessage()
        msg["From"] = formataddr(("PetFit Team", sender_email))
        msg["To"] = owner_email
        msg["Subject"] = subject
        msg.set_content(body)

        # Attach PDF
        with open(report_file_name, "rb") as f:
            file_data = f.read()
            msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=report_file_name)

        # Send email
        context = ssl.create_default_context(cafile=certifi.where())
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)

        print(f"✅ Email sent to {owner_email} with report {report_file_name}")
        os.remove(report_file_name)
    else:
        print("No match found")

def pet_python_code_execution(tool_context: ToolContext, content: dict):
    python_code = content["python_code"]
    print("Python Code: ", python_code)
    exec(python_code, {"reportlab":reportlab})
    pet_info = tool_context.state["pet_information"]
    pdf_path = f"{pet_info['pet_id']}_weekly_petfit_report-*.pdf"
    send_report_mail(tool_context, pdf_path, pet_info)
    return True