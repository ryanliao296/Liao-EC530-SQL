# Chat-Driven Spreadsheet Assistant

This is a simple command-line application that lets you interact with your data like a spreadsheet — but using natural language powered by OpenAI's GPT models. Upload CSVs, ask questions like “Show me the top 5 products by revenue,” and get answers — no SQL required!

## Features

- Load CSV files into a SQLite database
- View table schema
- Ask natural language queries
- Automatically converts your queries into SQL via OpenAI GPT-4
- Executes the SQL and displays results

## Requirements

- Python 3.8+
- [OpenAI Python SDK](https://github.com/openai/openai-python)
- Pandas
- SQLite3 (included with Python)

## Usage

Run the program
```bash
python chat.py
```

### Available Commands:

- load : load a csv into the SQLite Database
- schema : view the current database schema
- query : ask a question
- exit : quit the app 
