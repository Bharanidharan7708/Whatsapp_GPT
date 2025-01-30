import os
from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from openai import OpenAI
import openai

# Initialize Flask app
app = Flask(__name__)

# Twilio credentials (set these as environment variables in Heroku)
account_sid = ''
auth_token = ""
twilio_number = 'whatsapp:+14155238886'  # Twilio's WhatsApp Sandbox Number

# OpenAI API Key (set as environment variable in Heroku)
openai.api_key = ""

# Twilio client
client = Client(account_sid, auth_token)


# Allowed numbers
allowed_numbers = ['+', '+']

# Function to generate GPT response
def generate_gpt_response(user_message):
    try:
        client = OpenAI(
            api_key=""
        )

        chat_completion = client.chat.completions.create(
            messages=[{"role": "system", "content": 'You are a helpful AI assistant that helps with any questions or tasks. Your name is alex'},
                      {"role": "user", "content": user_message}],
            max_tokens=200,
            model="gpt-3.5-turbo",
        )
        gpt_response = chat_completion.choices[0].message.content

        return gpt_response 

    except Exception as e:
        return f"Error generating response: {str(e)}"

# Webhook to handle incoming messages
@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    sender = request.form.get("From")
    message_body = request.form.get("Body")

    if sender in [f"whatsapp:{num}" for num in allowed_numbers]:
        # Generate GPT response
        gpt_response = generate_gpt_response(message_body)

        # Send GPT response via Twilio API
        client.messages.create(
            body=gpt_response,
            from_=twilio_number,
            to=sender
        )

        return '', 200  # Return empty response after sending the message
    else:
        # Unauthorized number
        resp = MessagingResponse()
        resp.message("Sorry, you are not authorized to send messages.")
        return str(resp)
    
@app.route('/status', methods=['POST'])
def status_callback():
    message_sid = request.values.get('MessageSid')
    message_status = request.values.get('MessageStatus')
    print(f"Message SID: {message_sid}, Status: {message_status}")
    return "Status received", 200


# Test endpoint
@app.route("/")
def home():
    return "GPT WhatsApp Reply Bot is running!"

# Run Flask app
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
