import os
from enum import Enum
from pydantic import BaseModel, TypeAdapter
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


# Create the pydantic model to represent the planet names and their masses.
class PlanetName(str, Enum):
    Mercury = "Mercury"
    Venus = "Venus"
    Earth = "Earth"
    Mars = "Mars"
    Jupiter = "Jupiter"
    Saturn = "Saturn"
    Uranus = "Uranus"
    Neptune = "Neptune"


class Planet(BaseModel):
    name: PlanetName
    mass: float


class Planets(BaseModel):
    planets: list[Planet]


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
                description="Masses of Solar System planets.",
                schema=Planets.model_json_schema(),
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