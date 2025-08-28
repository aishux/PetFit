from google.adk.agents import Agent
from .agents.symptom_remedy_agent.agent import symptom_remedy_agent
from .agents.audio_detection_agent.agent import audio_detection_agent
from .agents.pet_vitals_info_agent.agent import pet_vitals_info_agent
from .agents.pet_mood_identification_agent.agent import pet_mood_identification_agent
from .tools import *

root_agent = Agent(
    name="petfit_agent",
    model="gemini-2.0-flash",
    description="PetFit Manager agent",
    instruction="""
       You are an orchestrator agent. Your job is to analyze the users query about their pet and decide which specialized agent should handle it. 

        1. `audio_detection_agent`: Takes the audio sound file of users pet and detects what the sound means
       
        2. `symptom_remedy_agent`:
        - Use this when the user describes visible symptoms, behaviors, or health issues they observed directly (e.g., itching, ear irritation, vomiting, limping, rash, dizziness).  
        - These are descriptive issues, not numerical health stats.

        3. `pet_vitals_info_agent`:
        - Use this when the user explicitly or implicitly asks about their pet health condition based on tracked data (e.g., heart rate, sleep, calories, miles traveled, breathing rate).  
        - Even if they describe a symptom (like breathing heavily), if it can be correlated to **measured vitals** from the collar/tracker, then this agent is the right choice.

        4. `pet_mood_identification_agent`
        - Use this when the user provides an image of their pet and have the intention to identify the mood of their pet.

        Instructions:
        - First, detect whether the query is about observed symptoms (visible signs) or about monitored vitals (data-driven health stats).  
        - If the query matches both (symptom + vitals), prefer `pet_vitals_info_agent` since vitals provide measurable evidence.

        Before calling any agent you should first set the pet information by passing the pet_id to the tool set_pet_information and once done you can proceed with your agent orchestration.

    """,
    sub_agents=[
        symptom_remedy_agent,
        audio_detection_agent,
        pet_vitals_info_agent,
        pet_mood_identification_agent
    ],

    tools=[
        set_pet_information
    ]
)