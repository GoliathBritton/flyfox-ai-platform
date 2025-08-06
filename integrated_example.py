#!/usr/bin/env python3
"""
Integrated example demonstrating OpenAI Agents SDK with Dynex quantum computing.
This example shows how to use both systems together for advanced AI applications.
"""

import asyncio
import configparser
from agents import Agent, Runner, function_tool
import dynex

@function_tool
def solve_quantum_problem(problem_type: str) -> str:
    """
    Solve a quantum computing problem using Dynex.
    
    Args:
        problem_type: Type of problem ('qubo', 'ising', 'optimization')
        
    Returns:
        Solution or status information
    """
    try:
        # Load dynex configuration
        config = configparser.ConfigParser()
        config.read('dynex.ini')
        
        print(f"Solving {problem_type} problem with Dynex...")
        
        # Example: Check account status first
        try:
            status = dynex.account_status()
            print(f"Dynex account status: {status}")
        except Exception as e:
            print(f"Account status check failed: {e}")
        
        # Example: Estimate costs for a problem
        try:
            # This would be a real problem in practice
            cost_estimate = dynex.estimate_costs()
            print(f"Cost estimate: {cost_estimate}")
        except Exception as e:
            print(f"Cost estimation failed: {e}")
        
        return f"Dynex {problem_type} problem processing initiated. Check account for results."
        
    except Exception as e:
        return f"Error processing quantum problem: {e}"

@function_tool
def get_dynex_config() -> str:
    """Get the current Dynex configuration."""
    try:
        config = configparser.ConfigParser()
        config.read('dynex.ini')
        
        if 'DYNEX' in config:
            return f"Dynex configured with endpoint: {config['DYNEX']['API_ENDPOINT']}"
        else:
            return "Dynex configuration not found"
    except Exception as e:
        return f"Error reading Dynex config: {e}"

async def main():
    """Main function demonstrating integrated capabilities."""
    
    # Create an agent with quantum computing capabilities
    agent = Agent(
        name="quantum_assistant",
        instructions="""You are an AI assistant with access to quantum computing capabilities through Dynex. 
        You can help users solve complex optimization problems, QUBO problems, and Ising model problems.
        When users ask about quantum computing or optimization problems, use the available tools to help them.
        Always explain what you're doing and provide clear information about the quantum computing process.""",
        tools=[solve_quantum_problem, get_dynex_config]
    )
    
    print("🤖 Quantum Computing Assistant")
    print("=" * 50)
    print("This agent combines OpenAI's language capabilities with Dynex quantum computing.")
    print()
    
    # Example conversations
    conversations = [
        "What quantum computing capabilities do you have?",
        "Can you help me solve a QUBO optimization problem?",
        "What's the current status of the Dynex quantum computing service?",
        "Explain how quantum computing can help with optimization problems."
    ]
    
    for i, message in enumerate(conversations, 1):
        print(f"\n--- Conversation {i} ---")
        print(f"User: {message}")
        
        result = await Runner.run(agent, message)
        print(f"Assistant: {result}")
        
        if i < len(conversations):
            print("\n" + "-" * 30)

if __name__ == "__main__":
    asyncio.run(main()) 