from google.adk.agents import LlmAgent
from .tools import identify_sound_meaning, get_info_dog_behaviour


audio_detection_agent = LlmAgent(
    name="audio_detection_agent",
    model="gemini-2.0-flash",
    description="Audio Detection Agent",
    instruction="""
       You are an agent that detects the meaning of the audio input for the user's pet.
       To detect what the provided sound means use the tool identify_sound_meaning.
       Once you get the identification about what the sound means, summarize it in 2 lines to the user.

       When user asks more information on the identification identified use the tool get_info_dog_behaviour to fetch informative bits, use the information which you feel is relevant then frame the response summary and explain to the user in detail.
    """,
    tools=[identify_sound_meaning, get_info_dog_behaviour],
    output_key="summary_sound_identification",
)