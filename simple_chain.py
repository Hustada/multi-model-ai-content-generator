from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize the language model
llm = OpenAI(openai_api_key=os.getenv('OPENAI_API_KEY'))

# Create a simple prompt template
prompt = PromptTemplate(
    input_variables=["topic"],
    template="Give me a creative 3-sentence explanation about {topic}."
)

# Create a chain
def explain_topic(topic):
    # Format the prompt
    formatted_prompt = prompt.format(topic=topic)
    
    # Run the chain
    result = llm.invoke(formatted_prompt)
    
    return result

# Example usage
if __name__ == "__main__":
    print(explain_topic("artificial intelligence"))
