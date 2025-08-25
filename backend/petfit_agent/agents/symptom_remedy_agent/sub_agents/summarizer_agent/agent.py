from google.adk.agents import LlmAgent
from petfit_agent.setup import save_pet_weekly_history_cache

from google.adk.agents.callback_context import CallbackContext

def after_agent_callback_method(callback_context: CallbackContext):
    save_pet_weekly_history_cache(callback_context, callback_context.state["summarized_output"])
    return None

# Define the ADK agent
summarizer_agent = LlmAgent(
    name="summarizer_agent",
    model="gemini-2.0-flash",
    description="Summarizes the symptoms, clinical notes and prescriptions to the user",
    instruction="""
    You are responsible for generating a informative and educative summary for the finalized matches as below for the user.

    Finalized Matches:
    {finalized_matches}

    You must:
    1. Format the data in a detailed informative way with proper headings. Also make sure to include the prescriptions for each of the identified issue.
    2. The information should be educative and not argumentative
    3. Do not mention the keywords like according to match 1, user should be provided the response as an end user not like someone who is internal.
    4. Do not ask for any more information or any questions, just provide the summary as expected.
    5. At the end mention that you are not a veterinarian and take this advice for information purpose only.

    For making the response more customized use the below pet's information:
    {pet_information}

    DO NOT HALLUCINATE.
    """,
    output_key="summarized_output",
    after_agent_callback=after_agent_callback_method
)

