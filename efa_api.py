import os
import json
import smtplib
from dotenv import load_dotenv, find_dotenv
from email.message import EmailMessage
import numpy as np
from flask import Flask, request

app = Flask(__name__)

@app.route("/getCode", methods=['GET', 'POST'])
def index():
    code = np.random.randint(999999)
    try:
        load_dotenv(find_dotenv())

        EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
        EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

        msg = EmailMessage()
        msg['Subject'] = 'Blue Alert Codigo de Verificacion'
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = request.args.get("email")

        msg.add_alternative(f'<!DOCTYPE html><html><body><h1 style="color:SlateGray;">{code}</h1></body></html>', subtype='html')
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
    except:
        return {
            "error": "invalid email"
        }
    return {
        "authCode": code
    }

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port="8080")