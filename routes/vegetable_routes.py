from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.vegetable_service import VegetableService
from schemas.vegetable_schema import VegetableSchema
from marshmallow import ValidationError  # ✅ add this

vegetable_bp = Blueprint("vegetables", __name__)
vegetable_schema = VegetableSchema()
vegetable_service = VegetableService()

@vegetable_bp.route("/", methods=["GET"])
@jwt_required()
def list_vegetables():
    """
    Get all vegetables
    ---
    tags:
      - Vegetables
    security:
      - Bearer: []
    responses:
      200:
        description: List of vegetables
    """
    veggies = vegetable_service.list_vegetables()
    return jsonify(vegetable_schema.dump(veggies, many=True))

@vegetable_bp.route("/", methods=["POST"])
@jwt_required()
def create_vegetable():
    """
    Add a new vegetable
    ---
    tags:
      - Vegetables
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        schema:
          required:
            - name
            - price
            - stock
          properties:
            name:
              type: string
            price:
              type: number
            stock:
              type: integer
    responses:
      201:
        description: Vegetable created
    """
    try:
        data = vegetable_schema.load(request.json)  # ✅ validation here
    except ValidationError as err:
        return jsonify(err.messages), 400

    veg = vegetable_service.create_vegetable(data)
    return vegetable_schema.dump(veg), 201

@vegetable_bp.route("/<string:veg_id>", methods=["PUT"])
@jwt_required()
def edit_vegetable(veg_id):
    """
    Update a vegetable
    ---
    tags:
      - Vegetables
    security:
      - Bearer: []
    parameters:
      - in: path
        name: veg_id
        type: integer
      - in: body
        name: body
        schema:
          properties:
            name:
              type: string
            price:
              type: number
            stock:
              type: integer
    responses:
      200:
        description: Vegetable updated
    """
    try:
        data = vegetable_schema.load(request.json, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    veg = vegetable_service.update_vegetable(veg_id, data)
    if not veg:
        return jsonify({"error": "Vegetable not found"}), 404

    return vegetable_schema.dump(veg), 200

@vegetable_bp.route("/<string:veg_id>", methods=["DELETE"])
@jwt_required()
def remove_vegetable(veg_id):
    """
    Delete a vegetable
    ---
    tags:
      - Vegetables
    security:
      - Bearer: []
    parameters:
      - in: path
        name: veg_id
        type: integer
    responses:
      200:
        description: Vegetable deleted
    """
    success = vegetable_service.delete_vegetable(veg_id)
    if not success:
        return jsonify({"error": "Vegetable not found"}), 404

    return jsonify({"message": "Vegetable deleted"}), 200
