from flask import Flask, jsonify, request
from db import db, init_app
from models import User, Allergen, Preferences, user_allergens, user_preferences

app = init_app()

# Initialize DB with sample data
def init_db():
    with app.app_context():
        db.create_all()
        
        # Add sample allergens
        if not Allergen.query.first():
            allergen1 = Allergen(name="Peanuts")
            allergen2 = Allergen(name="Gluten")
            db.session.add_all([allergen1, allergen2])
        
        # Add sample preferences
        if not Preferences.query.first():
            pref1 = Preferences(name="Vegan", type="diet")
            pref2 = Preferences(name="Low Sugar", type="health")
            db.session.add_all([pref1, pref2])
        
        # Add sample user
        if not User.query.first():
            user = User(
                username="alice",
                password_hash="hash",
                password_salt="salt",
                first_name="Alice",
                last_name="Smith"
            )
            user.allergens.append(allergen1)
            user.preferences.append(pref1)
            db.session.add(user)
        
        db.session.commit()

# Routes
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    result = []
    for u in users:
        result.append({
            'id': u.id,
            'username': u.username,
            'allergens': [a.name for a in u.allergens],
            'preferences': [p.name for p in u.preferences]
        })
    return jsonify(result)

@app.route('/allergens', methods=['GET'])
def get_allergens():
    allergens = Allergen.query.all()
    return jsonify([{'id': a.id, 'name': a.name} for a in allergens])

@app.route('/preferences', methods=['GET'])
def get_preferences():
    prefs = Preferences.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'type': p.type} for p in prefs])

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
