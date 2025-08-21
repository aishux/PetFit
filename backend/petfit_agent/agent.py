from google.adk.agents import Agent
from .agents.symptom_remedy_agent.agent import symptom_remedy_agent
from .agents.audio_detection_agent.agent import audio_detection_agent
from .agents.pet_vitals_info_agent.agent import pet_vitals_info_agent

root_agent = Agent(
    name="petfit_agent",
    model="gemini-2.0-flash",
    description="PetFit Manager agent",
    instruction="""
       You are the PetFit Manager agent responsible for orchestrating the following agents:
        - `audio_detection_agent`: Takes the audio sound file of users pet and detects what the sound means
        - `pet_vitals_info_agent`: Helps user with the information about pet's tracked vital health related queries. Use this agent when queries are related to heart, sleep, calories or miles travelled.
        - `symptom_remedy_agent`: Provides detailed analysis on the symptoms and its remedies. Use this agent when the queries are more related to symptoms which are not matching for pet_vitals_info_agent.

        When a pet id is provided in the query strictly use the pet_vitals_info_agent.

    """,
    sub_agents=[
        symptom_remedy_agent,
        audio_detection_agent,
        pet_vitals_info_agent
    ]
)