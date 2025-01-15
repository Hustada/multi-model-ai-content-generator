import os
from typing import Dict, Any
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field
import black
import isort

# Load environment variables
load_dotenv()

class TechContentGenerator:
    def __init__(self):
        # Initialize specialized models
        self.research_model = ChatOpenAI(
            model='gpt-4-turbo',
            temperature=0.3,
            api_key=os.getenv('OPENAI_API_KEY')
        )
        
        self.creative_model = ChatAnthropic(
            model='claude-2.1',
            temperature=0.7,
            api_key=os.getenv('ANTHROPIC_API_KEY')
        )
        
        self.code_model = ChatOpenAI(
            model='gpt-3.5-turbo',
            temperature=0.2,
            api_key=os.getenv('OPENAI_API_KEY')
        )

    class BlogPostStructure(BaseModel):
        """Structured output for blog post generation"""
        title: str = Field(description="Catchy and informative blog post title")
        introduction: str = Field(description="Engaging introduction to the topic")
        key_sections: list[str] = Field(description="Main sections of the blog post")
        conclusion: str = Field(description="Summarizing conclusion")

    class CodeExample(BaseModel):
        """Structured output for code generation"""
        language: str = Field(description="Programming language for the code")
        purpose: str = Field(description="Brief description of the code's purpose")
        code: str = Field(description="Actual code implementation")
        explanation: str = Field(description="Detailed explanation of the code")

    def generate_technical_content(self, topic: str) -> Dict[str, Any]:
        """
        Collaborative process to generate a technical blog post with code example
        """
        # Stage 1: Research and Topic Exploration
        research_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="You are a technical research expert. Provide comprehensive insights."),
            HumanMessage(content=f"Research and analyze the technical aspects of: {topic}")
        ])
        research_parser = PydanticOutputParser(pydantic_object=self.BlogPostStructure)
        research_chain = research_prompt | self.research_model
        blog_structure = research_chain.invoke({})
        print("🔬 Blog Post Structure:")
        print(blog_structure.content)

        # Stage 2: Creative Content Development
        creative_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="You are a creative technical writer. Develop engaging content."),
            HumanMessage(content=f"Develop a detailed blog post based on this research: {blog_structure.content}")
        ])
        creative_chain = creative_prompt | self.creative_model
        full_blog_content = creative_chain.invoke({})
        print("\n✍️ Blog Content:")
        print(full_blog_content.content)

        # Stage 3: Code Example Generation
        code_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="You are an expert programmer. Generate a practical code example."),
            HumanMessage(content=f"Create a code example related to this blog content: {full_blog_content.content}")
        ])
        code_parser = PydanticOutputParser(pydantic_object=self.CodeExample)
        code_chain = code_prompt | self.code_model
        code_example = code_chain.invoke({
            "format_instructions": code_parser.get_format_instructions()
        })
        print("\n💻 Code Example:")
        print(code_example)

        # Stage 4: Code Formatting and Optimization
        def format_code(code: str, language: str = 'python') -> str:
            """Format and optimize code"""
            try:
                if language.lower() == 'python':
                    # Use black for formatting
                    formatted_code = black.format_str(code, mode=black.FileMode())
                    # Use isort to organize imports
                    formatted_code = isort.code(formatted_code)
                    return formatted_code
                return code
            except Exception as e:
                print(f"Code formatting error: {e}")
                return code

        formatted_code = format_code(code_example.code)
        print("\n🧹 Formatted Code:")
        print(formatted_code)

        # Combine all outputs
        return {
            'blog_structure': blog_structure.content,
            'blog_content': full_blog_content.content,
            'code_example': {
                'original': code_example.code,
                'formatted': formatted_code,
                'language': code_example.language,
                'explanation': code_example.explanation
            }
        }

def main():
    # Example usage
    content_generator = TechContentGenerator()
    result = content_generator.generate_technical_content(
        "Building a Real-Time Collaborative AI Assistant"
    )
    
    # Optional: Write outputs to files
    os.makedirs('outputs', exist_ok=True)
    
    with open('outputs/blog_post.md', 'w') as f:
        f.write(result['blog_content'])
    
    with open('outputs/code_example.py', 'w') as f:
        f.write(result['code_example']['formatted'])

if __name__ == "__main__":
    main()
