from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.user import User
from schemas.user_schema import UserSchema
from services.auth_service import AuthService
from marshmallow import ValidationError  # ✅ add this

auth_bp = Blueprint("auth", __name__)
auth_service = AuthService()
auth_schema = UserSchema()

@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Login to get a JWT token
    ---
    tags:
      - Auth
    parameters:
      - in: body
        name: body
        schema:
          required:
            - username
            - password
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: JWT token
        schema:
          properties:
            access_token:
              type: string
      401:
        description: Invalid credentials
    """
    try:
        data = auth_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    user = auth_service.verify_user(data["username"], data["password"])
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity=user.username)
    return jsonify(access_token=token), 200
