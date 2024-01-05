from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Store visitors in memory
visitors = []

# Endpoint to get the visitor's location based on IP
@app.route('/get_location', methods=['GET'])
def get_location():
    # Get the client's IP address
    ip = request.remote_addr if not app.debug else requests.get('https://api.ipify.org').text

    # Get geospatial location from ip-api.com
    endpoint = f'http://ip-api.com/json/{ip}'
    response = requests.get(endpoint)
    data = response.json()

    # Save data in memory
    visitor_data = {
        'ip_address': ip,
        'country': data['country'],
        'latitude': data['lat'],
        'longitude': data['lon']
    }
    visitors.append(visitor_data)

    return jsonify({'ip': ip, 'country': data['country'], 'latitude': data['lat'], 'longitude': data['lon']}), 200

# Endpoint to get all visitors
@app.route('/get_all_visitors', methods=['GET'])
def get_all_visitors():
    return jsonify(visitors), 200

if __name__ == '__main__':
    app.run(debug=True)
