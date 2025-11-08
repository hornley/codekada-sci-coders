from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([{'id': item.id, 'name': item.name} for item in items])

# Initialize DB on startup
def init_db():
    with app.app_context():
        db.create_all()
        if not Item.query.first():
            db.session.add(Item(name="Sample Item"))
            db.session.commit()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
