import requests

# Target URLs (replace with the actual endpoints)
login_url = "https://portal.zetech.ac.ke/api/login"  # Example, update this
fee_check_url = "https://portal.zetech.ac.ke/financials/Financials?isFee=true"

# Credentials (use environment variables or input for security)
username = "BSE-05-0146/2024"
password = "BSE-05-0146/2024"

# Initialize session
session = requests.Session()

# Add headers if required (e.g., for JSON payloads)
headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}

# Login data
login_data = {
    "username": username,
    "password": password
}

try:
    # Send login request
    login_response = session.post(login_url, json=login_data, headers=headers)
    
    # Check if login was successful (status code and response content)
    if login_response.status_code == 200:
        print("Logged in successfully")
        print("Response:", login_response.json())  # Debug response
    else:
        print(f"Login failed with status code: {login_response.status_code}")
        print("Response:", login_response.text)  # Debug error
        exit()

    # Check fee status
    fee_response = session.get(fee_check_url)
    if fee_response.status_code == 200:
        fee_data = fee_response.json()
        print("Original fee status:", fee_data.get("fee_status"))

        # Tamper with the response (for testing only)
        fee_data["fee_status"] = "Paid"
        print("Tampered fee status:", fee_data.get("fee_status"))
    else:
        print(f"Failed to retrieve fee status. Status code: {fee_response.status_code}")
        print("Response:", fee_response.text)  # Debug error

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
