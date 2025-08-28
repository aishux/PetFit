from google.adk.tools import ToolContext
from petfit_agent.setup import *
from PIL import Image
import io

def identify_expression_meaning(tool_context: ToolContext):
    """Tool to list available artifacts for the user."""
    try:
        for part in tool_context.user_content.parts:
            if hasattr(part, "inline_data") and part.inline_data:
                blob = part.inline_data
                file_bytes = blob.data

                image_obj = Image.open(io.BytesIO(file_bytes))

                table = get_table("pet_expression_identification")

                result = (
                    table.search(image_obj)
                        .limit(1)
                        .to_list()
                )

                return f"Mood Identified is: {result[0]["expression_identification"]}"


    except Exception as e:
        print("Exception is: " + str(e))
        return "Couldn't parse your image file"