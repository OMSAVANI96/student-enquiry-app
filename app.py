from flask import Flask, request, render_template
import requests

app = Flask(__name__)

# Direct webhook connection
N8N_WEBHOOK_URL = "https://n8ntelebot.duckdns.org/webhook-test/558cba18-bdd2-4d54-ae96-b96bc0014404"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    form_data = {}
    for key, value in request.form.items():
        clean_key = key.replace('_', ' ').replace('-', ' ').title()
        if value.strip():
            form_data[clean_key] = value

    try:
        requests.post(N8N_WEBHOOK_URL, json=form_data)
        return "<h1>Success! Your enquiry has been sent.</h1><br><a href='/'>Go back</a>"
    except Exception as e:
        return f"<h1>Error sending to automation.</h1><p>{str(e)}</p>"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
