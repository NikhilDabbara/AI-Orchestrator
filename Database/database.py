# # import mysql.connector

# # conn = None
# # try:
# #     conn = mysql.connector.connect(**credentials)
# #     if conn.is_connected():
# #         print("Connection successful!")
# # except mysql.connector.Error as err:
# #     print(f"Error while connecting to MySQL: {err}")
# # finally:
# #     if conn.is_connected():
# #         conn.close()
# #         print("MySQL connection is closed.")


# import mysql.connector

# # Hardcoded for now. We will move this to a .env file later!
# credentials = {
#     "host": "localhost",
#     "user": "root",
#     "password": "Nikhil@3869", # REMEMBER to change this to your actual password
#     "database": "AI_DB"
# }

# def get_db_connection():
#     """Establishes and returns a connection to the MySQL database."""
#     try:
#         conn = mysql.connector.connect(**credentials)
#         if conn.is_connected():
#             return conn
#     except mysql.connector.Error as err:
#         print(f"Error connecting to MySQL: {err}")
#         return None

# def create_session(session_name="New Chat"):
#     """Creates a new session in the database and returns the session_id."""
#     conn = get_db_connection()
#     if conn is None:
#         return None
    
#     try:
#         # A cursor is like a temporary workspace to execute SQL commands
#         cursor = conn.cursor()
        
#         # The SQL query with a placeholder %s to prevent SQL injection
#         query = "INSERT INTO sessions (session_name) VALUES (%s)"
        
#         # Execute the query, passing the session_name as a tuple
#         cursor.execute(query, (session_name,))
        
#         # CRITICAL: You must commit() to save the changes permanently!
#         conn.commit()
        
#         # Get the ID of the session we just created
#         session_id = cursor.lastrowid
#         print(f"Created new session with ID: {session_id}")
#         return session_id
        
#     except mysql.connector.Error as err:
#         print(f"Error creating session: {err}")
#         return None
#     finally:
#         # Always close the cursor and connection when done
#         if conn.is_connected():
#             cursor.close()
#             conn.close()

# def add_message(session_id, role, content):
#     """Saves a single message (user or agent) to the database."""
#     conn = get_db_connection()
#     if conn is None:
#         return False
        
#     try:
#         cursor = conn.cursor()
        
#         # We leave out 'id' and 'created_at' because MySQL auto-generates them
#         query = "INSERT INTO messages (session_id, role, content) VALUES (%s, %s, %s)"
        
#         cursor.execute(query, (session_id, role, content))
#         conn.commit()
        
#         print(f"Message added for session {session_id} by {role}")
#         return True
        
#     except mysql.connector.Error as err:
#         print(f"Error adding message: {err}")
#         return False
#     finally:
#         if conn.is_connected():
#             cursor.close()
#             conn.close()

# def get_recent_history(session_id, limit=5):
#     """Retrieves the most recent messages for a specific session."""
#     conn = get_db_connection()
#     if conn is None:
#         return []
        
#     try:
#         # dictionary=True makes the results easier to read (like a JSON object)
#         cursor = conn.cursor(dictionary=True)
        
#         # Grab the newest messages, but sort them chronologically (oldest to newest)
#         # We order by id DESC, limit it, then order back to ASC in Python or via a subquery.
#         # For simplicity now, we just order by created_at.
#         query = """
#             SELECT role, content 
#             FROM messages 
#             WHERE session_id = %s 
#             ORDER BY created_at ASC 
#             LIMIT %s
#         """
        
#         cursor.execute(query, (session_id, limit))
        
#         # fetchall() grabs all the rows that matched our query
#         results = cursor.fetchall()
#         return results
        
#     except mysql.connector.Error as err:
#         print(f"Error retrieving history: {err}")
#         return []
#     finally:
#         if conn.is_connected():
#             cursor.close()
#             conn.close()

# # This block only runs if you run this file directly, not if you import it elsewhere
# if __name__ == "__main__":
#     print("Testing Database Functions...")
    
#     # 1. Create a session
#     my_session_id = create_session("First Test Chat")
    
#     if my_session_id:
#         # 2. Add some messages
#         add_message(my_session_id, "user", "Hello! Who are you?")
#         add_message(my_session_id, "assistant", "I am your AI Orchestrator.")
#         add_message(my_session_id, "user", "What is my database called?")
        
#         # 3. Retrieve the history
#         history = get_recent_history(my_session_id, limit=5)
        
