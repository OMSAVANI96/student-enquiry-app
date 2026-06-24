from flask import Flask, request, render_template
import requests
import os

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    message = "📢 *New Student Enquiry!*\n\n"
    
    for key, value in request.form.items():
        clean_key = key.replace('_', ' ').replace('-', ' ').title()
        if value.strip(): 
            message += f"*{clean_key}:* {value}\n"

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        requests.post(url, json=payload)
        return "<h1>Success! Your enquiry has been sent.</h1><br><a href='/'>Go back</a>"
    except Exception as e:
        return f"<h1>Error sending message.</h1><p>{str(e)}</p>"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
