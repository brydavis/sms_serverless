import requests
import json 

username = "john@example.com"
password = "aWrds!@12@!34mnop"

class Messenger:

    def __init__(self, URL, username, password):
        # Your API Gateway URL should look like this fake one...
        # "https://daio54iygh.execute-api.ca-central-1.amazonaws.com/api"
        self.URL = URL

        self.username = username
        self.password = password
        self.id_token = ""

    def signup(self):
        r = requests.post(self.URL + "/signup", data = {
            "username": username,
            "password": password,
        })
        print("SIGNUP: ", r.text)

    def confirm(self, code):
        # SIGNUP CONFIRM (via email)
        r = requests.post(self.URL + "/signup/confirm", data = {
            "username": username,
            "code": code,
        })
        print("CONFIRM: ", r.text)

    def login(self):
        # LOGIN
        r = requests.post(self.URL + "/login", data = {
            "username": username,
            "password": password,
        })

        print("LOGIN: ", r.text)
        self.id_token = json.loads(r.text)["id_token"]

    def get_user_info(self):
        # USER RETRIEVE
        r = requests.get(
            self.URL + "/user", 
            headers = {"Authorization": "Bearer " + self.id_token},
        )
        print("USER RETRIEVE: ", r.text)
        return r.text

    def update_user_info(self, data):
        if not data:
            data = {
                "account_sid": "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                "auth_token": "cXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                "phone_number": "+12025551234",
            }

        # USER UPDATE
        r = requests.post(
            self.URL + "/user/update",
            data = data,
            headers = {"Authorization": "Bearer " + self.id_token},
        )
        print("USER UPDATE: ", r.text)

    def get_messages(self):
        # MESSAGES PULL
        r = requests.get(
            self.URL + "/message/pull", 
            headers = {"Authorization": "Bearer " + self.id_token},
        )        
        messages = json.loads(r.text)  
        print(messages)
        return messages

    def send_message(self, to, message):
        # MESSAGES SEND
        # to = input("To: ")
        # message = input("Message: ")

        r = requests.post(
            self.URL + "/message/send", 
            data = {
                "to": to,
                "message": message,    
            },
            headers = {"Authorization": "Bearer " + self.id_token},
        )

        print("MESSAGE SID", r.text)

    def prank(self, to):
        # MESSAGES PRANK
        # to = input("To: ")
        r = requests.post(
            self.URL + "/prank", 
            data = {
                "to": to,
            },
            headers = {"Authorization": "Bearer " + self.id_token},
        )

        print("PRANK", r.text)

    def reuse(self, username, password):
        self.username = username
        self.password = password
        self.id_token = ""

    def cleanup(self):
        self.username = ""
        self.password = ""
        self.id_token = ""


messenger = Messenger(
    # Fake API Gateway URL... please replace
    "https://daio54iygh.execute-api.ca-central-1.amazonaws.com/api",
    
    username, 
    password,
)