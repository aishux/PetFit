from google.adk.tools import ToolContext
from petfit_agent.setup import *
from PIL import Image
import io

def identify_skin_disease(tool_context: ToolContext):
    """To identify the skin disease of the pet"""
    try:
        for part in tool_context.user_content.parts:
            if hasattr(part, "inline_data") and part.inline_data:
                blob = part.inline_data
                file_bytes = blob.data

                image_obj = Image.open(io.BytesIO(file_bytes))

                if tool_context.state["pet_information"]["pet_type"].lower() == "dog":
                    table = get_table("dog_skin_disease_detection")
                else:
                    table = get_table("cat_skin_disease_detection")

                result = (
                    table.search(image_obj)
                        .limit(1)
                        .to_list()
                )

                return f"Skin Disease Identified is: {result[0]["skin_disease"]}"


    except Exception as e:
        print("Exception is: " + str(e))
        return "Couldn't parse your image file"