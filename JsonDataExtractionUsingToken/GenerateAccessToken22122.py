import json
import requests
import pyodbc

# Proxy settings
proxy_address = 'http://your_proxy_address:your_proxy_port'
proxy_dict = {
    'http': proxy_address,
    'https': proxy_address
}

clientId = 'dummy_client_id'
clientSecret = 'dummy_client_secret'
scope = 'dummy_scope'
grantType = 'client_credentials'
# Mock token endpoint URL (replace with your mock endpoint URL)
token_endpoint_url = 'https://run.mocky.io/v3/0ae324fa-bbc4-46bc-8496-b6a42a123940'
# Subsequent URL
subsequent_url = 'https://your_subsequent_endpoint_here'

# JSON data to be sent in the POST request
data = {
    'client_id': clientId,
    'client_secret': clientSecret,
    'scope': scope,
    'grant_type': grantType
}
# json_data = json.dumps(data)

# Custom headers
headers = {
    'X-CSRF-Header': 'value',
    'Content-Type': 'application/json'
}

try:
    # Encode the form data
    encoded_data = '&'.join([f"{key}={value}" for key, value in data.items()])
    # Making the POST request with proxy and custom headers
    response = requests.post(token_endpoint_url, data=encoded_data, proxies=proxy_dict, headers=headers)
    # response = requests.post(token_endpoint_url, data=json_data, proxies=proxy_dict, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors

    # Extracting JSON response data
    # json_response = response.json()
    # Extracting access token from the response
    access_token = response.json().get('access_token')

    if access_token:
        # Setting up headers for the subsequent request with Bearer Token
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

        # Data for the subsequent request
        payload = {
            "dataKey": "202403",
            "metricKeys": []
        }

        # Making the subsequent POST request with the generated token
        response = requests.post(subsequent_url, json=payload, proxies=proxy_dict, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Extracting JSON response data from the subsequent request
        json_response = response.json()

        # Process the JSON data as needed
        print(json_response)
    else:
        print("Error: No access token found in the response.")
    # Process the JSON data as needed
    # print(json_response)

except requests.exceptions.RequestException as e:
    print("Error:", e)

# # Provide the path to your JSON file
# file_path = r"C:\Users\abhij\Downloads\testj.json"

# # Open and read the JSON file
# with open(file_path, 'r') as file:
#     data = json.load(file)
data = json_response
def combine_keys(data, prefix=''):
    combined_data = {}
    for key, value in data.items():
        if isinstance(value, dict):
            sub_combined_data = combine_keys(value, prefix=f"{prefix}_{key}" if prefix else key)
            combined_data.update(sub_combined_data)
        else:
            # Replace empty list with NULL
            if isinstance(value, list) and not value:
                value = None
            combined_data[f"{prefix}_{key}" if prefix else key] = value
    return combined_data

# Print combined keys and their values
print("Combined Keys and Values:")
combined_data = combine_keys(data)
for key, value in combined_data.items():
    print(f"{key}: {value}")

# Establish connection to the SQL Server database
server = 'DESKTOP-GR6FEMK\\SQLEXPRESS'
database = 'TE_3E_PROD'
trusted_connection = 'yes'
conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection={trusted_connection};'
conn = pyodbc.connect(conn_str)

# Create a cursor object
cursor = conn.cursor()

# Define table name
table_name = 'YourTableName'

# Check if the table exists, if not, create it
if not cursor.tables(table=table_name).fetchone():
    create_table_query = f"CREATE TABLE {table_name} ({', '.join([f'{column} NVARCHAR(MAX)' for column in combined_data.keys()])})"
    cursor.execute(create_table_query)
    conn.commit()
    print(f"Table '{table_name}' created successfully.")

# Construct insert query
insert_query = f"INSERT INTO {table_name} ({', '.join(combined_data.keys())}) VALUES ({', '.join(['?' for _ in combined_data.keys()])})"

# Extract values from combined_data dictionary
values = list(combined_data.values())

# Execute the insert query
cursor.execute(insert_query, values)
conn.commit()
print("Data inserted successfully.")

# Close connections
cursor.close()
conn.close()
