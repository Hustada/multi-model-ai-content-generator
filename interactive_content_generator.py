import os
import time
import streamlit as st
from typing import Dict, Any
from dotenv import load_dotenv
from loguru import logger

# Langchain and AI imports
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field

# Code formatting
import black
import isort
import re

# Retry and error handling
from tenacity import retry, stop_after_attempt, wait_exponential
import anthropic

# Configure logging
logger.add("content_generation.log", rotation="10 MB")

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
        
        self.backup_model = ChatGoogleGenerativeAI(
            model='gemini-pro',
            temperature=0.5,
            api_key=os.getenv('GEMINI_API_KEY')
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

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry_error_callback=lambda retry_state: retry_state.outcome.result()
    )
    def generate_with_retry(self, model, prompt, max_tokens=1000):
        """
        Retry mechanism for model generation with exponential backoff
        Fallback to alternative models if primary model fails
        """
        try:
            return model.invoke(prompt)
        except (anthropic.RateLimitError, anthropic.APIError) as e:
            logger.warning(f"Primary model failed: {e}. Attempting backup model...")
            try:
                return self.backup_model.invoke(prompt)
            except Exception as backup_error:
                logger.error(f"Backup model also failed: {backup_error}")
                raise

    def extract_code_block(self, model_output: str) -> str:
        """
        Extract code block from model output using multiple strategies
        """
        # Strategy 1: Look for triple backtick code blocks
        code_match = re.search(r'```(?:python)?\n(.*?)```', model_output, re.DOTALL)
        if code_match:
            return code_match.group(1).strip()
        
        # Strategy 2: Look for code between specific markers
        code_match = re.search(r'<code>(.*?)</code>', model_output, re.DOTALL)
        if code_match:
            return code_match.group(1).strip()
        
        # Strategy 3: Use the entire output if it looks like code
        if model_output.strip().startswith('def ') or model_output.strip().startswith('import '):
            return model_output.strip()
        
        # Fallback: Return a default example
        return "# No code could be extracted\ndef example_function():\n    pass"

    def generate_technical_content(self, topic: str, progress_callback=None, log_callback=None) -> Dict[str, Any]:
        """
        Collaborative process to generate a technical blog post with code example
        """
        # Logging helper
        def log_and_progress(message, percent=None):
            if log_callback:
                log_callback(message)
            if progress_callback and percent is not None:
                progress_callback(percent, message)
            logger.info(message)

        # Stage 1: Research and Topic Exploration
        log_and_progress(f"Starting research phase for topic: {topic}", 0)
        
        research_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="You are a technical research expert. Provide comprehensive insights."),
            HumanMessage(content=f"Research and analyze the technical aspects of: {topic}")
        ])
        research_chain = research_prompt | self.research_model
        blog_structure = self.generate_with_retry(research_chain, {})
        
        log_and_progress("Research phase completed", 25)

        # Stage 2: Creative Content Development
        log_and_progress("Starting creative content development", 25)
        
        creative_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="You are a creative technical writer. Develop engaging content."),
            HumanMessage(content=f"Develop a detailed blog post based on this research: {blog_structure.content}")
        ])
        creative_chain = creative_prompt | self.creative_model
        full_blog_content = self.generate_with_retry(creative_chain, {})
        
        log_and_progress("Creative content development completed", 50)

        # Stage 3: Code Example Generation
        log_and_progress("Starting code example generation", 50)
        
        code_prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="You are an expert programmer. Generate a practical code example related to the topic."),
            HumanMessage(content=f"Create a Python code example for this topic: {topic}. Provide a complete, runnable code snippet with comments explaining its purpose and functionality.")
        ])
        code_chain = code_prompt | self.code_model | StrOutputParser()
        code_example_text = self.generate_with_retry(code_chain, {})
        
        log_and_progress("Code example generation completed", 75)

        # Stage 4: Code Extraction and Formatting
        log_and_progress("Extracting and formatting code", 75)
        
        def format_code(code: str, language: str = 'python') -> str:
            """Format and optimize code"""
            try:
                if language.lower() == 'python':
                    formatted_code = black.format_str(code, mode=black.FileMode())
                    formatted_code = isort.code(formatted_code)
                    return formatted_code
                return code
            except Exception as e:
                logger.error(f"Code formatting error: {e}")
                return code

        # Extract code block and format
        extracted_code = self.extract_code_block(code_example_text)
        formatted_code = format_code(extracted_code)
        
        log_and_progress("Content generation completed", 100)

        # Combine all outputs
        return {
            'blog_structure': blog_structure.content,
            'blog_content': full_blog_content.content,
            'code_example': {
                'original': extracted_code,
                'formatted': formatted_code,
                'language': 'python',
                'explanation': 'Code example generated for the given topic'
            }
        }

def main():
    # Streamlit UI
    st.set_page_config(page_title="AI Content Generator", page_icon="🤖")
    st.title("🚀 AI-Powered Technical Content Generator")

    # Load environment variables
    load_dotenv()

    # Logging area in Streamlit
    log_container = st.empty()
    log_messages = []

    def update_log(message):
        log_messages.append(message)
        if len(log_messages) > 10:
            log_messages.pop(0)
        log_container.text('\n'.join(log_messages))

    # Topic input
    topic = st.text_input("Enter a technical topic for content generation", 
                          placeholder="e.g., Building a Real-Time Collaborative AI Assistant")

    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()

    def update_progress(percent, message):
        progress_bar.progress(percent)
        status_text.text(message)
        update_log(message)

    # Generation button
    if st.button("Generate Content"):
        if not topic:
            st.error("Please enter a topic")
            return

        # Initialize content generator
        content_generator = TechContentGenerator()

        try:
            # Generate content with progress tracking
            result = content_generator.generate_technical_content(
                topic, 
                progress_callback=update_progress,
                log_callback=update_log
            )

            # Display results
            st.subheader("📝 Generated Blog Post")
            st.write(result['blog_content'])

            st.subheader("💻 Code Example")
            st.code(result['code_example']['formatted'], language='python')

            # Optional: Download buttons
            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    label="Download Blog Post",
                    data=result['blog_content'],
                    file_name=f"{topic.replace(' ', '_')}_blog_post.md",
                    mime="text/markdown"
                )
            with col2:
                st.download_button(
                    label="Download Code Example",
                    data=result['code_example']['formatted'],
                    file_name=f"{topic.replace(' ', '_')}_code_example.py",
                    mime="text/python"
                )

        except Exception as e:
            st.error(f"An error occurred: {e}")
            logger.error(f"Content generation error: {e}")
            update_log(f"Error: {e}")

if __name__ == "__main__":
    main()
