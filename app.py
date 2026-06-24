from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Paste your actual keys inside the quotes below!
TELEGRAM_BOT_TOKEN = "8927887360:AAF4ZKovuyQ-ePgIJGfVQeXS49G_JpoDZ-s"
TELEGRAM_CHAT_ID = "7184813258"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Pull the exact fields from your frontend form
    data = request.form
    name = data.get('student_name', 'N/A')
    whatsapp = data.get('whatsapp_number', 'N/A')
    branch = data.get('branch', 'N/A')
    course = data.get('course', 'N/A')
    timeline = data.get('timeline', 'N/A')
    
    # Format the Telegram message exactly how you want to read it
    message = (
        f"📢 *New Student Enquiry!*\n\n"
        f"👤 *Name:* {name}\n"
        f"📱 *WhatsApp:* {whatsapp}\n"
        f"📍 *Branch:* {branch}\n"
        f"📚 *Course:* {course}\n"
        f"⏱ *Timeline:* {timeline}"
    )
    
    # Fire the message to the Telegram API
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            # We can easily redirect this to a "Thank You" page later
            return "<h2>Success! Your enquiry has been sent.</h2><br><a href='/'>Go back</a>"
        else:
            return f"Telegram Error: {response.text}"
    except Exception as e:
        return f"Server Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
