# twilio_utils.py
from twilio.rest import Client

def send_sms(recipient_number, message):
    # Your Twilio credentials
    account_sid = 'AC92d60b381a5001f92b074412190efa89'
    auth_token = '335cae33bcbfc947dceec5019608fde4'
    twilio_number = '+14155238886'

    # Initialize Twilio client
    client = Client(account_sid, auth_token)

    try:
        # Send SMS message
        message = client.messages.create(
            body=message,
            from_=twilio_number,
            to=recipient_number
        )
        print("Message sent successfully:", message.sid)
        return True
    except Exception as e:
        print("Failed to send message:", str(e))
        return False
