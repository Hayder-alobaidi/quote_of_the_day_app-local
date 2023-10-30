from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

quote_service_url = 'http://localhost:5000'  # URL of the Quote Service
analytics_service_url = 'http://localhost:5001'  # URL of the Analytics Service

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/quote', methods=['GET'])
def get_quote():
    # Get a random quote from the Quote Service
    quote_response = requests.get(f"{quote_service_url}/quote")
    if quote_response.status_code == 200:
        quote_data = quote_response.json()
        quote_id = quote_data['id']

        # Get count data for the received quote ID from the Analytics Service
        analytics_response = requests.get(f"{analytics_service_url}/count/{quote_id}")
        if analytics_response.status_code == 200:
            count_data = analytics_response.json()
            current_count = count_data['current_count']
        else:
            current_count = "Unavailable"

        # Combine quote and count data
        combined_data = {
            "id": quote_id,
            "text": quote_data['text'],
            "current_count": current_count
        }
        return jsonify(combined_data)
    else:
        return jsonify({"error": "Quote service is unavailable"}), 503

if __name__ == '__main__':
    app.run(debug=True, port=5002, host='0.0.0.0')
