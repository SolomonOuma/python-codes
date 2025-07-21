import requests

url="https://elearning.zetech.ac.ke/login/index.php"

response=requests.get(url)
headers=response.headers

security_headers=["X-Content-Type-Options","X-Frame-Options","Content-Security-Policy"]

for header in security_headers:
    if header in headers:
        print(f"{header}:{header[header]}")
    else:
        print(f"{header}:Not Found")
        
#this code checks for security headers in the response from the specified URL
#when run, the headers are not found, indicating a potential security risk
