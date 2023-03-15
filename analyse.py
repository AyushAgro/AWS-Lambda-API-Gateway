# API endpoint: https://ji9l7maz08.execute-api.us-east-1.amazonaws.com/default/analyze

import boto3
import json
import random
from datetime import datetime

# Initialize AWS services
s3 = boto3.client('s3', region_name='us-east-1')

# Bucket name and keys
BUCKET_NAME = 'stockprice9871'
DATA_KEY = 'data.json'
WHITE_SOLDIERS_KEY = 'white_soldiers_chart.png'
BLACK_CROWS_KEY = 'black_crows_chart.png'
ANALYSIS_RESULTS_KEY = 'analysis_results.json'


# Fetch data from JSON file in S3
def fetch_data():
    response = s3.get_object(Bucket=BUCKET_NAME, Key=DATA_KEY)
    raw_data = json.loads(response['Body'].read().decode('utf-8'))

    data = []
    for timestamp in raw_data['Open']:
        data.append({
            'Date': datetime.utcfromtimestamp(int(timestamp) / 1000),
            'Open': raw_data['Open'][timestamp],
            'High': raw_data['High'][timestamp],
            'Low': raw_data['Low'][timestamp],
            'Close': raw_data['Close'][timestamp],
            'Adj Close': raw_data['Adj Close'][timestamp],
            'Volume': raw_data['Volume'][timestamp]
        })

    return data


# Function to generate candlestick chart for Three White Soldiers
def generate_white_soldiers_chart(data):
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    # Select relevant data
    selected_data = data[-9:]

    fig, ax = plt.subplots()
    candlestick_ohlc(ax, selected_data)
    ax.set_title('Three White Soldiers')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()

    # Save to file
    fig.savefig('/tmp/white_soldiers_chart.png')
    plt.close(fig)

    # Upload to S3
    s3.upload_file('/tmp/white_soldiers_chart.png', BUCKET_NAME, WHITE_SOLDIERS_KEY)


# Function to generate candlestick chart for Three Black Crows
def generate_black_crows_chart(data):
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    # Select relevant data
    selected_data = data[-9:]

    fig, ax = plt.subplots()
    candlestick_ohlc(ax, selected_data)
    ax.set_title('Three Black Crows')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()

    # Save to file
    fig.savefig('/tmp/black_crows_chart.png')
    plt.close(fig)

    # Upload to S3
    s3.upload_file('/tmp/black_crows_chart.png', BUCKET_NAME, BLACK_CROWS_KEY)


# Helper function to plot candlestick chart
def candlestick_ohlc(ax, data):
    import matplotlib.dates as mdates
    ax.xaxis_date()
    ax.grid(True)

    for entry in data:
        date_num = mdates.date2num(entry['Date'])
        color = 'green' if entry['Close'] >= entry['Open'] else 'red'
        ax.plot([date_num, date_num], [entry['Low'], entry['High']], color=color)
        ax.plot([date_num, date_num - 0.2], [entry['Open'], entry['Open']], color=color)
        ax.plot([date_num, date_num + 0.2], [entry['Close'], entry['Close']], color=color)


# Run analysis
def run_analysis(h, d, t, p):
    data = fetch_data()
    min_history = h
    shots = d
    signals = []

    for i in range(2, len(data)):
        body = 0.01
        if t == 'sell':
            if (data[i]['Open'] - data[i]['Close']) >= body \
                    and data[i]['Close'] < data[i - 1]['Close'] \
                    and (data[i - 1]['Open'] - data[i - 1]['Close']) >= body \
                    and data[i - 1]['Close'] < data[i - 2]['Close'] \
                    and (data[i - 2]['Open'] - data[i - 2]['Close']) >= body:
                signals.append(i)
        elif t == 'buy':
            if (data[i]['Close'] - data[i]['Open']) >= body \
                    and data[i]['Close'] > data[i - 1]['Close'] \
                    and (data[i - 1]['Close'] - data[i - 1]['Open']) >= body \
                    and data[i - 1]['Close'] > data[i - 2]['Close'] \
                    and (data[i - 2]['Close'] - data[i - 2]['Open']) >= body:
                signals.append(i)

    simulated_var95 = []
    simulated_var99 = []
    for signal in signals:
        if signal >= min_history:
            mean = sum([data[j]['Close'] / data[j - 1]['Close'] - 1 for j in
                        range(signal - min_history + 1, signal + 1)]) / min_history
            std = (sum([(data[j]['Close'] / data[j - 1]['Close'] - 1 - mean) ** 2 for j in
                        range(signal - min_history + 1, signal + 1)]) / (min_history - 1)) ** 0.5
            simulated = [random.gauss(mean, std) for _ in range(shots)]
            simulated.sort(reverse=True)
            var95 = simulated[int(len(simulated) * 0.95)]
            var99 = simulated[int(len(simulated) * 0.99)]
            simulated_var95.append(var95)
            simulated_var99.append(var99)

    profit_loss = []
    for signal in signals:
        if signal + p < len(data):
            if t == 'sell':
                profit = data[signal + p]['Close'] - data[signal]['Close']
                profit_loss.append(profit)
            elif t == 'buy':
                profit = data[signal]['Close'] - data[signal + p]['Close']
                profit_loss.append(profit)

    total_profit_loss = sum(profit_loss)
    # generate_white_soldiers_chart(data)
    # generate_black_crows_chart(data)
    chart_url = {'WHITE_SOLDIERS': 'https://stockprice9871.s3.amazonaws.com/white_soldiers_chart.png',
                 'BLACK_SOLDIERS': 'https://stockprice9871.s3.amazonaws.com/black_crows_chart.png'}
    timestamp = datetime.utcnow().isoformat()

    analysis_result = {
        'timestamp': timestamp,
        'parameters': {
            'h': h,
            'd': d,
            't': t,
            'p': p
        },
        'results': {
            'var95': simulated_var95,
            'var99': simulated_var99,
            'profit_loss': profit_loss,
            'total_profit_loss': total_profit_loss,
            'chart_url': chart_url
        }
    }

    # Fetch existing analysis results
    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=ANALYSIS_RESULTS_KEY)
        analysis_history = json.loads(response['Body'].read().decode('utf-8'))
    except s3.exceptions.NoSuchKey:
        analysis_history = {}

    # Append new analysis result
    analysis_history[timestamp] = analysis_result

    # Save analysis results to S3
    s3.put_object(Bucket=BUCKET_NAME, Key=ANALYSIS_RESULTS_KEY, Body=json.dumps(analysis_history))

"""

  "h": 104,
  "d": 987,
  "t": "sell",
  "p": 12"
  """

def lambda_handler(event, context):
    h = event.get('h', 104)
    d = event.get('d', 987)
    t = event.get('t', 'sell')
    p = event.get('p', 12)

    run_analysis(h, d, t, p)
    return {
        'statusCode': 200,
        'body': json.dumps({'result': 'ok'})
    }
