"""
Flask Backend Server - Ingredient Intelligence Analyzer
Simple Flask integration example using the unified app.py
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import tempfile
from werkzeug.utils import secure_filename
from datetime import datetime

from app import IngredientAnalysisService

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Initialize service
service = IngredientAnalysisService()

# Configuration
UPLOAD_FOLDER = 'temp_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Create upload folder
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ==================== HEALTH CHECK ====================

@app.route('/', methods=['GET'])
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify(service.health_check())


# ==================== ANALYSIS ENDPOINTS ====================

@app.route('/api/analyze/image', methods=['POST'])
def analyze_image():
    """
    Analyze product from uploaded image.
    
    Form data:
        - image: file (required)
        - user_id: string (optional)
        - user_profile: JSON string (optional)
    """
    # Check if file uploaded
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        temp_filename = f"{timestamp}_{filename}"
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], temp_filename)
        file.save(temp_path)
        
        # Get user profile if provided
        user_profile = None
        if 'user_profile' in request.form:
            import json
            user_profile = json.loads(request.form['user_profile'])
        elif 'user_id' in request.form:
            user_id = request.form['user_id']
            user_profile = service.get_user_preferences(user_id)
        
        # Analyze
        result = service.analyze_image(temp_path, user_profile)
        
        # Cleanup temp file
        os.remove(temp_path)
        
        return jsonify(result), 200
    
    except Exception as e:
        # Cleanup on error
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return jsonify({'error': str(e)}), 500


@app.route('/api/analyze/text', methods=['POST'])
def analyze_text():
    """
    Analyze product from ingredients text.
    
    JSON body:
        - ingredients_text: string (required)
        - product_type: string (optional)
        - user_profile: object (optional)
    """
    data = request.get_json()
    
    if not data or 'ingredients_text' not in data:
        return jsonify({'error': 'ingredients_text is required'}), 400
    
    try:
        result = service.analyze_text(
            ingredients_text=data['ingredients_text'],
            product_type=data.get('product_type'),
            user_profile=data.get('user_profile'),
            expiration_date=data.get('expiration_date')
        )
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/extract/ingredients', methods=['POST'])
def extract_ingredients():
    """Extract ingredients text only (OCR without analysis)."""
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file'}), 400
    
    try:
        # Save temp file
        filename = secure_filename(file.filename)
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], f"temp_{filename}")
        file.save(temp_path)
        
        # Extract
        result = service.extract_ingredients_only(temp_path)
        
        # Cleanup
        os.remove(temp_path)
        
        return jsonify(result), 200
    
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return jsonify({'error': str(e)}), 500


# ==================== USER PROFILE ENDPOINTS ====================

@app.route('/api/user/register', methods=['POST'])
def register_user():
    """Create new user profile."""
    data = request.get_json()
    
    try:
        result = service.create_user_profile(data)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/user/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get user profile."""
    try:
        profile = service.get_user_profile(user_id)
        if profile:
            return jsonify(profile), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user profile."""
    data = request.get_json()
    
    try:
        result = service.update_user_profile(user_id, data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/user/<user_id>/preferences', methods=['GET'])
def get_preferences(user_id):
    """Get user health preferences."""
    try:
        prefs = service.get_user_preferences(user_id)
        if prefs:
            return jsonify({'preferences': prefs}), 200
        else:
            return jsonify({'preferences': None}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/user/<user_id>/preferences', methods=['POST'])
def save_preferences(user_id):
    """Save user health preferences."""
    data = request.get_json()
    
    try:
        result = service.save_user_preferences(user_id, data)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== INTAKE TRACKING ENDPOINTS ====================

@app.route('/api/intake/log', methods=['POST'])
def log_intake():
    """
    Log consumed product.
    
    JSON body:
        - user_id: string (required)
        - analysis_result: object (required)
        - timestamp: string (optional, ISO format)
    """
    data = request.get_json()
    
    if not data or 'user_id' not in data or 'analysis_result' not in data:
        return jsonify({'error': 'user_id and analysis_result are required'}), 400
    
    try:
        result = service.log_intake(
            user_id=data['user_id'],
            analysis_result=data['analysis_result'],
            timestamp=data.get('timestamp')
        )
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/intake/daily/<user_id>', methods=['GET'])
def get_daily_summary(user_id):
    """Get daily intake summary."""
    date = request.args.get('date')  # Optional YYYY-MM-DD
    
    try:
        summary = service.get_daily_summary(user_id, date)
        return jsonify(summary), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/intake/weekly/<user_id>', methods=['GET'])
def get_weekly_report(user_id):
    """Get weekly intake report."""
    end_date = request.args.get('end_date')  # Optional YYYY-MM-DD
    
    try:
        report = service.get_weekly_report(user_id, end_date)
        return jsonify(report), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/intake/history/<user_id>', methods=['GET'])
def get_history(user_id):
    """Get intake history."""
    limit = request.args.get('limit', 20, type=int)
    
    try:
        history = service.get_intake_history(user_id, limit)
        return jsonify(history), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/intake/check/<user_id>/<product_name>', methods=['GET'])
def check_history(user_id, product_name):
    """Check if product consumed before."""
    try:
        result = service.check_product_history(user_id, product_name)
        if result:
            return jsonify(result), 200
        else:
            return jsonify({'found': False}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/intake/<user_id>/<int:entry_id>', methods=['DELETE'])
def delete_entry(user_id, entry_id):
    """Delete intake entry."""
    try:
        result = service.delete_intake_entry(user_id, entry_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== BATCH OPERATIONS ====================

@app.route('/api/analyze/batch', methods=['POST'])
def analyze_batch():
    """
    Analyze multiple products in batch.
    
    JSON body:
        - items: array of objects (required)
        - user_profile: object (optional)
    """
    data = request.get_json()
    
    if not data or 'items' not in data:
        return jsonify({'error': 'items array is required'}), 400
    
    try:
        results = service.analyze_batch(
            items=data['items'],
            user_profile=data.get('user_profile')
        )
        return jsonify({'results': results}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(413)
def too_large(error):
    return jsonify({'error': 'File too large (max 16MB)'}), 413


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


# ==================== MAIN ====================

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🚀 Ingredient Intelligence Flask Server")
    print("="*70)
    print("\n📋 Available Endpoints:")
    print("   GET  /health - Health check")
    print("   POST /api/analyze/image - Analyze from image")
    print("   POST /api/analyze/text - Analyze from text")
    print("   POST /api/extract/ingredients - Extract ingredients only")
    print("   POST /api/user/register - Register user")
    print("   GET  /api/user/<id> - Get user profile")
    print("   POST /api/intake/log - Log consumed product")
    print("   GET  /api/intake/daily/<id> - Daily summary")
    print("   GET  /api/intake/weekly/<id> - Weekly report")
    print("\n🌐 Server starting on http://localhost:5000")
    print("="*70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
