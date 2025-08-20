from google.adk.agents import Agent
from .agents.symptom_remedy_agent.agent import symptom_remedy_agent
from .agents.audio_detection_agent.agent import audio_detection_agent

root_agent = Agent(
    name="petfit_agent",
    model="gemini-2.0-flash",
    description="PetFit Manager agent",
    instruction="""
       You are the PetFit Manager agent responsible for orchestrating the following agents:
        - `symptom_remedy_agent`: Provides detailed analysis on the symptoms and its remedies.
        - `audio_detection_agent`: Takes the audio sound file of users pet and detects what the sound means

    """,
    sub_agents=[
        symptom_remedy_agent,
        audio_detection_agent
    ]
)