#         print("\n--- Retrieved Chat History ---")
#         for msg in history:
#             print(f"[{msg['role'].upper()}]: {msg['content']}")
#         print("------------------------------")









import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

credentials = {
    "host": os.environ.get("DB_HOST"),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("MYSQL_PASSWORD"),
    "database": os.environ.get("DB_NAME")
}

def get_db_connection():
    """Establishes and returns a connection to the MySQL database."""
    try:
        conn = mysql.connector.connect(**credentials)
        if conn.is_connected():
            return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

def create_session(session_name="New Chat"):
    """Creates a new session in the database and returns the session_id."""
    conn = get_db_connection()
    if conn is None:
        return None
    
    try:
        # A cursor is like a temporary workspace to execute SQL commands
        cursor = conn.cursor()
        
        # The SQL query with a placeholder %s to prevent SQL injection
        query = "INSERT INTO sessions (session_name) VALUES (%s)"
        
        # Execute the query, passing the session_name as a tuple
        cursor.execute(query, (session_name,))
        
        # CRITICAL: You must commit() to save the changes permanently!
        conn.commit()
        
        # Get the ID of the session we just created
        session_id = cursor.lastrowid
        print(f"Created new session with ID: {session_id}")
        return session_id
        
    except mysql.connector.Error as err:
        print(f"Error creating session: {err}")
        return None
    finally:
        # Always close the cursor and connection when done
        if conn.is_connected():
            cursor.close()
            conn.close()

def add_message(session_id, role, content):
    """Saves a single message (user or agent) to the database."""
    conn = get_db_connection()
    if conn is None:
        return False
        
    try:
        cursor = conn.cursor()
        
        # We leave out 'id' and 'created_at' because MySQL auto-generates them
        query = "INSERT INTO messages (session_id, role, content) VALUES (%s, %s, %s)"
        
        cursor.execute(query, (session_id, role, content))
        conn.commit()
        
        print(f"Message added for session {session_id} by {role}")
        return True
        
    except mysql.connector.Error as err:
        print(f"Error adding message: {err}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def get_recent_history(session_id, limit=5):
    """Retrieves the most recent messages for a specific session."""
    conn = get_db_connection()
    if conn is None:
        return []
        
    try:
        # dictionary=True makes the results easier to read (like a JSON object)
        cursor = conn.cursor(dictionary=True)
        
        # Grab the newest messages, but sort them chronologically (oldest to newest)
        # We order by id DESC, limit it, then order back to ASC in Python or via a subquery.
        # For simplicity now, we just order by created_at.
        query = """
            SELECT role, content 
            FROM messages 
            WHERE session_id = %s 
            ORDER BY created_at ASC 
            LIMIT %s
        """
        
        cursor.execute(query, (session_id, limit))
        
        # fetchall() grabs all the rows that matched our query
        results = cursor.fetchall()
        return results
        
    except mysql.connector.Error as err:
        print(f"Error retrieving history: {err}")
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def get_all_sessions():
    """Retrieves all sessions for the sidebar."""
    conn = get_db_connection()
    if conn is None:
        return []
    try:
        cursor = conn.cursor(dictionary=True)
        # Grab all sessions, newest first
        cursor.execute("SELECT id, session_name FROM sessions ORDER BY id DESC")
        return cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error retrieving sessions: {err}")
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def delete_session(session_id):
    """Deletes a session and its messages."""
    conn = get_db_connection()
    if conn is None:
        return False
    try:
        cursor = conn.cursor()
        # Delete messages first due to foreign key constraints!
        cursor.execute("DELETE FROM messages WHERE session_id = %s", (session_id,))
        cursor.execute("DELETE FROM sessions WHERE id = %s", (session_id,))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error deleting session: {err}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# This block only runs if you run this file directly, not if you import it elsewhere
if __name__ == "__main__":
    print("Testing Database Functions...")
    
    # 1. Create a session
    my_session_id = create_session("First Test Chat")
    
    if my_session_id:
        # 2. Add some messages
        add_message(my_session_id, "user", "Hello! Who are you?")
        add_message(my_session_id, "assistant", "I am your AI Orchestrator.")
        add_message(my_session_id, "user", "What is my database called?")
        
        # 3. Retrieve the history
        history = get_recent_history(my_session_id, limit=5)
        
        print("\n--- Retrieved Chat History ---")
        for msg in history:
            print(f"[{msg['role'].upper()}]: {msg['content']}")
        print("------------------------------")