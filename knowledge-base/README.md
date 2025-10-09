# Knowledge Base Configuration

This folder contains all the configuration files needed to set up your Rippletide customer support agent. You can customize these files to match your specific business needs.

## Files Overview

### `tags.json`
Defines the categories/tags used to organize your knowledge base. Each tag has:
- `name`: Unique identifier for the tag
- `description`: What this tag represents

**Example:**
```json
{
  "name": "pricing_billing",
  "description": "Pricing, billing, payment methods, and invoicing information"
}
```

### `qanda.json`
Contains question-answer pairs that form your agent's knowledge base. Each entry has:
- `question`: The question or query
- `answer`: The accurate response
- `tags`: Array of tag names this Q&A relates to

**Example:**
```json
{
  "question": "What is your return policy?",
  "answer": "We offer a 30-day return policy for most items...",
  "tags": ["returns_refunds", "company_policies"]
}
```

### `actions.json`
Defines actions your agent can perform (like calling external tools or APIs). Each action has:
- `name`: Unique identifier for the action
- `description`: What this action does
- `what_to_do`: Detailed instructions for executing the action

**Example:**
```json
{
  "name": "check_order_status",
  "description": "Check the current status of a customer's order",
  "what_to_do": "Retrieve order information including current status, tracking number..."
}
```

### `guardrails.json`
Defines rules and constraints for your agent's behavior. Each guardrail has:
- `type`: Usually "action" for behavioral rules
- `instruction`: The rule or constraint

**Example:**
```json
{
  "type": "action",
  "instruction": "Always maintain a professional, friendly, and empathetic tone"
}
```

### `state_predicate.json`
Defines the conversation flow and decision tree for your agent. This determines how the agent navigates different customer scenarios.

The structure includes:
- `transition_kind`: Type of transition (branch, go_to_next, end)
- `question_to_evaluate`: The decision point or question
- `possible_values`: Possible outcomes/paths
- `value_to_node`: Nested decision trees for each path

## Customizing Your Knowledge Base

1. **Add Your Company Information**: Update the Q&A entries with your actual business hours, policies, and contact information

2. **Expand the Knowledge Base**: Add more questions and answers relevant to your products and services

3. **Define Your Tags**: Create tags that match your organization's structure and customer support categories

4. **Configure Actions**: Define the actual API calls or tools your agent needs to interact with your systems

5. **Set Your Guardrails**: Add company-specific compliance requirements and behavioral guidelines

6. **Design Your Flow**: Customize the state_predicate.json to match your customer support workflow

## Running the Setup

After customizing these files, run the setup script:

```bash
python src/setup.py
```

The script will read these files and create all the necessary components in your Rippletide agent.

