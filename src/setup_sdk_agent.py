#!/usr/bin/env python3
"""
Rippletide SDK Agent Setup Script

Creates a full-featured SDK agent with tool calls, user inputs, guardrails, etc.
Based on postgoux/backend/src/agent/custom_agent pattern.

Usage:
    uv run src/setup_sdk_agent.py agent_config.json
"""

import sys
import json
from pathlib import Path
from typing import Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rippletide_client import RippletideAgent

# Hardcoded API key - update this with your API key from https://eval.rippletide.com
RIPPLETIDE_API_KEY = ""

def load_config_file(file_path: Path) -> Any:
    """Load and parse a JSON configuration file"""
    with open(file_path, 'r') as f:
        return json.load(f)

def main():
    """Main setup function"""
    if len(sys.argv) < 2:
        print("Error: No configuration file provided", file=sys.stderr)
        sys.exit(1)
    
    config_path = Path(sys.argv[1])
    if not config_path.exists():
        print(f"Error: Configuration file not found: {config_path}", file=sys.stderr)
        sys.exit(1)
    
    if RIPPLETIDE_API_KEY == "your-api-key-here":
        print("Error: API key not configured", file=sys.stderr)
        sys.exit(1)
    
    agent = RippletideAgent(RIPPLETIDE_API_KEY, None)
    config = load_config_file(config_path)
    
    agent_prompt = config.get("agent_purpose", "You are a helpful assistant.")
    agent_name = config.get("agent_name", "rippletide-agent")
    
    agent_data = agent.create_agent(name=agent_name, prompt=agent_prompt)
    agent_id = agent_data["id"]
    
    agent.setup_agent_knowledge(agent_id, config)
    
    response = agent.chat("How can I track my order?")
    print(response)

if __name__ == "__main__":
    main()

