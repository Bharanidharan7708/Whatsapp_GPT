import os
from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from openai import OpenAI
import openai

client = OpenAI(
    api_key = "" 
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Reply stating this is a test",
        }
    ],
    model="gpt-4o",
)
gpt_response = chat_completion.choices[0].message.content
print(gpt_response)