from dotenv import load_dotenv
import os
from pathlib import Path
import asyncio

def setup_gemini_api_key():
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)

    # reference: https://stackoverflow.com/questions/16924471/difference-between-os-getenv-and-os-environ-get
    try:
        api_key = os.environ["GOOGLE_API_KEY"]
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"
        print("✅ Gemini API key setup complete.")
    except Exception as e:
        print(f"🔑 Authentication Error: Please make sure you have added 'GOOGLE_API_KEY' in .env file. Details: {e}")
    return api_key

def setup_adk():
    from google.adk.agents import Agent, SequentialAgent, ParallelAgent, LoopAgent
    from google.adk.runners import InMemoryRunner
    from google.adk.tools import AgentTool, FunctionTool, google_search
    from google.genai import types
    print("✅ ADK components imported successfully.")

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
        3. Finally, present the final summary claerly to the user as your response in Korean with proper citations.""",
        tools=[
            AgentTool(research_agent),
            AgentTool(summarizer_agent)
        ],
    )
    print("✅ root_agent created.")
    return root_agent


if __name__ == "__main__":
    setup_gemini_api_key()
    setup_adk()

    research_agent = create_research_agent()
    summarizer_agent = create_summarizer_agent()
    root_agent = create_root_agent(research_agent, summarizer_agent)

    runner = InMemoryRunner(agent=root_agent)
    async def main():
        response = await runner.run_debug("What are the latest advancements in sns user tracking technologies?")
        print("\n📝 Final Response:\n", response)

    asyncio.run(main())
    print("\n📝 Final Response:\n", response)