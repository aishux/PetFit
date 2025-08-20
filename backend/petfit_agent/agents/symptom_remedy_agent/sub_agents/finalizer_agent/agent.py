from google.adk.agents import LlmAgent

# Define the ADK agent
finalizer_agent = LlmAgent(
    name="finalizer_agent",
    model="gemini-2.0-flash",
    description="Questions user about the top 3 possible matches of symptoms and drills down to the final matches",
    instruction="""
    You are responsible for framing the questions for user and asking the questions to user to arrive at the decision for finalzing the possible matching symptoms for the matches found as below.

    Matches found:
    {top_matches}

    You must:
    1. Understand the top matches found and frame few questions for the users
    2. Analyse the users answers and finalize what are final matches, it could be 1 or 2 if you are not very confident about just 1 match.
    3. Formulate the data finalized in such a format that other agent can get more information on the symptoms and remediations to summarize the details.

    Important rules:
    - Make sure to think carefully about the user's answers and drill down on to the final matches
    - The questions should be framed as per the top 3 matches received
    - Strictly Do not use the keywords like (match 1) in the question, just ask questions as required without giving for which match you are asking the question.
    - All the columns should be included in the output
    - DO NOT HALLUCINATE

    IMPORTANT:
    ONCE THE MATCHES ARE FINALIZED TRANSFER THE CONTROL TO THE PARENT AGENT.

    """,
    output_key="finalized_matches"
)

