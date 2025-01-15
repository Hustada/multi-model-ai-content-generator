from langchain_openai import OpenAI, ChatOpenAI
from langchain_huggingface import HuggingFacePipeline
from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import sys

# Load environment variables
load_dotenv()

def openai_example():
    """Example using OpenAI's language model"""
    try:
        openai_llm = OpenAI(openai_api_key=os.getenv('OPENAI_API_KEY'))
        
        openai_prompt = PromptTemplate(
            input_variables=["topic"],
            template="Explain {topic} in a way a 5-year-old would understand."
        )
        
        # Use the new recommended method: prompt | llm
        chain = openai_prompt | openai_llm
        return chain.invoke({"topic": "artificial intelligence"})
    except Exception as e:
        print(f"OpenAI example failed: {e}")
        return None

def huggingface_example():
    """Advanced example using Hugging Face models with more context"""
    try:
        from transformers import pipeline
        
        # Demonstrate different model capabilities
        text_generation_pipeline = pipeline(
            'text-generation', 
            model='gpt2',  # Small, accessible model
            max_length=100,
            truncation=True
        )
        
        # Create Langchain wrapper for Hugging Face pipeline
        hf_llm = HuggingFacePipeline(pipeline=text_generation_pipeline)
        
        # More complex prompt to showcase text generation
        hf_prompt = PromptTemplate(
            input_variables=["context"],
            template="Given the context of {context}, continue the story in an imaginative way."
        )
        
        # Use the new recommended method: prompt | llm
        chain = hf_prompt | hf_llm
        
        # Example context for story continuation
        story_context = "In a world where robots and humans coexist peacefully"
        return chain.invoke({"context": story_context})
    except ImportError:
        print("Hugging Face example requires PyTorch or TensorFlow. Install using: pip install torch transformers")
        return None
    except Exception as e:
        print(f"Hugging Face example failed: {e}")
        return None

def claude_example():
    """Example using Anthropic's Claude model"""
    try:
        claude_llm = ChatAnthropic(
            anthropic_api_key=os.getenv('ANTHROPIC_API_KEY'), 
            model='claude-2.1'
        )
        
        claude_prompt = PromptTemplate(
            input_variables=["topic"],
            template="Provide a detailed strategy for {topic}."
        )
        
        # Use the new recommended method: prompt | llm
        chain = claude_prompt | claude_llm
        return chain.invoke({"topic": "reducing plastic waste in oceans"}).content
    except Exception as e:
        print(f"Claude example failed: {e}")
        return None

def main():
    print("OpenAI Example:")
    openai_result = openai_example()
    print(openai_result or "No result")
    
    print("\nHugging Face Example:")
    huggingface_result = huggingface_example()
    print(huggingface_result or "No result")
    
    print("\nClaude Example:")
    claude_result = claude_example()
    print(claude_result or "No result")

if __name__ == "__main__":
    main()
