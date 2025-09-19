from models.vegetable import Vegetable
from db import db

class VegetableService:
    def list_vegetables(self):
        veggies = Vegetable.query.all()
        return [{"id": v.id, "name": v.name, "price": v.price, "stock": v.stock} for v in veggies]

    def create_vegetable(self, data):
        veg = Vegetable(name=data["name"], price=data["price"], stock=data["stock"])
        db.session.add(veg)
        db.session.commit()
        return {"message": "Vegetable added", "id": veg.id}

    def update_vegetable(self, veg_id, data):
        veg = Vegetable.query.get(veg_id)
        if not veg:
            return {"error": "Vegetable not found"}
        veg.name = data.get("name", veg.name)
        veg.price = data.get("price", veg.price)
        veg.stock = data.get("stock", veg.stock)
        db.session.commit()
        return {"message": "Vegetable updated"}

    def delete_vegetable(self, veg_id):
        veg = Vegetable.query.get(veg_id)
        if not veg:
            return {"error": "Vegetable not found"}
        db.session.delete(veg)
        db.session.commit()
        return {"message": "Vegetable deleted"}
