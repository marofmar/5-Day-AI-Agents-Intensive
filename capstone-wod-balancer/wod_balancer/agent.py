import os
from dotenv import load_dotenv
from google.adk.agents import Agent, SequentialAgent
from google.adk.tools import google_search

load_dotenv()
# Ensure Vertex AI is disabled if using API key
if "GOOGLE_API_KEY" in os.environ:
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"

# customer_facing_agent
get_wod_agent = Agent(
    name="GetWodAgent",
    model="gemini-2.5-flash-lite",
    instruction="""
        To customer user, politely inquire which date the user has attended crossfit WOD out of the prior 7 days. 
        Based on the response of the user, retrieve daily wod content only from official crossfit website, https://www.crossfit.com/ 
        The url is very straight-forward for each date.
        For example, if user attended wod on 2025 Nov 24, you should look up "crossift.com/251124
        Unless specified, the default year is this year.
        """,
    tools=[google_search],
    output_key="get_wod_agent_output",
)

# per_wod_analysis_agent
analyze_wod_agent = Agent(
    name="AnalyzeWodAgent",
    model="gemini-2.5-flash-lite",
    instruction="""
        You are an experienced researcher in functional anatomy, and exercise physiology specialized in CrossFit movements.
        Based on {get_wod_agent_output}, analyze the cumulative physiological adaptations 
        assuming these WODs were performed sequentially in different days. 
        Break down each wod's effect by MGW modalities and specify the targeted muscle groups.
        Present the summary as a bulleted list with 3-5 key pointsn for each different wod.
    """,
    output_key="analyze_wod_output"
)

recommend_agent = Agent(
    name="RecommendAgent",
    model="gemini-2.5-flash-lite",
    instruction="""Review {analyze_wod_output}, and suggest 3-5 supplementary exercises or stretches 
    to help the member maintain a balanced physique and recover overused muscle areas. 
    Present the result in 3 to 5 bullet points.
    """,
    tools=[google_search],
    output_key="recommend_output"
)

root_agent = SequentialAgent(
    name="ResearchSystem",
    sub_agents=[get_wod_agent, analyze_wod_agent, recommend_agent],
)
