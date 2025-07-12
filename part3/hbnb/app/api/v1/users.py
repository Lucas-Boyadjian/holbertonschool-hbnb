from flask_restx import Namespace, Resource, fields
from app.services import facade
from app import bcrypt
import re
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask import request


api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

def is_valid_email(email):
    pattern = r"^[^@]+@[^@]+\.[^@]+$"
    return re.match(pattern, email) is not None

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Bad request')
    @api.response(403, "Unauthorized action")
    @api.response(409, 'Conflict')
    @jwt_required()
    def post(self):
        """Create a new user (admin only)"""
        current_user_id = get_jwt_identity()

        # Récupère l'utilisateur complet depuis la base de données
        current_user = facade.get_user(current_user_id)

        if not current_user or not current_user.is_admin:
            return {'error': 'Admin privileges required'}, 403
        
        user_data = api.payload

        if facade.get_user_by_email(user_data['email']):
            return {'error': 'Email already registered'}, 409
        if not is_valid_email(user_data["email"]):
            return {"error": "Invalid email"}, 400

        hashed_password = bcrypt.generate_password_hash(
            user_data['password']).decode('utf-8')
        user_data['password'] = hashed_password

        try:
            new_user = facade.create_user(user_data)
            return {"id": new_user.id, "message": "User successfully created"}, 201
        except ValueError:
            return {"error": "Invalid input data"}, 400
            
    @api.response(200, "OK")
    def get(self):
        """Get a list of user"""
        users = facade.get_all_users()
        return [user.to_dict() for user in users], 200
             

@api.route("/<user_id>")
class UserRessource(Resource):
    @api.response(200, "User details retrieved successfully")
    @api.response(404, "Not found")
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404
        return user.to_dict(), 200
    
    @api.response(200, "OK")
    @api.response(400, "Bad Request")
    @api.response(403, "Unauthorized action")
    @api.response(404, "Not Found")
    @api.response(409, "Conflict")
    @api.expect(user_model, validate=False)
    @jwt_required()
    def put(self, user_id):
        """Update the data of user (admin: tout, user: limité)"""
        current_user_id = get_jwt_identity()
        
        current_user = facade.get_user(current_user_id)
        
        if not current_user:
            return {'error': 'Invalid user'}, 401
        
        is_admin = current_user.is_admin
        
        user_to_update = facade.get_user(user_id)
        if not user_to_update:
            return {"error": "User not found"}, 404
        
        if not is_admin and current_user_id != user_id:
            return {'error': 'Admin privileges required'}, 403
        
        data = api.payload
        
        if not is_admin:
            if 'email' in data or 'password' in data:
                return {'error': 'Admin privileges required'}, 403
        else:
            email = data.get('email')
            if email:
                if not is_valid_email(email):
                    return {'error': 'Invalid email'}, 400
                existing_user = facade.get_user_by_email(email)
                if existing_user and str(existing_user.id) != str(user_id):
                    return {'error': 'Email already in use'}, 409
            
            if "password" in data:
                hashed_password = bcrypt.generate_password_hash(
                    data['password']).decode('utf-8')
                data['password'] = hashed_password

        try:
            updated_user = facade.put_user(user_id, data)
            if not updated_user:
                return {"error": "User not found"}, 404
            return updated_user.to_dict(), 200
        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            print(e)
            return {"error": "Bad Request"}, 400
