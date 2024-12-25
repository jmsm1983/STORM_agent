import asyncio
from dotenv import load_dotenv
from graph.state import ResearchState
from graph.consts import INIT_RESEARCH
from graph.graph import app  # Import the compiled app from your workflow file

# Load environment variables
load_dotenv(override=True)  # <-- Forces .env to override system variables


import os
api_key = os.getenv("OPENAI_API_KEY")

# Async function to run the workflow
async def run_workflow():
    # Configuration (optional but useful for multi-threading)
    config = {
        "configurable": {
            "thread_id": "my-thread"
        }
    }

    # Define the input state (e.g., topic for research)
    initial_state = {
        "topic": "The Evolution of Olympic Broadcasting: How OBS is Revolutionizing Global Sports Coverage"
    }

    # Stream the workflow steps and handle output
    async for step in app.astream(initial_state, config):
        step_name = next(iter(step))  # Get the step name
        print(step_name)  # Print the node name
        print("-- ", str(step[step_name])[:300])  # Print the first 300 chars of the output

# Entry point for async execution
if __name__ == "__main__":
    asyncio.run(run_workflow())
