import requests
#target URLs for login and fee check
login_url="https://portal.zetech.ac.ke/tour.json"
fee_check_url="https://portal.zetech.ac.ke/financials/Financials?isFee=true"
#input your login details here
username="BSE-05-0146/2024"
password="BSE-05-0146/2024"
#this code logs into the web applictation and checks the fee status
session=requests.Session()
login_data={
    "username":username,
    "password":password
}
login_response=session.post(login_url,data=login_data)
if login_response.status_code==200:
    print("Logged in successfully")
else:
    print("Login failed")
    exit()
#check fee status(this might be the API the system uses
fee_response=session.get(fee_check_url)
if fee_response.status_code==200:
    fee_data=fee_response.json()
    print("Fee status:",fee_data.get("fee_status"))
#tamper with the response to check for vulnerabilities
    fee_data["fee_status"]="Paid"
    print("Tampered fee status:",fee_data.get("fee_status"))
else:
    print("Failed to retrieve fee status")
