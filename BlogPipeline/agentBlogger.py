from dotenv import load_dotenv
import os
import asyncio
from pathlib import Path
from google.adk.agents import Agent, SequentialAgent, ParallelAgent, LoopAgent
from google.adk.runners import InMemoryRunner
from google.adk.tools import AgentTool, FunctionTool, google_search
from google.genai import types

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# reference: https://stackoverflow.com/questions/16924471/difference-between-os-getenv-and-os-environ-get
try:
    api_key = os.environ["GOOGLE_API_KEY"]
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"
    print("✅ Gemini API key setup complete.")
except Exception as e:
    print(f"🔑 Authentication Error: Please make sure you have added 'GOOGLE_API_KEY' in .env file. Details: {e}")



def create_research_agent():
    research_agent = Agent(
        name="ResearchAgent",
        model="gemini-2.5-flash-lite",
        instruction="""
        You are a specialized research agent. Your one and only job is to use the google_search tool 
        to find 2-3 pieces of relevant information on the given topic and present the findings 
        with proper citations.""",
        tools=[google_search],
        output_key="research_findings",
    )

    print("✅ research_agent created.")
    return research_agent

def create_summarizer_agent():
    summarizer_agent = Agent(
        name="SummarizerAgent",
        model="gemini-2.5-flash-lite",
        instruction="""
    Read the provided research findings: {research_findings} 
    Create a concise summary as a bulleted list with 3-5 key points with proper citations in parentheses.""",
    output_key="final_summary",
    )

    print("✅ summarizer_agent created.")
    return summarizer_agent

def create_root_agent(research_agent, summarizer_agent):
    root_agent = Agent(
        name="ResearchCoordinator",
        model="gemini-2.5-flash-lite",
        # This instruction tells the root agent HOW to use its tools
        instruction="""You are a research coordinator. Your goal is to answer the user's query by orchestrating a workflow.
        1. First, you MUST call the `ResearchAgent` tool to find relevant information on the topic provided by the user.
        2. Next, after receiving the reserach findings, you MUST call the `SummarizerAgent` tool to create a concise summary.
        3. Finally, present the final summary claerly to the user as your response in Korean.""",
        tools=[
            AgentTool(research_agent),
            AgentTool(summarizer_agent)
        ],
    )
    print("✅ root_agent created.")
    return root_agent


async def main(user_query):
    research_agent = create_research_agent()
    summarizer_agent = create_summarizer_agent()
    root_agent = create_root_agent(research_agent, summarizer_agent)

    runner = InMemoryRunner(agent=root_agent)

    print(f"🤖 Running the agent for the query...")
    response = await runner.run_debug(user_query)

    print("\n📝 Final Response:\n")
    #print(response)
    return response


if __name__ == "__main__":


    
    user_query = input("Enter your research topic: ")

    asyncio.run(main(user_query))