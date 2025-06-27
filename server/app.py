from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

class Plant(db.Model):
    __tablename__ = 'plants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    image = db.Column(db.String)
    price = db.Column(db.Float)
    is_in_stock = db.Column(db.Boolean)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'image': self.image,
            'price': self.price,
            'is_in_stock': self.is_in_stock
        }

class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.get(id)
        if not plant:
            return {'error': 'Plant not found'}, 404
        return plant.to_dict(), 200

    def patch(self, id):
        plant = Plant.query.get(id)
        if not plant:
            return {'error': 'Plant not found'}, 404
        
        data = request.get_json()
        for attr, value in data.items():
            setattr(plant, attr, value)
        
        db.session.add(plant)
        db.session.commit()
        
        return plant.to_dict(), 200

    def delete(self, id):
        plant = Plant.query.get(id)
        if not plant:
            return {'error': 'Plant not found'}, 404
        
        db.session.delete(plant)
        db.session.commit()
        
        return '', 204

api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)