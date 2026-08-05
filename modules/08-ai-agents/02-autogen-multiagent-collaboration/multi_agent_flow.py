"""
Simple multi-agent loop simulation.
This example runs three agents exchanging messages. Replace with real model calls in production.
"""
import time
import json

from typing import List, Dict

with open('modules/08-ai-agents/02-autogen-multiagent-collaboration/autogen_config.json') as f:
    CONFIG = json.load(f)

class Agent:
    def __init__(self, name, role):
        self.name = name
        self.role = role

    def act(self, message: str) -> str:
        # Placeholder: echo with role context
        return f"[{self.name}] processed: {message}"

def run_multi_agent_flow(user_prompt: str, max_turns: int = 5):
    agents = [Agent(a['name'], a['role']) for a in CONFIG['agents']]
    history: List[Dict] = []
    current = user_prompt
    for turn in range(max_turns):
        for agent in agents:
            out = agent.act(current)
            history.append({'agent': agent.name, 'output': out})
            current = out
            time.sleep(0.1)
    return history

if __name__ == '__main__':
    h = run_multi_agent_flow('Please design a deployment that scales GPUs for inference')
    for entry in h:
        print(entry)
