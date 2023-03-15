#!/usr/bin/env python3
"""
AWS Lambda API Gateway with Postman Integration
Enhanced Flask application for AWS Lambda API management and financial analysis
"""

from flask import Flask, jsonify, request, send_file
import requests
import json
import logging
import os
from datetime import datetime
import time
from functools import wraps

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration
AWS_API_URL = "https://ji9l7maz08.execute-api.us-east-1.amazonaws.com/default/"
API_VERSION = "1.0.0"

# Request tracking
request_log = []

def log_request(f):
    """Decorator to log API requests"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        response = f(*args, **kwargs)
        end_time = time.time()
        
        request_data = {
            'endpoint': request.endpoint,
            'method': request.method,
            'timestamp': datetime.now().isoformat(),
            'response_time': end_time - start_time,
            'status_code': response[1] if isinstance(response, tuple) else 200
        }
        request_log.append(request_data)
        
        logger.info(f"API Request: {request.method} {request.endpoint} - {request_data['status_code']} - {request_data['response_time']:.3f}s")
        return response
    return decorated_function

def make_aws_request(endpoint, method='GET', payload=None):
    """Make request to AWS Lambda API"""
    try:
        headers = {'Content-Type': 'application/json'}
        url = f"{AWS_API_URL}{endpoint}"
        
        if method == 'POST' and payload:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
        else:
            response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            return response.json(), 200
        else:
            logger.error(f"AWS API Error: {response.status_code} - {response.text}")
            return {'error': response.text or response.reason}, response.status_code
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {str(e)}")
        return {'error': f'Request failed: {str(e)}'}, 500

@app.route('/')
def home():
    """Home endpoint with API information"""
    return jsonify({
        'message': 'AWS Lambda API Gateway',
        'version': API_VERSION,
        'status': 'running',
        'endpoints': [
            '/warmup - POST - Warm up Lambda functions',
            '/scaled_ready - GET - Check if scaled and ready',
            '/analyze - POST - Analyze financial data',
            '/get_warmup_cost - GET - Get warmup costs',
            '/get_endpoints - GET - Get available endpoints',
            '/get_sig_vars9599 - GET - Get VaR values for signals',
            '/get_avg_vars9599 - GET - Get average VaR values',
            '/get_sig_profit_loss - GET - Get profit/loss for signals',
            '/get_tot_profit_loss - GET - Get total profit/loss',
            '/get_chart_url - GET - Get chart URL',
            '/get_time_cost - GET - Get time and cost analysis',
            '/get_audit - GET - Get audit information',
            '/reset - GET - Reset analysis',
            '/terminate - GET - Terminate services',
            '/scaled_terminated - GET - Check if scaled to zero',
            '/health - GET - Health check',
            '/metrics - GET - API metrics'
        ]
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': API_VERSION
    })

@app.route('/metrics')
def get_metrics():
    """Get API metrics"""
    if not request_log:
        return jsonify({'message': 'No metrics available yet'})
    
    total_requests = len(request_log)
    avg_response_time = sum(r['response_time'] for r in request_log) / total_requests
    status_codes = {}
    
    for request in request_log:
        status = request['status_code']
        status_codes[status] = status_codes.get(status, 0) + 1
    
    return jsonify({
        'total_requests': total_requests,
        'average_response_time': round(avg_response_time, 3),
        'status_codes': status_codes,
        'last_10_requests': request_log[-10:] if len(request_log) >= 10 else request_log
    })

@app.route('/warmup', methods=['POST'])
@log_request
def warmup():
    """Warm up Lambda functions"""
    payload = {
        "r": "lambda",
        "s": "lambda"
    }
    
    return make_aws_request('warmup', method='POST', payload=payload)

@app.route('/scaled_ready', methods=['GET'])
@log_request
def scaled_ready():
    """Check if services are scaled and ready"""
    return make_aws_request('scaled_ready')

@app.route('/get_warmup_cost', methods=['GET'])
@log_request
def get_warmup_cost():
    """Get warmup costs for different services"""
    result, status_code = make_aws_request('get_warmup_cost')
    
    if status_code != 200:
        # Return default warmup costs
        return jsonify({
            'lambda': {'time': 0, 'cost': 0},
            'ec2': {'time': 0, 'cost': 0},
            'emr': {'time': 0, 'cost': 0},
            'ecs': {'time': 0, 'cost': 0}
        })
    
    return jsonify(result)

@app.route('/get_endpoints', methods=['GET'])
@log_request
def get_endpoints():
    """Get available endpoints for direct calling"""
    return make_aws_request('get_endpoints')

@app.route('/analyze', methods=['POST'])
@log_request
def analyze():
    """Analyze financial data"""
    payload = request.get_json()
    
    if not payload:
        return jsonify({'error': 'No payload provided'}), 400
    
    return make_aws_request('analyze', method='POST', payload=payload)

@app.route('/get_sig_vars9599', methods=['GET'])
@log_request
def get_sig_vars9599():
    """Get VaR values for signals"""
    return make_aws_request('get_sig_vars9599')

@app.route('/get_avg_vars9599', methods=['GET'])
@log_request
def get_avg_vars9599():
    """Get average VaR values"""
    return make_aws_request('get_avg_vars9599')

@app.route('/get_sig_profit_loss', methods=['GET'])
@log_request
def get_sig_profit_loss():
    """Get profit/loss values for signals"""
    return make_aws_request('get_sig_profit_loss')

@app.route('/get_tot_profit_loss', methods=['GET'])
@log_request
def get_tot_profit_loss():
    """Get total profit/loss"""
    return make_aws_request('get_tot_profit_loss')

@app.route('/get_chart_url', methods=['GET'])
@log_request
def get_chart_url():
    """Get chart URL for VaR visualization"""
    return make_aws_request('get_chart_url')

@app.route('/get_time_cost', methods=['GET'])
@log_request
def get_time_cost():
    """Get time and cost analysis"""
    return make_aws_request('get_time_cost')

@app.route('/get_audit', methods=['GET'])
@log_request
def get_audit():
    """Get audit information"""
    return make_aws_request('get_audit')

@app.route('/reset', methods=['GET'])
@log_request
def reset():
    """Reset analysis for another run"""
    return make_aws_request('reset')

@app.route('/terminate', methods=['GET'])
@log_request
def terminate():
    """Terminate and scale-to-zero"""
    return make_aws_request('terminate')

@app.route('/scaled_terminated', methods=['GET'])
@log_request
def scaled_terminated():
    """Check if scaled to zero"""
    return make_aws_request('scaled_terminated')

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {str(e)}")
    return jsonify({'error': 'An unexpected error occurred'}), 500

class FinancialAnalyzer:
    """Enhanced financial analysis class"""
    
    def __init__(self):
        self.analysis_results = {}
    
    def analyze_portfolio(self, data):
        """Analyze portfolio data"""
        try:
            # This would contain the actual financial analysis logic
            # For now, return a sample analysis
            return {
                'status': 'success',
                'analysis_type': 'portfolio',
                'timestamp': datetime.now().isoformat(),
                'risk_metrics': {
                    'var_95': 0.02,
                    'var_99': 0.03,
                    'sharpe_ratio': 1.2
                },
                'performance_metrics': {
                    'total_return': 0.15,
                    'volatility': 0.12,
                    'max_drawdown': -0.08
                }
            }
        except Exception as e:
            logger.error(f"Portfolio analysis failed: {str(e)}")
            return {'error': f'Analysis failed: {str(e)}'}
    
    def calculate_var(self, returns, confidence_level=0.95):
        """Calculate Value at Risk"""
        try:
            import numpy as np
            var = np.percentile(returns, (1 - confidence_level) * 100)
            return abs(var)
        except Exception as e:
            logger.error(f"VaR calculation failed: {str(e)}")
            return None
    
    def generate_report(self, analysis_data):
        """Generate analysis report"""
        return {
            'report_id': f"RPT_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'generated_at': datetime.now().isoformat(),
            'summary': analysis_data,
            'recommendations': [
                'Diversify portfolio to reduce risk',
                'Consider hedging strategies',
                'Monitor volatility closely'
            ]
        }

# Initialize financial analyzer
financial_analyzer = FinancialAnalyzer()

@app.route('/analyze_portfolio', methods=['POST'])
@log_request
def analyze_portfolio():
    """Enhanced portfolio analysis endpoint"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Perform analysis
        analysis_result = financial_analyzer.analyze_portfolio(data)
        
        # Generate report
        report = financial_analyzer.generate_report(analysis_result)
        
        return jsonify({
            'status': 'success',
            'analysis': analysis_result,
            'report': report
        })
        
    except Exception as e:
        logger.error(f"Portfolio analysis failed: {str(e)}")
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/get_analysis_status', methods=['GET'])
@log_request
def get_analysis_status():
    """Get current analysis status"""
    return jsonify({
        'status': 'ready',
        'last_analysis': datetime.now().isoformat(),
        'available_analyses': [
            'portfolio_analysis',
            'risk_assessment',
            'performance_metrics',
            'var_calculation'
        ]
    })

if __name__ == '__main__':
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))
    
    logger.info(f"Starting AWS Lambda API Gateway on port {port}")
    logger.info(f"API Version: {API_VERSION}")
    
    app.run(host='0.0.0.0', port=port, debug=False) 