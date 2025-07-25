from dotenv import load_dotenv
from twilio.rest import Client
import os

load_dotenv()

account_sid = os.getenv("TWILIO_SID")
auth_token = os.getenv("TWILIO_AUTH")
from_whatsapp = os.getenv("TWILIO_FROM")
to_whatsapp = os.getenv("TWILIO_TO")

client = Client(account_sid, auth_token)

def send_message(msg):
    try:
        message = client.messages.create(
            body=msg,
            from_=from_whatsapp,
            to=to_whatsapp
        )
        print("whatsapp message send:", message.sid)
    except Exception as e:
        print("faild to send whatsapp message")
        print("Failed to send WhatsApp message:", str(e))

# import requests

# url = "https://graph.facebook.com/v19.0//messages"
# token = "EAAtuyIF2SlgBPHJqEverqRuzVH4qSGXPs0X0DBMjSjBuWtTLjwKNZBI6FwHZC8jUtXfFanl5SJXzRt0ZC5d4XmNZCeDwDIymCiDgohnH8yW5YTWdj2IrnXSYNTq9ObiT2q14KzuZCMPf4J87rAZBeGz9QRYEP17yqSLzKX8DGXbTrnL1qyHK0O6dtENR9r3kZC6mS9EZBiUMTTVy773np1AFA4AwssOW4kfLQjXs48JWGI4AnQZDZD"
# headers = {
#     "Authorization": f"Bearer {token}",
#     "Content-Type": "application/json"
# }

# data = {
#     "messaging_product": "whatsapp",
#     "to": "+918320452875",  # Include country code
#     "type": "text",
#     "text": {
#         "body": "Hello from WhatsApp Cloud API!"
#     }
# }

# response = requests.post(url, headers=headers, json=data)
# print(response.status_code)
# print(response.json())
