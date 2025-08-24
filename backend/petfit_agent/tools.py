from .setup import *
from google.adk.tools import ToolContext

def set_pet_information(tool_context: ToolContext, pet_id: str):

    table = get_table("Pets")
    pet_info = table.get(pet_id).__dict__
    del pet_info["_sa_instance_state"]

    tool_context.state["pet_information"] = pet_info

    return True