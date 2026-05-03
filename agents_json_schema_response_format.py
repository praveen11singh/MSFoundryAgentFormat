import os
import json
from typing import Dict, Any
from azure.identity import DefaultAzureCredential
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import (
    ListSortOrder,
    MessageRole,
    ResponseFormatJsonSchema,
    ResponseFormatJsonSchemaType,
    RunStatus,
)

from dotenv import load_dotenv

load_dotenv()

json_schema: Dict[str, Any] = {
    "$defs": {
        "PlanetName": {
            "type": "string",
            "description": "The name of the planet",
            "enum": ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"],
        }
    },
    "type": "object",
    "description": "Information about the planets in the Solar System",
    "properties": {
        "planets": {
            "type": "array",
            "items": {
                "type": "object",
                "description": "Information about a planet in the Solar System",
                "properties": {
                    "name": {"$ref": "#/$defs/PlanetName"},
                    "mass": {
                        "type": "number",
                        "description": "Mass of the planet in kilograms",
                    },
                    "relative_mass": {
                        "type": "number",
                        "description": "Relative mass of the planet compared to Earth",
                    },
                },
                "required": ["name", "mass"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["planets"],
    "additionalProperties": False,
}

# Use AgentsClient directly — NOT AIProjectClient
agents_client = AgentsClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)

with agents_client:

    agent = agents_client.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        name="my-agent",
        instructions="You are helpful agent. Your response is JSON formatted.",
        response_format=ResponseFormatJsonSchemaType(
            json_schema=ResponseFormatJsonSchema(
                name="planet_mass",
                description="Masses of Solar System planets",
                schema=json_schema,
            )
        ),
    )
    print(f"Created agent, agent ID: {agent.id}")

    thread = agents_client.threads.create()
    print(f"Created thread, thread ID: {thread.id}")

    message = agents_client.messages.create(
        thread_id=thread.id,
        role="user",
        content="Hello, give me a list of planets in our solar system, and their mass in kilograms.",
    )
    print(f"Created message, message ID: {message.id}")

    run = agents_client.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)

    if run.status != RunStatus.COMPLETED:
        print(f"The run did not succeed: {run.status=}.")

    agents_client.delete_agent(agent.id)
    print("Deleted agent")

    messages = agents_client.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
    for msg in messages:
        if msg.text_messages:
            last_text = msg.text_messages[-1]
            print(f"{msg.role}: {last_text.text.value}")
            if msg.role == MessageRole.AGENT:
                response_dict = json.loads(last_text.text.value)
                for planet in response_dict["planets"]:
                    print(f"The mass of {planet['name']} is {planet['mass']} kg.")