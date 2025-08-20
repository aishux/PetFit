from .sub_agents.rephraser_agent.agent import rephraser_agent
from .sub_agents.recommender_agent.agent import recommender_agent
from .sub_agents.finalizer_agent.agent import finalizer_agent
from .sub_agents.summarizer_agent.agent import summarizer_agent

from google.adk.tools.agent_tool import AgentTool

from google.adk.agents import LlmAgent


symptom_remedy_agent = LlmAgent(
    name="symptom_remedy_agent",
    model="gemini-2.0-flash",
    description="Symptom Analysis Manager agent",
    instruction="""
       You are the Symptom analyser and remedy recommendation Manager agent responsible for orchestrating the following agent tools:
        - `rephraser_agent`: Rephrases the user query for better results in full text search and vector search.
        - `recommender_agent`: Provides top 3 matches as per the user query.
        - `summarizer_agent`: Summarizes the symptoms, clinical notes and prescriptions to the user.

        Sub-Agent:
        - `finalizer_agent`: A sub-agent that helps in finalizing the matches by questioning user about the top 3 possible matches of symptoms.

        ### Strictly follow the Step-by-step flow:

        1. Call the rephraser_agent passing the raw user query to get the rephrased query
        2. Call the recommender_agent to find the top matching results
        3. Go to the finalizer_agent sub-agent to finalize on the most prominient matches as it does Q&A with the user
        4. Finally call the summarizer_agent and get the summarized output. Then strictly present this output to the user as it is without any changes.
    """,
    sub_agents=[finalizer_agent],
    tools=[
        AgentTool(rephraser_agent),
        AgentTool(recommender_agent),
        AgentTool(summarizer_agent)
    ],
    output_key="symptom_remedies"
)
