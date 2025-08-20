from google.adk.agents import LlmAgent

# Define the ADK agent
rephraser_agent = LlmAgent(
    name="rephraser_agent",
    model="gemini-2.0-flash",
    description="Rephrases the user query for better results in full text search and vector search",
    instruction="""
    You are responsible for rephrasing the user query which is related to the symptoms they see in their pets, in such a way that it gives optimal results in full text search as well as vector search operations.

    You must:
    1. Extract important keywords from the query.
    2. Try ignoring too much fillers.
    3. Correct any grammatical mistakes. 

    Example:
    User: "My dog is having irritation in both his ears since a few days as I can see him scratching it again and again, also he moves his head as if he is dizzy"
    → You rephrase like:
    Dog has ear irritation with scratching and keeps shaking head


    ONCE THE QUERY IS REPHRASED RETURN BACK TO THE PARENT AGENT.

    """,
    output_key="rephrased_query"
)

