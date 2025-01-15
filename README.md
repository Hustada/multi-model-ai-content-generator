# 🤖 Multi-Model AI Content Generator

## Overview
A cutting-edge Streamlit application that leverages multiple AI models to generate technical content and code examples dynamically.

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![AI Models](https://img.shields.io/badge/models-OpenAI%20%7C%20Anthropic%20%7C%20Google-green)

## 🌟 Features

### Multi-Model Collaboration
- **Research Phase**: Uses OpenAI GPT-4 to generate structured insights
- **Creative Development**: Employs Claude for engaging content generation
- **Code Generation**: Utilizes OpenAI GPT-3.5 for practical code examples
- **Fallback Mechanism**: Seamlessly switches to Google Gemini if primary models fail

### Key Capabilities
- Generate technical blog posts on any topic
- Create relevant, runnable code snippets
- Real-time progress tracking
- Detailed logging
- Flexible model integration

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- API Keys:
  - OpenAI
  - Anthropic
  - Google (Gemini)

### Installation
1. Clone the repository
```bash
git clone https://github.com/yourusername/ai-content-generator.git
cd ai-content-generator
```

2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
Create a `.env` file with:
```
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GEMINI_API_KEY=your_gemini_key
```

### Running the Application
```bash
streamlit run interactive_content_generator.py
```

## 🔧 Technologies

### AI Models
- OpenAI GPT-4
- Claude (Anthropic)
- Google Gemini

### Libraries
- Langchain
- Streamlit
- Black (Code Formatting)
- Isort (Import Sorting)

## 🤝 Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.

## 🌐 Contact
Your Name - your.email@example.com

Project Link: [https://github.com/yourusername/ai-content-generator](https://github.com/yourusername/ai-content-generator)
