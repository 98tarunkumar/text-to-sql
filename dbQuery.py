import ollama
from typing import List, Dict, Any
import json
import mysql.connector
from mysql.connector import Error
import re
import csv
from datetime import datetime
import pandas as pd
import os
from dotenv import load_dotenv

class DatabaseQueryAssistant:
    def __init__(self, model_name: str = "qwen:1.8b"):
        # Load environment variables
        load_dotenv()
        
        self.model = model_name
        self.system_prompt = """
        You are a database query assistant. When given questions about database operations:
        1. Explain the query in simple terms
        2. Provide the actual SQL query if applicable
        3. Give best practices related to the query
        Be concise and technical in your responses.
        """
        self.db_connection = None
        self.connect_to_database()

    def connect_to_database(self):
        """Connect to MySQL database"""
        try:
            self.db_connection = mysql.connector.connect(
                host=os.getenv('DB_HOST', '127.0.0.1'),
                user=os.getenv('DB_USER', 'root'),
                password=os.getenv('DB_PASSWORD'),
                database=os.getenv('DB_NAME')
            )
            print("Successfully connected to the database!")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")

    def save_to_csv(self, results: List[Dict], query: str):
        """Save query results to CSV file"""
        try:
            if not results:
                print("No results to save")
                return
            
            # Create filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"query_results_{timestamp}.csv"
            
            # Convert to DataFrame and save to CSV
            df = pd.DataFrame(results)
            df.to_csv(filename, index=False)
            
            # Also save query metadata
            with open(f"query_metadata_{timestamp}.txt", 'w') as f:
                f.write(f"Query executed: {query}\n")
                f.write(f"Timestamp: {datetime.now()}\n")
                f.write(f"Number of results: {len(results)}")
            
            print(f"Results saved to {filename}")
            return filename
            
        except Exception as e:
            print(f"Error saving to CSV: {str(e)}")
            return None

    def execute_query(self, query: str) -> List[Dict]:
        """Execute SQL query and return results"""
        try:
            print(f"Attempting to execute query: {query}")
            if not self.db_connection or not self.db_connection.is_connected():
                print("Reconnecting to database...")
                self.connect_to_database()
                
            cursor = self.db_connection.cursor(dictionary=True)
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            print(f"Query executed successfully. Results: {results}")
            return results
        except Error as e:
            print(f"Database error: {str(e)}")
            return [{"error": str(e)}]

    def get_query_response(self, question: str) -> str:
        """Get response from Qwen model and execute if it's a valid SQL query"""
        try:
            # Get AI response
            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        'role': 'system',
                        'content': self.system_prompt
                    },
                    {
                        'role': 'user',
                        'content': question
                    }
                ]
            )
            ai_response = response['message']['content']
            print(f"AI Response: {ai_response}")

            # Extract SQL query
            sql_query = None
            sql_match = re.search(r'```sql\n(.*?)\n```', ai_response, re.DOTALL)
            if sql_match:
                sql_query = sql_match.group(1).strip()
            else:
                sql_match = re.search(r'(SELECT|INSERT|UPDATE|DELETE|SHOW).*?;', ai_response, re.DOTALL | re.IGNORECASE)
                if sql_match:
                    sql_query = sql_match.group(0).strip()

            print(f"Extracted SQL Query: {sql_query}")

            if sql_query:
                # Execute query
                query_results = self.execute_query(sql_query)
                
                # Save results to CSV
                csv_file = self.save_to_csv(query_results, sql_query)
                
                # Add CSV info to response
                result_info = "\n\nQuery Results:\n" + json.dumps(query_results, indent=2)
                if csv_file:
                    result_info += f"\n\nResults saved to: {csv_file}"
                
                return ai_response + result_info
            else:
                return ai_response + "\n\nNo SQL query found in the response."

        except Exception as e:
            print(f"Error in get_query_response: {str(e)}")
            return f"Error: {str(e)}"

    def __del__(self):
        """Close database connection when object is destroyed"""
        if self.db_connection and self.db_connection.is_connected():
            self.db_connection.close()

def main():
    # Initialize the assistant
    db_assistant = DatabaseQueryAssistant()
    
    print("Database Query Assistant (using Qwen model)")
    print("Type 'quit' to exit\n")

    while True:
        # Get input from user
        query = input("\nEnter your database question: ")
        
        # Check if user wants to quit
        if query.lower() in ['quit', 'exit', 'q']:
            break
            
        # Get and print response
        response = db_assistant.get_query_response(query)
        print("\nResponse:", response)
        result=db_assistant.execute_query(response)
        print(result)
        print("\n" + "="*50)

if __name__ == "__main__":
    main()
