from google.adk.agents import LlmAgent
from petfit_agent.setup import *

def get_top_matches(query: str):
    """Returns the Matches by performing Hybrid Search and Reranks the matches"""
    table = get_table("symptom_remediation")
    df = (
      table.search(query, search_type="hybrid")
        .rerank(reranker_model, "owner_observation_notes")
        .limit(3)
        .text_column("owner_observation_notes")
        .to_list()
    )

    # Remove 'owner_observation_notes_vec' from each result
    for item in df:
        item.pop('owner_observation_notes_vec', None)

    return df


recommender_agent = LlmAgent(
    name="recommender_agent",
    model="gemini-2.0-flash",
    description="Provides top 3 matches as per the user query",
    instruction="""
    Your main goal is delivering Top 3 possible symptoms and remedies based on the rephrased query: 
    
    Query:
    {rephrased_query}
    
    You must:
    1. Call the `get_top_matches` tool with the rephrased query.
    2. Format the results in a non table format and make to include all the columns.
    3. Add notes section to each match containing doubts about the match as per user query. These doubts will be used to ask user questions and finalize the remediation.

    Important rules:
    - Pass the rephrased query as it is to the tool
    - Format the output with additional details as mentioned

    ONCE THE MATCHES ARE FOUND ASSIGN THE RESULTS AND RETURN BACK TO THE PARENT AGENT.

    """,
    tools=[get_top_matches],
    output_key="top_matches"
)