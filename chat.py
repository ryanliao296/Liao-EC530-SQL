import sqlite3
import pandas as pd
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")  
DB_NAME = "chat_sheet.db"
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

def load_csv_to_sqlite(csv_path, table_name):
    try:
        df = pd.read_csv(csv_path)
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Loaded '{table_name}' successfully.")
    except Exception as e:
        print(f"Error loading CSV: {e}")

def get_schema():
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    schema = []
    for (table,) in tables:
        cursor.execute(f"PRAGMA table_info({table});")
        columns = cursor.fetchall()
        cols = ", ".join([col[1] for col in columns])
        schema.append(f"- {table}({cols})")
    return "\n".join(schema)

def ask_llm(question, schema):
    prompt = f"""
You are an AI assistant converting user queries into SQL.
Database schema:
{schema}

User Query: "{question}"

Provide:
1. The SQL query (SQLite compatible)
2. A brief explanation of what the query does
Output format:
SQL: <SQL_QUERY>
Explanation: <EXPLANATION>
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful AI SQL assistant."},
            {"role": "user", "content": prompt},
        ]
    )
    return response['choices'][0]['message']['content']

def run_query(sql):
    try:
        df = pd.read_sql_query(sql, conn)
        print("\nQuery Result:")
        print(df)
    except Exception as e:
        print(f"Error executing SQL: {e}")

def main():
    print("Welcome to ChatSheet - Your Chat-Driven Spreadsheet Assistant!")
    while True:
        command = input("\nType a command (load/query/schema/exit): ").strip().lower()

        if command == 'load':
            csv_path = input("Enter path to CSV: ")
            table_name = input("Enter table name to store in DB: ")
            load_csv_to_sqlite(csv_path, table_name)

        elif command == 'schema':
            print("\nDatabase Schema:")
            print(get_schema())

        elif command == 'query':
            user_question = input("Ask your data question: ")
            schema = get_schema()
            llm_response = ask_llm(user_question, schema)
            print("\nLLM Response:")
            print(llm_response)

            if "SQL:" in llm_response:
                sql = llm_response.split("SQL:")[1].split("Explanation:")[0].strip()
                run_query(sql)

        elif command == 'exit':
            break
        else:
            print("Unknown command. Try: load, schema, query, exit")

if __name__ == '__main__':
    main()
