from flask import Flask, request, render_template
import requests
import re

app = Flask(__name__)

# The LIVE Production Webhook URL
N8N_WEBHOOK_URL = "https://n8ntelebot.duckdns.org/webhook/558cba18-bdd2-4d54-ae96-b96bc0014404"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    form_data = {key: value for key, value in request.form.items() if value.strip()}
    
    # Phone Number Validation (Checks if fields with 'Number' have at least 10 digits)
    for key, value in form_data.items():
        if 'Number' in key or 'Phone' in key:
            clean_num = re.sub(r'\D', '', value)
            if len(clean_num) < 10:
                return f"<h1>Error: {key} is invalid. Please enter a valid 10-digit number.</h1><br><a href='javascript:history.back()'>Go back</a>", 400

    try:
        requests.post(N8N_WEBHOOK_URL, json=form_data)
        return "<h1>Success! Your enquiry has been sent.</h1><br><a href='/'>Go back</a>"
    except Exception as e:
        return f"<h1>Error sending to automation.</h1><p>{str(e)}</p>"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
