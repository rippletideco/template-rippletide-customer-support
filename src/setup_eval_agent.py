#!/usr/bin/env python3
"""
Rippletide Evaluation Agent Setup Script

Creates an evaluation agent for testing and evaluation purposes.
Based on starter/rippletide_client pattern.

Usage:
    uv run src/setup_eval_agent.py
    uv run src/setup_eval_agent.py --pdf knowledge.pdf
"""

import sys
import argparse
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rippletide_client import RippletideEvalClient

# Hardcoded API key - update this with your API key from https://eval.rippletide.com
RIPPLETIDE_API_KEY = ""
# URL for evaluation API
RIPPLETIDE_EVAL_BASE_URL = "https://rippletide-backend-staging-gqdsh7h8drgfazdj.westeurope-01.azurewebsites.net"

def main():
    """Main setup function"""
    parser = argparse.ArgumentParser(description="Setup Rippletide Evaluation Agent")
    parser.add_argument(
        "--pdf",
        type=str,
        help="Path to PDF file for question extraction"
    )
    
    args = parser.parse_args()
    
    client = RippletideEvalClient(api_key=RIPPLETIDE_API_KEY, base_url=RIPPLETIDE_EVAL_BASE_URL)
    
    agent = client.create_agent(name="Evaluation Agent")
    agent_id = agent['id']
    
    if args.pdf:
        pdf_path = Path(args.pdf)
        if not pdf_path.exists():
            print(f"Error: PDF file not found: {pdf_path}", file=sys.stderr)
            sys.exit(1)
        client.extract_questions_from_pdf(
            agent_id=agent_id,
            pdf_path=str(pdf_path)
        )

    # print the report of the evaluation
    report = client.evaluate(
        agent_id=agent_id,
        question="What is the capital of France?",
        expected_answer="Paris"
    )
    print(agent_id)
    print(report)

if __name__ == "__main__":
    main()

