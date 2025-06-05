import os.path
import sqlite3

main_instance = None

# Getting the instance of main_window
def get_main_instance(main_window):
    global main_instance
    main_instance = main_window

# Creating the connection and tables
def create_connection(db_name):

    dir_name = os.path.dirname(db_name)

    try:
        if dir_name and not os.path.exists(dir_name):
            os.makedirs(dir_name)
            main_instance.write_log(f"Directory {dir_name} succesfully created")
    except Exception as e:
        main_instance.write_log(f"Something went wrong during creating the directory {dir_name} : {e}")

    try:
        connection = sqlite3.connect(db_name)
        main_instance.write_log(f"Database connection : {db_name} established")
        return connection
    except Exception as e:
        main_instance.write_log(f"Something went wrong creating the connection with : {db_name}, error message : {e}")

def create_table(cursor: sqlite3.Cursor, table_name: str):
    query = f"""
            CREATE TABLE IF NOT EXISTS {table_name}(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description VARCHAR(1000),
                category VARCHAR(255) NOT NULL,
                price FLOAT NOT NULL,
                date DATE NOT NULL
            )
        """
    try:
        cursor.execute(query)
        main_instance.write_log(f"Table {table_name} created")
    except Exception as e:
        main_instance.write_log(f"Something went wrong during creating the {table_name} table : {e}")

# Only for demonstration purposes, since insert_entry method would miss the newly added column
def add_column(cursor: sqlite3.Cursor, table_name, column_name, column_name_data_type):
    query = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_name_data_type}"

    try:
        cursor.execute(query)
    except Exception as e:
        main_instance.write_log(f"Something went wrong adding a column : {e}")

# Inserting and updating the entries
def insert_entry(cursor: sqlite3.Cursor, table_name, description: str, category: str, price: float, date: str):
    query = f"INSERT INTO {table_name} (description, category, price, date) VALUES (?, ?, ?, ?)"

    try:
        cursor.execute(query, (description, category, price, date))
        main_instance.write_log(f"Entries inserted : {description}, {category}, {price}, {date}")
    except Exception as e:
        main_instance.write_log(f"Something went wrong inserting the entries : {e}")

def update_entry(cursor: sqlite3.Cursor, table_name, column_search, keyword_search, column_update, keyword_update):
    query = f"UPDATE {table_name} SET {column_update} = ? WHERE {column_search} = ?"

    try:
        cursor.execute(query, (keyword_update, keyword_search))
        main_instance.write_log(f"Entry {column_search} : {keyword_search} successfully updated to "
                                f"{column_update} : {keyword_update}")
    except Exception as e:
        main_instance.write_log(f"Something went wrong during updating the entry : {e}")

# Search functions, fetching the rows, showing all
def show_all(cursor: sqlite3.Cursor, table_name):
    query = f"SELECT * FROM {table_name}"

    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        main_instance.write_log(f"Something went wrong showing the database : {e}")

    # Column_s meaning column(s), separate the with comma as in SQL syntax
def search_defined_columns(cursor: sqlite3.Cursor, table_name, column_s_name):
    query = f"SELECT {column_s_name} FROM {table_name}"

    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        for i in range(0, len(rows)):
            print(rows[i])
    except Exception as e:
        main_instance.write_log(f"Something went wrong during showing the selected entries : {e}")

def search(cursor: sqlite3.Cursor, table_name, column, keyword):
    query = f"SELECT * FROM {table_name} WHERE {column} = ?"

    try:
        cursor.execute(query, (keyword,))
        rows = cursor.fetchall()
        for i in range(0, len(rows)):
            print(rows[i])
    except Exception as e:
        main_instance.write_log(f"Something went wrong showing selected items : {e}")

    # Showing based on a condition : id >= 2, or : id > 2 AND id < 5
def search_based_on_condition(cursor: sqlite3.Cursor, table_name, condition):
    query = f"SELECT * FROM {table_name} WHERE {condition}"

    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        main_instance.write_log(f"def search_based_on_condition : Something went wrong during showing based on condition : {e}")

# Ordering the table
def order_by(cursor: sqlite3.Cursor, table_name, column, direction):
    query = f"SELECT * FROM {table_name} ORDER BY {column} {direction}"

    cursor.execute(query)
    rows = cursor.fetchall()

    return rows

def group_by(cursor: sqlite3.Cursor, table_name, function_name, function_argument, show_column, group_by):
    query = f"""
        SELECT {show_column}, {function_name}({function_argument})
        FROM {table_name}
        GROUP BY {group_by}
    """
    cursor.execute(query)
    data = cursor.fetchall()
    for i in range(0, len(data)):
        print(data[i])

# Deleting functions
def delete_entry(cursor: sqlite3.Cursor, table_name, column, keyword):
    query = f"DELETE FROM {table_name} WHERE {column} = ?"

    try:
        cursor.execute(query, (keyword,))
        main_instance.write_log(f"Entry of {column} : {keyword} deleted")
    except Exception as e:
        main_instance.write_log(f"Something went wrong during deleting the entry : {e}")

def delete_table(cursor: sqlite3.Cursor, table_name):
    query = f"DROP TABLE {table_name}"

    try:
        cursor.execute(query)
        main_instance.write_log(f"Table {table_name} was deleted")
    except Exception as e:
        main_instance.write_log(f"Something went wrong deleting the table {table_name} : {e}")