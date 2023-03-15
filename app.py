from flask import Flask, jsonify, request, send_file
import requests
import json

app = Flask(__name__)

url_prefix = "https://ji9l7maz08.execute-api.us-east-1.amazonaws.com/default/"


@app.route('/warmup', methods=['POST'])
def warmup():
    payload = json.dumps({
        "r": "lambda",
        "s": "lambda"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    final_url = f'{url_prefix}/warmup'
    response = requests.request("POST", final_url, headers=headers, data=payload)

    # Check the response status code
    if response.status_code == 200:
        # Return the JSON response from the external service
        return response.json()
    else:
        # Return the reason for failure
        return jsonify({'reason': response.text or response.reason}), response.status_code


@app.route('/scaled_ready', methods=['GET'])
def scaled_ready():
    headers = {
        'Content-Type': 'application/json'
    }

    final_url = f'{url_prefix}/scaled_ready'
    response = requests.request("GET", final_url, headers=headers)
    # Check the response status code
    if response.status_code == 200:
        # Return the JSON response from the external service
        return response.json()
    else:
        # Return the reason for failure
        return jsonify({'reason': response.text or response.reason}), response.status_code


@app.route('/get_warmup_cost', methods=['GET'])
def get_warmup_cost():
    headers = {
        'Content-Type': 'application/json'
    }

    final_url = f'{url_prefix}/get_warmup_cost'
    response = requests.request("GET", final_url, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        # Return the JSON response from the external service
        return response.json()
    else:
        warmup_details = {
            'lambda': {'time': 0, 'cost': 0},
            'ec2': {'time': 0, 'cost': 0},
            'emr': {'time': 0, 'cost': 0},
            'ecs': {'time': 0, 'cost': 0}
        }
        return jsonify(warmup_details)


# Endpoint to retrieve call strings relevant to directly calling each unique endpoint made available at warmup

@app.route('/get_endpoints', methods=['GET'])
def get_endpoints():
    headers = {
        'Content-Type': 'application/json'
    }

    final_url = f'{url_prefix}/get_endpoints'
    response = requests.request("GET", final_url, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        # Return the JSON response from the external service
        return response.json()
    else:
        # Return the reason for failure
        return jsonify({'reason': response.text or response.reason}), response.status_code


@app.route('/analyze', methods=['POST'])
def analyse():
    payload = request.get_json()

    headers = {
        'Content-Type': 'application/json'
    }

    final_url = f'{url_prefix}/analyze'
    response = requests.request("POST", final_url, headers=headers, data=payload)

    # Check the response status code
    if response.status_code == 200:
        # Return the JSON response from the external service
        return response.json()
    else:
        # Return the reason for failure
        return jsonify({'reason': response.text or response.reason}), response.status_code

# Endpoint to retrieve pairs of 95% and 99% VaR values for each signal

@app.route('/get_sig_vars9599', methods=['GET'])
def get_sig_vars9599():
    headers = {
        'Content-Type': 'application/json'
    }

    final_url = f'{url_prefix}/get_sig_vars9599'
    response = requests.request("GET", final_url, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        # Return the JSON response from the external service
        return response.json()
    else:
        # Return the reason for failure
        return jsonify({'reason': response.text or response.reason}), response.status_code


# Endpoint to retrieve the average risk values over all signals at each of 95% and 99%

@app.route('/get_avg_vars9599', methods=['GET'])
def get_avg_vars9599():
    headers = {
        'Content-Type': 'application/json'
    }

    final_url = f'{url_prefix}/get_avg_vars9599'
    response = requests.request("GET", final_url, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        # Return the JSON response from the external service
        return response.json()
    else:
        # Return the reason for failure
        return jsonify({'reason': response.text or response.reason}), response.status_code


# Endpoint to retrieve profit/loss values for all signals

@app.route('/get_sig_profit_loss', methods=['GET'])
def get_sig_profit_loss():
    headers = {
        'Content-Type': 'application/json'
    }

    final_url = f'{url_prefix}/get_sig_profit_loss'
    response = requests.request("GET", final_url, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        # Return the JSON response from the external service
        return response.json()
    else:
        # Return the reason for failure
        return jsonify({'reason': response.text or response.reason}), response.status_code


# Endpoint to retrieve total resulting profit/loss

@app.route('/get_tot_profit_loss', methods=['GET'])
def get_tot_profit_loss():
    headers = {
        'Content-Type': 'application/json'
    }

    final_url = f'{url_prefix}/get_tot_profit_loss'
    response = requests.request("GET", final_url, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        # Return the JSON response from the external service
        return response.json()
    else:
        # Return the reason for failure
        return jsonify({'reason': response.text or response.reason}), response.status_code


# Endpoint to retrieve the URL for a chart generated using the VaR values

@app.route('/get_chart_url', methods=['GET'])
def get_chart_url():
    headers = {
        'Content-Type': 'application/json'
    }

    final_url = f'{url_prefix}/get_chart_url'
    response = requests.request("GET", final_url, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        # Return the JSON response from the external service
        return response.json()
    else:
        # Return the reason for failure
        return jsonify({'reason': response.text or response.reason}), response.status_code


# Endpoint to retrieve total billable time for the analysis and the cost related to this

@app.route('/get_time_cost', methods=['GET'])
def get_time_cost():
    headers = {
        'Content-Type': 'application/json'
    }

    final_url = f'{url_prefix}/get_time_cost'
    response = requests.request("GET", final_url, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        # Return the JSON response from the external service
        return response.json()
    else:
        # Return the reason for failure
        return jsonify({'reason': response.text or response.reason}), response.status_code


# Endpoint to retrieve information about all previous runs

@app.route('/get_audit', methods=['GET'])
def get_audit():
    headers = {
        'Content-Type': 'application/json'
    }

    final_url = f'{url_prefix}/get_audit'
    response = requests.request("GET", final_url, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        # Return the JSON response from the external service
        return response.json()
    else:
        # Return the reason for failure
        return jsonify({'reason': response.text or response.reason}), response.status_code


# Endpoint to clean up and reset for another analysis
@app.route('/reset', methods=['GET'])
def reset():
    headers = {
        'Content-Type': 'application/json'
    }

    final_url = f'{url_prefix}/reset'
    response = requests.request("GET", final_url, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        # Return the JSON response from the external service
        return response.json()
    else:
        # Return the reason for failure
        return jsonify({'reason': response.text or response.reason}), response.status_code


# Endpoint to terminate and scale-to-zero
@app.route('/terminate', methods=['GET'])
def terminate():
    headers = {
        'Content-Type': 'application/json'
    }

    final_url = f'{url_prefix}/terminate'
    response = requests.request("GET", final_url, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        # Return the JSON response from the external service
        return response.json()
    else:
        # Return the reason for failure
        return jsonify({'reason': response.text or response.reason}), response.status_code


# Endpoint to retrieve confirmation of scale-to-zero
@app.route('/scaled_terminated', methods=['GET'])
def scaled_terminated():
    headers = {
        'Content-Type': 'application/json'
    }

    final_url = f'{url_prefix}/scaled_terminated'
    response = requests.request("GET", final_url, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        # Return the JSON response from the external service
        return response.json()
    else:
        # Return the reason for failure
        return jsonify({'reason': response.text or response.reason}), response.status_code


@app.route('/')
def home():
    return jsonify({'result': 'Ok'})


if __name__ == '__main__':
    app.run(debug=True)
