from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_huggingface import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from transformers import pipeline
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class CollaborativeLanguageChain:
    def __init__(self):
        # Initialize models
        self.openai_model = ChatOpenAI(
            openai_api_key=os.getenv('OPENAI_API_KEY'), 
            model='gpt-3.5-turbo'
        )
        self.claude_model = ChatAnthropic(
            anthropic_api_key=os.getenv('ANTHROPIC_API_KEY'), 
            model='claude-2.1'
        )
        
        # Hugging Face model for text generation
        text_generation_pipeline = pipeline(
            'text-generation', 
            model='gpt2',
            max_new_tokens=100,  
            truncation=True
        )
        self.huggingface_model = HuggingFacePipeline(pipeline=text_generation_pipeline)

    def collaborative_story_generation(self, initial_prompt):
        """
        Demonstrate a collaborative story generation process:
        1. OpenAI generates initial story outline
        2. Hugging Face expands on the outline
        3. Claude refines and adds depth to the story
        """
        # Step 1: OpenAI generates story outline
        openai_prompt = PromptTemplate(
            input_variables=["topic"],
            template="Create a concise, imaginative story outline about {topic}."
        )
        openai_chain = openai_prompt | self.openai_model
        story_outline = openai_chain.invoke({"topic": initial_prompt})
        print("🤖 OpenAI Story Outline:")
        print(story_outline.content)
        print("\n---\n")

        # Step 2: Hugging Face expands the outline
        huggingface_prompt = PromptTemplate(
            input_variables=["outline"],
            template="Expand this story outline with creative details: {outline}"
        )
        huggingface_chain = huggingface_prompt | self.huggingface_model
        expanded_story = huggingface_chain.invoke({"outline": story_outline.content})
        print("🤖 Hugging Face Story Expansion:")
        print(expanded_story)
        print("\n---\n")

        # Step 3: Claude refines the story
        claude_prompt = PromptTemplate(
            input_variables=["expanded_story"],
            template="Review and enhance this story, adding depth and emotional nuance: {expanded_story}"
        )
        claude_chain = claude_prompt | self.claude_model
        final_story = claude_chain.invoke({"expanded_story": expanded_story})
        print("🤖 Claude Story Refinement:")
        print(final_story.content)

def main():
    collaborative_chain = CollaborativeLanguageChain()
    collaborative_chain.collaborative_story_generation("a future where humans and AI coexist")

if __name__ == "__main__":
    main()
