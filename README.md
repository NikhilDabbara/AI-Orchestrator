AI Orchestrator

A full-stack, multi-agent AI chat application. This project intelligently routes user prompts to the most capable AI model (Local Ollama for coding, Cloud Gemini for general knowledge) while maintaining persistent cross-session memory using MySQL.

Features

Intelligent Routing: Uses Groq (Llama-3) to analyze prompts and route them to specific specialist models.

Local & Cloud Agents: Integrates local offline execution via Ollama (qwen2.5-coder) and cloud execution via Google Gemini.

Persistent Memory: All sessions and messages are stored in a local MySQL database.

Context Compression: Automatically summarizes long chat histories using Gemini to save tokens and maintain speed.

Modern UI: A responsive, Vanilla JS & Tailwind CSS frontend inspired by Google Gemini.

Prerequisites

To run this project on your local machine, you will need:

Python 3.8+

MySQL Server & MySQL Workbench

Ollama (Running locally)

API Keys for Groq and Google Gemini

Setup Instructions

1. Database Setup

Open MySQL Workbench.

Run the SQL script found in database/schema.sql to create the AI_DB database and tables.

2. Local AI Setup

Install Ollama.

Open your terminal and pull the required model:

ollama run qwen2.5-coder:7b


3. Environment Setup

Clone this repository.

Install the required Python packages:

pip install -r requirements.txt


Create a .env file in the root directory and add your credentials:

# Database
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=AI_DB

# API Keys
GROQ_API_KEY=your_groq_key
GEMINI_API_KEY=your_gemini_key


4. Running the Application

Start the FastAPI backend server:

fastapi dev server.py


Open the frontend UI by double-clicking frontend/index.html in your web browser.