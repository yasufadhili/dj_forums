import requests

def login():
    login_url = "http://localhost:8000/auth/login/" 

    # Create a dictionary with the user's credentials
    login_data = {
        "username": "user1",
        "password": "userpass123"
    }

    # Make a POST request to the login endpoint
    response = requests.post(login_url, data=login_data)

    # Check the response status code
    if response.status_code == 200:
        print("Login successful!")
        token = response.json().get("token")
        print(token)
    else:
        print("Login failed. Check your credentials or the API endpoint.")

def register():
    register_url = "http://localhost:8000/auth/register/" 
    
    registration_data = {
        "username": "new_user",
        "password": "password123", 
        "email": "new_user@example.com",  
    }

    # Make a POST request to the registration endpoint
    response = requests.post(register_url, data=registration_data)
    
    # Check the response status code
    if response.status_code == 201:
        print("Registration successful!")
    else:
        print("Registration failed. Check the API endpoint or data format.")


def user_data():
    
    restricted_data_url = "http://localhost:8000/auth/user/" 

    # Include the token in the request headers
    headers = {
        "Authorization": f"Token {'token'}",  
    }

    # Make a GET request with the token in the headers
    response = requests.get(restricted_data_url, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        data = response.json()  # Access the restricted data in the response
        print("Data retrieved successfully:", data)
    else:
        print("Failed to retrieve data. Check the API endpoint or authentication token.")


