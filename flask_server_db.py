"""
Flask Backend Server with Database Integration
Ingredient Intelligence Analyzer with SQLAlchemy
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import json

# Database imports
from src.db import db
from src.init_db import init_database
from src.user_profile_manager import (
    UserProfileManager,
    get_all_allergens,
    get_all_preferences,
    get_all_comorbidities
)
from src.db_models import User, Ingredient, Product, IntakeLog

# Service import
from app import IngredientAnalysisService

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Database Configuration
# Use absolute path to ensure database is in project root, not instance folder
DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ingredient_analyzer.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Upload Configuration
UPLOAD_FOLDER = 'temp_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Initialize database
db.init_app(app)

# Create upload folder
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize service
service = IngredientAnalysisService()


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ==================== HEALTH CHECK ====================

@app.route('/', methods=['GET'])
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'Ingredient Intelligence Analyzer',
        'version': '4.0.0',
        'database': 'connected'
    })


# ==================== USER MANAGEMENT ====================

@app.route('/api/user/register', methods=['POST'])
def register_user():
    """
    Register new user with profile.
    
    Body: {
        "username": "johndoe",
        "email": "john@example.com",
        "personal_info": {...},
        "allergens": ["Peanuts", "Shellfish"],
        "preferences": ["Vegan", "Low Sodium"],
        "comorbidities": ["Diabetes Type 2"]
    }
    """
    data = request.get_json()
    
    try:
        user = UserProfileManager.create_user_from_dict(data)
        
        return jsonify({
            'success': True,
            'user_id': user.user_id,
            'message': 'User registered successfully'
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/user/<user_id>', methods=['GET'])
def get_user(user_id):
    """Get user profile."""
    try:
        user = UserProfileManager.get_user(user_id=user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        profile = UserProfileManager.get_user_profile_dict(user)
        return jsonify(profile), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user profile."""
    data = request.get_json()
    
    try:
        user = UserProfileManager.get_user(user_id=user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Update basic info
        if 'full_name' in data:
            user = UserProfileManager.update_user(user, full_name=data['full_name'])
        if 'age' in data:
            user = UserProfileManager.update_user(user, age=data['age'])
        if 'email' in data:
            user = UserProfileManager.update_user(user, email=data['email'])
        
        # Update allergens
        if 'allergens' in data:
            UserProfileManager.set_allergens(user, data['allergens'])
        
        # Update preferences
        if 'preferences' in data:
            UserProfileManager.set_preferences(user, data['preferences'])
        
        # Update comorbidities
        if 'comorbidities' in data:
            UserProfileManager.set_comorbidities(user, data['comorbidities'])
        
        profile = UserProfileManager.get_user_profile_dict(user)
        return jsonify({'success': True, 'profile': profile}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete user profile."""
    try:
        user = UserProfileManager.get_user(user_id=user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        UserProfileManager.delete_user(user)
        
        return jsonify({'success': True, 'message': 'User deleted'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== ALLERGENS / PREFERENCES / COMORBIDITIES ====================

@app.route('/api/allergens', methods=['GET'])
def list_allergens():
    """Get all available allergens."""
    try:
        allergens = get_all_allergens()
        return jsonify({'allergens': allergens}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/preferences', methods=['GET'])
def list_preferences():
    """Get all available preferences."""
    try:
        preferences = get_all_preferences()
        return jsonify({'preferences': preferences}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/comorbidities', methods=['GET'])
def list_comorbidities():
    """Get all available comorbidities."""
    try:
        comorbidities = get_all_comorbidities()
        return jsonify({'comorbidities': comorbidities}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== ANALYSIS ENDPOINTS ====================

@app.route('/api/analyze/image', methods=['POST'])
def analyze_image():
    """
    Analyze product from uploaded image.
    
    Form data:
        - image: file (required)
        - user_id: string (optional)
    """
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
        if 'user_id' in request.form:
            user_id = request.form['user_id']
            user = UserProfileManager.get_user(user_id=user_id)
            if user:
                user_profile = UserProfileManager.get_user_profile_dict(user)
        
        # Analyze
        result = service.analyze_image(temp_path, user_profile)
        
        # Store ingredients in database (if analysis successful)
        if result.get('success') and 'ingredients' in result:
            ingredient_names = result['ingredients']
            for ing_name in ingredient_names:
                Ingredient.get_or_create(ing_name)
        
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
        - user_id: string (optional)
    """
    data = request.get_json()
    
    if not data or 'ingredients_text' not in data:
        return jsonify({'error': 'ingredients_text is required'}), 400
    
    try:
        # Get user profile if provided
        user_profile = None
        if 'user_id' in data:
            user = UserProfileManager.get_user(user_id=data['user_id'])
            if user:
                user_profile = UserProfileManager.get_user_profile_dict(user)
        
        result = service.analyze_text(
            ingredients_text=data['ingredients_text'],
            product_type=data.get('product_type'),
            user_profile=user_profile,
            expiration_date=data.get('expiration_date')
        )
        
        # Store ingredients in database
        if result.get('success') and 'ingredients' in result:
            for ing_name in result['ingredients']:
                Ingredient.get_or_create(ing_name)
        
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
        filename = secure_filename(file.filename)
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], f"temp_{filename}")
        file.save(temp_path)
        
        result = service.extract_ingredients_only(temp_path)
        
        os.remove(temp_path)
        
        return jsonify(result), 200
    
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return jsonify({'error': str(e)}), 500


# ==================== INGREDIENTS DATABASE ====================

