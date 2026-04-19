# MSFoundryAgentFormat

> **Microsoft Foundry — Agent Response Format Patterns**
> Four production-ready patterns for controlling agent output format in Azure AI Foundry — from free-form text to strict JSON schemas and Pydantic-validated structured responses.

---

## Overview

`MSFoundryAgentFormat` demonstrates how to enforce **structured, predictable output** from Azure AI Foundry agents using response format controls. When agents are integrated into pipelines, downstream systems need outputs in a guaranteed shape — not free-form prose.

Each script is a self-contained, runnable reference showing a distinct formatting approach, from the simplest text mode through to fully schema-validated JSON with Pydantic models.

---

## Format Patterns Covered

| Script | Pattern | What it demonstrates |
|---|---|---|
| `agents_text_response_format.py` | **Text** | Default free-form text output — no format constraints |
| `agents_json_object_response_format.py` | **JSON object mode** | Instructs the agent to return valid JSON without a fixed schema |
| `agents_json_schema_response_format.py` | **JSON schema** | Enforces a strict JSON schema — agent output is validated against a defined structure |
| `agents_json_schema_response_format_using_pydantic.py` | **Pydantic schema** | Derives the JSON schema automatically from a Pydantic model — type-safe, IDE-friendly |

---

## Architecture

```
Azure AI Foundry Agent
        │
        ▼
  response_format parameter
        │
        ├── "text"              ← free-form prose (default)
        ├── {"type": "json_object"}    ← valid JSON, no schema
        ├── {"type": "json_schema",    ← strict schema enforcement
        │    "json_schema": {...}}
        └── Pydantic model      ← schema auto-derived, type-safe
                │
                ▼
        Parsed, validated output
        ready for downstream use
```

---

## Prerequisites

- Python 3.10+
- Azure subscription with **Azure AI Foundry** access
- An AI Foundry project with an agent deployment
- `pip install -r requirements.txt`

---

## Quickstart

### 1. Clone the repo

```bash
git clone https://github.com/praveen11singh/MSFoundryAgentFormat.git
cd MSFoundryAgentFormat
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
```

```env
# .env
PROJECT_CONNECTION_STRING=<your-foundry-project-connection-string>
MODEL_DEPLOYMENT_NAME=<your-model-deployment-name>
```

> **Note:** Uses `DefaultAzureCredential` — no hardcoded keys. Run `az login` locally or assign a managed identity in production.

### 4. Run any pattern

```bash
# Free-form text
python agents_text_response_format.py

# JSON object mode
python agents_json_object_response_format.py

# Strict JSON schema
python agents_json_schema_response_format.py

# Pydantic-derived schema
python agents_json_schema_response_format_using_pydantic.py
```

---

## Pattern Deep-Dives

### 1. Text Format — `agents_text_response_format.py`

The default mode. No format constraints — the agent responds in natural language prose. Use this for conversational agents where output will be displayed directly to a user.

```python
agent = agents_client.create_agent(
    model=MODEL_DEPLOYMENT_NAME,
    instructions="You are a helpful assistant.",
    response_format="text",
)
```

---

### 2. JSON Object Mode — `agents_json_object_response_format.py`

Instructs the agent to always return valid, parseable JSON — but without enforcing a specific shape. Useful when you need machine-readable output but the structure is flexible or varies by prompt.

```python
agent = agents_client.create_agent(
    model=MODEL_DEPLOYMENT_NAME,
    response_format={"type": "json_object"},
)

# Response is guaranteed valid JSON
data = json.loads(response_message.content)
```

---

### 3. JSON Schema Format — `agents_json_schema_response_format.py`

Enforces a **strict, predefined JSON schema**. The agent will only return output that conforms to the schema — ideal for pipeline integrations where downstream consumers expect a guaranteed field structure.

```python
schema = {
    "type": "object",
    "properties": {
        "name":       {"type": "string"},
        "role":       {"type": "string"},
        "company":    {"type": "string"},
        "confidence": {"type": "number"},
    },
    "required": ["name", "role", "company"],
}

agent = agents_client.create_agent(
    model=MODEL_DEPLOYMENT_NAME,
    response_format={
        "type": "json_schema",
        "json_schema": {"name": "entity_extraction", "schema": schema, "strict": True},
    },
)
```

---

### 4. Pydantic Schema Format — `agents_json_schema_response_format_using_pydantic.py`

The most production-friendly approach. Define your output structure as a **Pydantic model** — the JSON schema is derived automatically. You get IDE autocompletion, type checking, and validation out of the box.

```python
from pydantic import BaseModel

class EntityExtraction(BaseModel):
    name: str
    role: str
    company: str
    confidence: float

agent = agents_client.create_agent(
    model=MODEL_DEPLOYMENT_NAME,
    response_format=EntityExtraction,  # schema auto-derived
)

# Deserialise directly into the model
result = EntityExtraction.model_validate_json(response_message.content)
print(result.name, result.role)
```

---

## Choosing the Right Format

| Use case | Recommended pattern |
|---|---|
| Conversational / display output | Text |
| Flexible machine-readable output | JSON object |
| Fixed pipeline integration (ETL, APIs) | JSON schema |
| Type-safe Python integration with validation | Pydantic schema |
| Microservice output contract enforcement | JSON schema or Pydantic |
| Data extraction from unstructured text | JSON schema or Pydantic |

---

## Project Structure

```
MSFoundryAgentFormat/
├── agents_text_response_format.py                       # Pattern 1 — text
├── agents_json_object_response_format.py                # Pattern 2 — JSON object
├── agents_json_schema_response_format.py                # Pattern 3 — JSON schema
├── agents_json_schema_response_format_using_pydantic.py # Pattern 4 — Pydantic
├── utils/                                               # Shared helpers
├── assets/                                              # Sample input files
├── .env.example                                         # Environment variable template
├── requirements.txt
└── README.md
```

---

## Part of the Microsoft Foundry Open-Source Series

| Repo | Focus |
|---|---|
| [MSFoundryAgentMemory](https://github.com/praveen11singh/MSFoundryAgentMemory) | Ephemeral, contextual & persistent memory patterns |
| [MSFoundryFunctionCall](https://github.com/praveen11singh/MSFoundryFunctionCall) | Auto & explicit function calling |
| [MSFoundryAgentStreamEvent](https://github.com/praveen11singh/MSFoundryAgentStreamEvent) | Agent streaming & event handling |
| [MSFoundryEvaluation](https://github.com/praveen11singh/MSFoundryEvaluation) | Agent evaluation with azure-ai-evaluation |
| [MSFoundryRedTeam](https://github.com/praveen11singh/MSFoundryRedTeam) | Red team jailbreak probing & RAI evaluators |
| [MSFoundryModelRouter](https://github.com/praveen11singh/MSFoundryModelRouter) | Dynamic multi-model routing |
| **MSFoundryAgentFormat** | Agent response format patterns ← you are here |

---

## Author

**Praveen Kumar**
Azure Solutions Architect & AI Architect 
[LinkedIn]([https://www.linkedin.com/in/praveen11singh](https://www.linkedin.com/in/praveen-kumar-b52a1a1a0/)) · [GitHub](https://github.com/praveen11singh) 
