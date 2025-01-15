import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.agents import AgentAction, AgentFinish
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Load environment variables
load_dotenv()

class MultiModelCollaborativeAgent:
    def __init__(self):
        # Initialize different models with specific roles
        self.research_model = ChatOpenAI(
            model='gpt-4-turbo',
            temperature=0.7,
            api_key=os.getenv('OPENAI_API_KEY')
        )
        
        self.creative_model = ChatAnthropic(
            model='claude-2.1',
            temperature=0.8,
            api_key=os.getenv('ANTHROPIC_API_KEY')
        )
        
        self.analytical_model = ChatOpenAI(
            model='gpt-3.5-turbo',
            temperature=0.2,
            api_key=os.getenv('OPENAI_API_KEY')
        )

    def collaborative_problem_solving(self, initial_problem: str):
        """
        A multi-stage collaborative problem-solving approach
        with specialized AI agents working together
        """
        # Stage 1: Research and Information Gathering
        research_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""
            You are a meticulous research assistant. 
            Your task is to gather comprehensive information about the given problem.
            Provide a detailed, objective analysis with key insights and background context.
            """),
            HumanMessage(content=f"Research and analyze the following problem in depth: {initial_problem}")
        ])
        research_chain = research_prompt | self.research_model
        research_output = research_chain.invoke({})
        print("🔬 Research Phase Output:")
        print(research_output.content)
        print("\n--- Next Phase ---\n")

        # Stage 2: Creative Solution Generation
        creative_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""
            You are a highly creative problem solver. 
            Using the research insights, generate innovative and unconventional solutions.
            Think outside the box and propose approaches that others might overlook.
            """),
            HumanMessage(content=f"Generate creative solutions based on this research: {research_output.content}")
        ])
        creative_chain = creative_prompt | self.creative_model
        creative_output = creative_chain.invoke({})
        print("💡 Creative Solutions Phase:")
        print(creative_output.content)
        print("\n--- Next Phase ---\n")

        # Stage 3: Analytical Evaluation and Refinement
        analytical_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""
            You are a critical and analytical problem solver.
            Evaluate the proposed creative solutions rigorously.
            Assess feasibility, potential challenges, and provide constructive recommendations.
            """),
            HumanMessage(content=f"Critically analyze these creative solutions: {creative_output.content}")
        ])
        analytical_chain = analytical_prompt | self.analytical_model
        analytical_output = analytical_chain.invoke({})
        print("📊 Analytical Evaluation Phase:")
        print(analytical_output.content)

        # Final Synthesis
        synthesis_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""
            You are a synthesizer who integrates insights from research, creativity, and analysis.
            Combine the best elements from each phase into a comprehensive, actionable strategy.
            """),
            HumanMessage(content=f"""
            Synthesize a final strategy using these inputs:
            Research Phase: {research_output.content}
            Creative Solutions: {creative_output.content}
            Analytical Evaluation: {analytical_output.content}
            """)
        ])
        synthesis_chain = synthesis_prompt | self.creative_model
        final_strategy = synthesis_chain.invoke({})
        print("\n🌟 Final Collaborative Strategy:")
        print(final_strategy.content)

        return {
            'research': research_output.content,
            'creative_solutions': creative_output.content,
            'analytical_evaluation': analytical_output.content,
            'final_strategy': final_strategy.content
        }

def main():
    collaborative_agent = MultiModelCollaborativeAgent()
    
    # Example problem: Addressing urban sustainability
    problem = "How can cities become more sustainable and resilient to climate change?"
    
    collaborative_result = collaborative_agent.collaborative_problem_solving(problem)

if __name__ == "__main__":
    main()