@app.route('/api/ingredients', methods=['GET'])
def list_ingredients():
    """
    Get all ingredients in database.
    
    Query params:
        - limit: max results (default 100)
        - search: search term
    """
    try:
        limit = request.args.get('limit', 100, type=int)
        search = request.args.get('search', '')
        
        if search:
            ingredients = Ingredient.query.filter(
                Ingredient.name.ilike(f'%{search}%')
            ).limit(limit).all()
        else:
            ingredients = Ingredient.query.order_by(
                Ingredient.times_seen.desc()
            ).limit(limit).all()
        
        return jsonify({
            'ingredients': [i.to_dict() for i in ingredients],
            'total': len(ingredients)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/ingredients/<int:ingredient_id>', methods=['GET'])
def get_ingredient(ingredient_id):
    """Get ingredient details."""
    try:
        ingredient = Ingredient.query.get(ingredient_id)
        
        if not ingredient:
            return jsonify({'error': 'Ingredient not found'}), 404
        
        return jsonify(ingredient.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/ingredients/stats', methods=['GET'])
def ingredient_stats():
    """Get ingredient database statistics."""
    try:
        total_ingredients = Ingredient.query.count()
        natural_count = Ingredient.query.filter_by(is_natural=True).count()
        artificial_count = Ingredient.query.filter_by(is_artificial=True).count()
        allergen_count = Ingredient.query.filter_by(is_allergen=True).count()
        
        # Most common ingredients
        top_ingredients = Ingredient.query.order_by(
            Ingredient.times_seen.desc()
        ).limit(10).all()
        
        return jsonify({
            'total_ingredients': total_ingredients,
            'natural_ingredients': natural_count,
            'artificial_ingredients': artificial_count,
            'allergen_ingredients': allergen_count,
            'top_ingredients': [
                {'name': i.name, 'times_seen': i.times_seen} 
                for i in top_ingredients
            ]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== INTAKE TRACKING ====================

@app.route('/api/intake/log', methods=['POST'])
def log_intake():
    """
    Log consumed product.
    
    JSON body:
        - user_id: string (required)
        - analysis_result: object (required)
        - quantity: number (optional)
        - unit: string (optional)
    """
    data = request.get_json()
    
    if not data or 'user_id' not in data or 'analysis_result' not in data:
        return jsonify({'error': 'user_id and analysis_result are required'}), 400
    
    try:
        user = UserProfileManager.get_user(user_id=data['user_id'])
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        analysis = data['analysis_result']
        
        # Create intake log
        log = IntakeLog(
            user_id=user.id,
            product_name=analysis.get('product_name'),
            product_type=analysis.get('product_type'),
            quantity=data.get('quantity'),
            unit=data.get('unit'),
            analysis_json=json.dumps(analysis),
            safety_score=analysis.get('analysis', {}).get('overall_safety_score'),
            warnings_count=len(analysis.get('analysis', {}).get('personalized_warnings', []))
        )
        
        db.session.add(log)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'entry_id': log.id,
            'message': 'Intake logged successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/intake/history/<user_id>', methods=['GET'])
def get_intake_history(user_id):
    """Get intake history for user."""
    try:
        user = UserProfileManager.get_user(user_id=user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        limit = request.args.get('limit', 50, type=int)
        
        logs = IntakeLog.query.filter_by(user_id=user.id).order_by(
            IntakeLog.timestamp.desc()
        ).limit(limit).all()
        
        return jsonify({
            'history': [log.to_dict() for log in logs],
            'total': len(logs)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/intake/<user_id>/<int:entry_id>', methods=['DELETE'])
def delete_intake_entry(user_id, entry_id):
    """Delete intake entry."""
    try:
        user = UserProfileManager.get_user(user_id=user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        log = IntakeLog.query.filter_by(id=entry_id, user_id=user.id).first()
        
        if not log:
            return jsonify({'error': 'Entry not found'}), 404
        
        db.session.delete(log)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Entry deleted'}), 200
        
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
    # Initialize database (creates tables and seeds data if needed)
    with app.app_context():
        print("\n🗄️  Checking database...")
        print(f"📁 Database path: {DATABASE_PATH}")
        
        db_exists = os.path.exists(DATABASE_PATH)
        
        if not db_exists:
            print("📦 Database not found. Creating new database...")
            init_database(app)
            print("✅ Database created and initialized successfully!")
        else:
            print("✓ Database file exists")
            
            # Ensure all tables exist (in case schema changed)
            try:
                db.create_all()
                print("✓ Database tables verified")
            except Exception as e:
                print(f"⚠️  Error verifying tables: {e}")
    
    print("\n" + "="*70)
    print("🚀 Ingredient Intelligence Flask Server (Database Edition)")
    print("="*70)
    print("\n📋 Available Endpoints:")
    print("   GET  /health - Health check")
    print("   POST /api/user/register - Register user")
    print("   GET  /api/user/<id> - Get user profile")
    print("   GET  /api/allergens - List allergens")
    print("   GET  /api/preferences - List preferences")
    print("   GET  /api/comorbidities - List comorbidities")
    print("   POST /api/analyze/image - Analyze from image")
    print("   POST /api/analyze/text - Analyze from text")
    print("   GET  /api/ingredients - List ingredients")
    print("   POST /api/intake/log - Log consumed product")
    print("   GET  /api/intake/history/<id> - Get intake history")
    print("\n🌐 Server starting on http://localhost:5000")
    print("="*70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
