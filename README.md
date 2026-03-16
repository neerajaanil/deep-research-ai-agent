# Deep Research Agent

A production-ready AI agent system for conducting deep research on any topic. The system uses multiple specialized agents to plan searches, gather information, synthesize reports, and optionally send results via email.

## Features

- 🔍 **Multi-Agent Architecture**: Specialized agents for planning, searching, writing, and emailing
- 🌐 **Web Search Integration**: Automated web searches using OpenAI's WebSearchTool
- 📊 **Comprehensive Reports**: Detailed markdown reports with summaries and follow-up questions
- 📧 **Email Integration**: Optional email delivery via SendGrid
- 🎨 **Modern UI**: Clean Gradio interface for easy interaction
- 🏗️ **Production Ready**: Structured codebase with proper error handling and logging

## Architecture

The system consists of four specialized agents:

1. **Planner Agent**: Creates a research plan with multiple search queries
2. **Search Agent**: Performs web searches and summarizes results
3. **Writer Agent**: Synthesizes search results into comprehensive reports
4. **Email Agent**: Formats and sends reports via email

```
deep_research_agent/
├── deep_research_agent/
│   ├── __init__.py
│   ├── config.py          # Configuration management
│   ├── manager.py          # Research orchestration
│   ├── app.py             # Gradio application
│   └── agents/
│       ├── __init__.py
│       ├── planner.py     # Search planning agent
│       ├── search.py      # Web search agent
│       ├── writer.py      # Report writing agent
│       └── email.py       # Email sending agent
├── requirements.txt
├── .env.example
└── README.md
```

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and set:
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPENAI_MODEL`: Model to use (default: gpt-4o-mini)
- `SENDGRID_API_KEY`: SendGrid API key (optional, for email)
- `EMAIL_FROM` and `EMAIL_TO`: Email addresses (optional)
- `HOW_MANY_SEARCHES`: Number of searches per query (default: 5)

### 3. Run the Application

```bash
python -m deep_research_agent.app
```

Or use the run script:

```bash
python run.py
```

The application will start on `http://localhost:7860`.

## Usage

1. Enter a research query in the text box
2. Click "Run Research" or press Enter
3. Watch the progress as the agent:
   - Plans search queries
   - Performs web searches
   - Writes a comprehensive report
   - Sends the report via email (if configured)
4. View the final report in the interface

## Configuration

All settings are managed through environment variables:

- **OpenAI**: API key and model selection
- **SendGrid**: Optional email service configuration
- **Research**: Number of searches to perform
- **Server**: Host, port, and sharing options

## Requirements

- Python 3.8+
- OpenAI API key
- Internet connection (for web searches and API calls)
- SendGrid account (optional, for email functionality)

## License

This project is provided as-is for showcasing AI agent capabilities.
