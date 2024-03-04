# twilio_utils.py
from twilio.rest import Client

def send_sms(recipient_number, message):
    # Your Twilio credentials
    account_sid = 'AC92d60b381a5001f92b074412190efa89'
    auth_token = '335cae33bcbfc947dceec5019608fde4'

    # Initialize Twilio client
    client = Client(account_sid, auth_token)

    try:
        # Send SMS message
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body=message,
            to='whatsapp:+919400453044'
        )
        print("Message sent successfully:", message.sid)
        return True
    except Exception as e:
        print("Failed to send message:", str(e))
        return False
