import os
import sys
import io
import asyncio
from pathlib import Path
from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner
from wod_balancer.agent import root_agent
from wod_balancer.utils import save_markdown_to_pdf

async def main():
    # Load env
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)
    
    try:
        if "GOOGLE_API_KEY" not in os.environ:
             raise Exception("GOOGLE_API_KEY not found in environment variables")
        
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"
        print("✅ Gemini API key setup complete.")
    except Exception as e:
        print(f"🔑 Authentication Error: Please make sure you have added 'GOOGLE_API_KEY' in .env file. Details: {e}")
        return

    print(">> Agents loaded. Running analysis...")

    # Get user input
    print("For the last 7 days, please tell me which date you have participated in WOD. I will analyze the effect on your body and recoomend accessary workouts for your balanced physique.")
    user_input = input("Your response: ")

    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = mystdout = io.StringIO()

    try:
        runner = InMemoryRunner(agent=root_agent)
        await runner.run_debug(user_input)
    finally:
        sys.stdout = old_stdout

    # Get the captured text
    captured_output = mystdout.getvalue()

    # Print it back to console
    print(captured_output)

    # Save to PDF
    save_markdown_to_pdf(captured_output, "crossfit_report.pdf")

if __name__ == "__main__":
    asyncio.run(main())
