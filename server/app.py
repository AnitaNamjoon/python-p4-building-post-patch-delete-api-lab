#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True  # Make JSON responses more human-readable

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    bakeries_serialized = [bakery.to_dict() for bakery in bakeries]

    return jsonify(bakeries_serialized), 200

@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = Bakery.query.get(id)

    if not bakery:
        return jsonify({"message": "Bakery not found"}), 404

    data = request.json  # Assuming you are sending JSON data in the request

    # Update bakery attributes based on the data sent in the request
    if 'name' in data:
        bakery.name = data['name']

    db.session.commit()

    bakery_serialized = bakery.to_dict()
    return jsonify(bakery_serialized), 200

@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.json  # Assuming you are sending JSON data in the request

    # Create a new BakedGood object based on the data sent in the request
    baked_good = BakedGood(name=data['name'], price=data['price'], bakery_id=data['bakery_id'])

    db.session.add(baked_good)
    db.session.commit()

    baked_good_serialized = baked_good.to_dict()
    return jsonify(baked_good_serialized), 201  # 201 Created status code

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get(id)

    if not baked_good:
        return jsonify({"message": "Baked Good not found"}), 404

    db.session.delete(baked_good)
    db.session.commit()

    return jsonify({"message": "Baked Good deleted successfully"}), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
