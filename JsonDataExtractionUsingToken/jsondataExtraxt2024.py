import pyodbc
import json

def insert_database_table(data, cursor, table_name, table_columns):
    try:
        # Insert data into the table only if the row values do not exist
        for obj in data:
            combined_data = combine_keys(obj)
            valid_keys = [key for key in combined_data.keys() if key in table_columns]
            if valid_keys:
                insert_query = f"INSERT INTO {table_name} ({', '.join(valid_keys)}) VALUES ({', '.join(['?' for _ in valid_keys])})"
                values = [combined_data[key] for key in valid_keys]
                try:
                    cursor.execute(insert_query, values)
                    print("Data inserted successfully.")
                except pyodbc.IntegrityError as ie:
                    print("Skipping insertion due to duplicate key error:", ie)
                    continue

    except pyodbc.Error as e:
        print("Error:", e)


def create_database_table(data, cursor, table_name):
    try:
        # Get combined keys and values for the first object in data
        combined_data = combine_keys(data[0])

        # Check if client_artifactID and workspace_artifactID are present in the combined_data
        if 'client_artifactID' not in combined_data or 'workspace_artifactID' not in combined_data:
            print("client_artifactID and/or workspace_artifactID not found in the data.")
            return

        # Define columns
        columns = [
            "client_artifactID NVARCHAR(255) NOT NULL",
            "workspace_artifactID NVARCHAR(255) NOT NULL"
        ]

        # Add other columns
        for column_name in combined_data.keys():
            if column_name not in ['client_artifactID', 'workspace_artifactID']:
                columns.append(f"{column_name} NVARCHAR(MAX)")

        # Define primary key constraint
        primary_key_constraint = ", PRIMARY KEY (client_artifactID, workspace_artifactID)"

        # Create table query
        create_table_query = f"CREATE TABLE {table_name} ({', '.join(columns)}{primary_key_constraint})"
        cursor.execute(create_table_query)
        print(f"Table '{table_name}' created successfully.")

    except pyodbc.Error as e:
        print("Error:", e)

def combine_keys(data, prefix=''):
    combined_data = {}
    for key, value in data.items():
        # Sanitize key to make it a valid column name
        sanitized_key = key.replace(' ', '_').replace('-', '_').replace('.', '_')
        if isinstance(value, dict):
            sub_combined_data = combine_keys(value, prefix=f"{prefix}_{sanitized_key}" if prefix else sanitized_key)
            combined_data.update(sub_combined_data)
        else:
            # Replace empty list with NULL
            if isinstance(value, list) and not value:
                value = None
            combined_data[f"{prefix}_{sanitized_key}" if prefix else sanitized_key] = value
    return combined_data

def main():
    # Database connection details
    server = 'DESKTOP-GR6FEMK\\SQLEXPRESS'
    database = 'TE_3E_PROD'
    trusted_connection = 'yes'
    conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection={trusted_connection};'

    # Table details
    table_name = 'YourTableName'

    try:
        # Establish connection to the SQL Server database
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()

            # Provide the path to your JSON file
            file_path = r"C:\Users\abhij\Downloads\sample.json"

            # Open and read the JSON file
            with open(file_path, 'r') as file:
                data = json.load(file)
                
            # Filter out the "results" array
            filtered_data = data["results"]

            # Check if the table exists, if not, create it
            if not cursor.tables(table=table_name).fetchone():
                create_database_table(filtered_data, cursor, table_name)
            else:
                print(f"Table '{table_name}' already exists.")

            # Fetch table columns from the database
            table_columns = [column.column_name for column in cursor.columns(table=table_name)]

            # Insert data into the table
            insert_database_table(filtered_data, cursor, table_name, table_columns)

    except pyodbc.Error as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
