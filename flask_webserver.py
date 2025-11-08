from flask import Flask, jsonify, request
from db import db, init_app
from models import User, Allergen, Preferences, user_allergens, user_preferences
from init_db import seed_data

app = init_app()
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
    with app.app_context():  # push app context
        db.create_all()      # ensure all tables exist
        seed_data()          # now seed the tables
    app.run(debug=True)

