# Customer Support Agent - Rippletide

<p align="center">
  <img style="border-radius:10px" src="img/cover.png" alt="Rippletide x Blaxel" width="90%"/>
</p>

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Rippletide](https://img.shields.io/badge/Rippletide-powered-brightgreen.svg)](https://rippletide.com/)
[![AI Agents](https://img.shields.io/badge/AI-Agents-orange.svg)](https://rippletide.com/)

</div>

An intelligent customer support agent powered by Rippletide's enterprise-grade AI platform. This template supports **two ways** to create Rippletide agents:

1. **SDK Agent Creation** - Full-featured agents with tool calls, user inputs, guardrails (like `postgoux/backend/src/agent/custom_agent`)
2. **Evaluation Agent Creation** - Agents for evaluation with PDF extraction (like `starter/rippletide_client`)

## Quick Start

```bash
# Clone the repository
git clone https://github.com/blaxel-ai/template-rippletide-customer-support.git

# Navigate to the project directory
cd template-rippletide-customer-support

# Install dependencies
uv sync

# Create SDK agent configuration
cp agent_config.json.example agent_config.json
# Edit agent_config.json with your configuration (optional)

# Run setup to create your agent in Rippletide
uv run src/setup_sdk_agent.py agent_config.json
# This will output an Agent ID - add it to your .env file

# Start the server
bl serve --hotreload

# In another terminal, test the agent
bl chat --local template-rippletide-customer-support
```

## Prerequisites

- **Python:** 3.10 or later
- **[UV](https://github.com/astral-sh/uv):** An extremely fast Python package and project manager, written in Rust
- **Rippletide API Key:** Go to [https://eval.rippletide.com](https://eval.rippletide.com), login, go to settings and get your API key.
- **Blaxel Platform Setup:** Complete Blaxel setup by following the [quickstart guide](https://docs.blaxel.ai/Get-started#quickstart)
  - **[Blaxel CLI](https://docs.blaxel.ai/Get-started):** Ensure you have the Blaxel CLI installed. If not, install it globally:
    ```bash
    curl -fsSL https://raw.githubusercontent.com/blaxel-ai/toolkit/main/install.sh | BINDIR=/usr/local/bin sudo -E sh
    ```
  - **Blaxel login:** Login to Blaxel platform
    ```bash
    bl login
    ```

## Configuration

### 1. Get Your API Key

1. Go to [https://eval.rippletide.com](https://eval.rippletide.com), login, go to settings and generate your API key
2. Update the hardcoded API key in these files:
   - `src/setup_sdk_agent.py` - Update `RIPPLETIDE_API_KEY = "your-api-key-here"`
   - `src/setup_eval_agent.py` - Update `RIPPLETIDE_API_KEY = "your-api-key-here"`
   - `src/agent.py` - Update `RIPPLETIDE_API_KEY = "your-api-key-here"`

### 2. Choose Agent Creation Method

#### Option A: SDK Agent (Production)

```bash
cp agent_config.json.example agent_config.json
# Edit agent_config.json with your config
uv run src/setup_sdk_agent.py agent_config.json
```

#### Option B: Evaluation Agent

```bash
# Basic evaluation agent
uv run src/setup_eval_agent.py

# With PDF extraction
uv run src/setup_eval_agent.py --pdf knowledge.pdf
```

### 3. Add Agent ID

After setup, add to `.env`:
```env
RIPPLETIDE_AGENT_ID=your-agent-id-here
```

## Toy Examples

### Example 1: Simple SDK Agent

```python
from src.rippletide_client import RippletideAgent

# Initialize
agent = RippletideAgent(api_key="your-api-key")

# Create agent
agent_data = agent.create_agent(
    name="Toy Agent",
    prompt="You are a helpful assistant that answers questions about toys."
)

# Simple config
config = {
    "agent_purpose": "Answer questions about toys",
    "qa_pairs": [
        {
            "question": "What is a teddy bear?",
            "answer": "A teddy bear is a soft toy bear, typically made of fabric and filled with stuffing."
        }
    ],
    "state_predicate": {
        "question_to_evaluate": "I cannot answer that.",
        "re_evaluate": True,
        "transition_kind": "end"
    }
}

# Setup knowledge
agent.setup_agent_knowledge(agent_data["id"], config)

# Chat
response = agent.chat("What is a teddy bear?")
print(response["answer"])
```

### Example 2: SDK Agent with Tool Calls

```python
from src.rippletide_client import RippletideAgent

agent = RippletideAgent(api_key="your-api-key")
agent_data = agent.create_agent(
    name="Order Status Agent",
    prompt="You help customers check their order status."
)

config = {
    "agent_purpose": "Help customers track orders",
    "qa_pairs": [],
    "tool_calls": [
        {
            "label": "get_order_status",
            "description": "Get order status by order ID",
            "api_call_config": {
                "url": "https://api.example.com/orders/{{order_id}}",
                "method": "GET",
                "headers": {"x-api-key": "your-key"},
                "body": {}
            },
            "required_user_inputs": ["order_id"]
        }
    ],
    "user_input_collection": [
        {
            "label": "order_id",
            "description": "Order number (alphanumeric)"
        }
    ],
    "guardrails": [
        {
            "label": "privacy",
            "description": "Never share customer data"
        }
    ],
    "format_answer": "Start with 'Hello! ' and end with 'Is there anything else?'",
    "state_predicate": {
        "question_to_evaluate": "I cannot help with that.",
        "re_evaluate": True,
        "transition_kind": "end"
    }
}

agent.setup_agent_knowledge(agent_data["id"], config)
response = agent.chat("What's the status of order 12345?")
```

### Example 3: Evaluation Agent

```python
from src.rippletide_client import RippletideEvalClient

# Initialize client
client = RippletideEvalClient(api_key="your-api-key")

# Create evaluation agent
agent = client.create_agent(
    name="Eval Agent",
    seed=42,
    num_nodes=100
)

# Extract questions from PDF
result = client.extract_questions_from_pdf(
    agent_id=agent['id'],
    pdf_path="knowledge.pdf"
)
print(f"Extracted {len(result.get('qaPairs', []))} Q&A pairs")

# Get test prompts
test_prompts = client.get_test_prompts(agent['id'])
for prompt in test_prompts:
    print(f"Q: {prompt['prompt']}")
    print(f"A: {prompt.get('expectedAnswer', 'N/A')}")

# Evaluate a response
report = client.evaluate(
    agent_id=agent['id'],
    question="What is this document about?",
    expected_answer="It's about AI agents"
)
print(f"Label: {report['label']}")
print(f"Justification: {report['justification']}")
```

### Example 4: Using Setup Scripts

```bash
# SDK agent
uv run src/setup_sdk_agent.py agent_config.json

# Evaluation agent
uv run src/setup_eval_agent.py

# Evaluation agent with PDF
uv run src/setup_eval_agent.py --pdf documents/knowledge.pdf

# Evaluation agent with custom base URL
uv run src/setup_eval_agent.py --base-url http://localhost:3001
```

## 📁 Project Structure

```
blaxel/
├── src/
│   ├── rippletide_client.py   # RippletideAgent & RippletideEvalClient
│   ├── setup_sdk_agent.py     # SDK agent setup script
│   ├── setup_eval_agent.py    # Evaluation agent setup script
│   ├── agent.py                # FastAPI agent endpoint
│   ├── main.py                 # FastAPI app
│   └── middleware.py           # Request middleware
├── agent_config.json.example   # SDK agent config template
├── pyproject.toml
└── README.md
```

## Usage

### Running Locally

```bash
bl serve --hotreload
```

### Testing

```bash
bl chat --local template-rippletide-customer-support
```

### Deployment

```bash
bl deploy
```

## Support

- [Rippletide Docs](https://docs.rippletide.com/)
- [Blaxel Docs](https://docs.blaxel.ai)

## License

MIT License - see [LICENSE](LICENSE) file for details.
