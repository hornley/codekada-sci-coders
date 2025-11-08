from flask import Flask, render_template, request, jsonify, redirect, url_for
import os

app = Flask(__name__)

# Configure static and template folders
app.static_folder = 'static'
app.template_folder = 'templates'

@app.route('/')
def index():
    """Main landing page"""
    return render_template('landing.html')

@app.route('/setup')
def user_setup():
    """User setup/registration page"""
    return render_template('user-setup.html')

@app.route('/dashboard')
def dashboard():
    """User dashboard"""
    return render_template('dashboard.html')

@app.route('/analyzer')
def product_analyzer():
    """Product analyzer page"""
    return render_template('product-analyzer.html')

@app.route('/scanner')
def product_scanner():
    """Product scanner page"""
    category = request.args.get('category', 'food')
    return render_template('product-scanner.html', category=category)

# API Routes for future backend integration
@app.route('/api/analyze', methods=['POST'])
def analyze_product():
    """API endpoint for product analysis"""
    data = request.get_json()
    
    # Placeholder for analysis logic
    # Here you would integrate your AI/ML models
    
    return jsonify({
        'status': 'success',
        'message': 'Analysis complete',
        'data': {
            'product_name': data.get('name', ''),
            'analysis_result': 'This is a placeholder result. Integrate your analysis logic here.',
            'safety_score': 85,
            'recommendations': [
                'This product appears to be safe for consumption',
                'Check for any personal allergens',
                'Consider dietary preferences'
            ]
        }
    })

@app.route('/api/search', methods=['GET'])
def search_products():
    """API endpoint for product search"""
    query = request.args.get('q', '')
    
    # Placeholder for database search
    # Here you would query your product database
    
    return jsonify({
        'status': 'success',
        'query': query,
        'results': [
            {
                'id': 1,
                'name': f'Sample Product matching "{query}"',
                'brand': 'Sample Brand',
                'category': 'food'
            }
        ]
    })

@app.route('/api/upload-image', methods=['POST'])
def upload_image():
    """API endpoint for image upload and barcode scanning"""
    if 'image' not in request.files:
        return jsonify({'status': 'error', 'message': 'No image uploaded'})
    
    image = request.files['image']
    
    # Placeholder for image processing
    # Here you would integrate barcode scanning and OCR
    
    return jsonify({
        'status': 'success',
        'message': 'Image processed successfully',
        'barcode': '1234567890123',
        'product_found': True
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)