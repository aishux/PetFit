from google.adk.agents import Agent
from .tools import identify_skin_disease
from google.adk.tools.agent_tool import AgentTool
from petfit_agent.setup import search_agent

pet_skin_disease_detection_agent = Agent(
    name="pet_skin_disease_detection_agent",
    model="gemini-2.0-flash",
    description="Pet Skin Disease Identification Agent",
    instruction="""
       You are an agent that identifies the skin disease of the pet when provided with the pet's image.
       To identify what the skin disease of pet is in the provided image use the tool identify_skin_disease.
       Once you get the identification about what the skin disease of the pet is, summarize it in short to the user by fetching more information about the identified skin disease using the search_agent tool.

       When user asks more information try to interact and answer as many questions as possible using the search_agent tool. 

       For making the response more customized use the below pet's information:
       {pet_information}
    """,
    tools=[identify_skin_disease, AgentTool(search_agent)],
    output_key="summary_skin_disease_identification",
)