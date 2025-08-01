from dotenv import load_dotenv
from twilio.rest import Client
import os

load_dotenv()

account_sid = os.getenv("TWILIO_SID")
auth_token = os.getenv("TWILIO_AUTH")
from_whatsapp = os.getenv("TWILIO_FROM")
to_whatsapp = os.getenv("TWILIO_TO")

client = Client(account_sid, auth_token)

def send_message(user_number, msg):
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