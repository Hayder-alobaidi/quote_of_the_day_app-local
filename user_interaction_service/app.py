from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

quote_service_url = 'http://localhost:5000'  # URL of the Quote Service
analytics_service_url = 'http://localhost:5001'  # URL of the Analytics Service

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/quote', methods=['GET'])
def get_quote():
    # Get a random quote from the Quote Service
    quote_response = requests.get(f"{quote_service_url}/quote")
    if quote_response.status_code != 200:
        return jsonify({"error": "Quote service is unavailable"}), 503

    quote_data = quote_response.json()
    quote_id = quote_data['id']

    # Initialize the default quote data
    combined_data = {
        "id": quote_id,
        "text": quote_data['text'],
        "current_count": "Unavailable"
    }

    # Attempt to get count data for the received quote ID from the Analytics Service
    try:
        analytics_response = requests.get(f"{analytics_service_url}/count/{quote_id}")
        if analytics_response.status_code == 200:
            count_data = analytics_response.json()
            combined_data["current_count"] = count_data['current_count']
    except requests.exceptions.RequestException:
        # Log this error in real scenario
        pass

    return jsonify(combined_data)

if __name__ == '__main__':
    app.run(debug=True, port=5002, host='0.0.0.0')
