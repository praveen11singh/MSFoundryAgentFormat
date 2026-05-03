import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import (
    AgentsResponseFormat,
    ListSortOrder,
    RunStatus,
)

load_dotenv()

# Use AgentsClient directly — NOT project_client.agents
agents_client = AgentsClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

with agents_client:

    #
    # 1. Create Agent
    #
    agent = agents_client.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        name="my-agent",
        instructions="You are a helpful agent. You will respond with a JSON object.",
        response_format=AgentsResponseFormat(type="json_object"),
    )
    print(f"Created agent, agent ID: {agent.id}")

    #
    # 2. Create Thread
    #
    thread = agents_client.threads.create()
    print(f"Created thread, thread ID: {thread.id}")

    #
    # 3. Add User Message
    #
    message = agents_client.messages.create(
        thread_id=thread.id,
        role="user",
        content="Hello, give me a list of planets in our solar system, and their mass in kilograms.",
    )
    print(f"Created message, message ID: {message.id}")

    #
    # 4. Run the Agent
    #
    run = agents_client.runs.create_and_process(
        thread_id=thread.id,
        agent_id=agent.id,
    )

    if run.status != RunStatus.COMPLETED:
        print(f"The run did not succeed: {run.status}")
    else:
        print("Run completed successfully.")

    #
    # 5. Read Messages
    #
    messages = agents_client.messages.list(
        thread_id=thread.id,
        order=ListSortOrder.ASCENDING,
    )

    for msg in messages:
        if msg.text_messages:
            last_text = msg.text_messages[-1]
            print(f"{msg.role}: {last_text.text.value}")

    #
    # 6. Delete Agent
    #
    agents_client.delete_agent(agent.id)
    print("Deleted agent")