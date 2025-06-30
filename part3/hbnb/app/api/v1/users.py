from flask_restx import Namespace, Resource, fields
from app.services import facade
from app import bcrypt
import re
from flask_jwt_extended import jwt_required, get_jwt_identity


api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
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
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        try:
            user_data = api.payload
            # Simulate email uniqueness check (to be replaced by real validation with persistence)
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
                return {'error': 'Email already registered'}, 400
            
            if not is_valid_email(user_data["email"]):
                return {"error": "Invalid email"}, 400
            
            hashed_password = bcrypt.generate_password_hash(
                user_data['password']).decode('utf-8')
            user_data['password'] = hashed_password
            
            new_user = facade.create_user(user_data)
            return {"id": new_user.id, "message": "User successfully created"}, 201
        
        except ValueError as e:
            return {"error": "Invalid input data"}, 400
        
    @api.response(200, "OK")
    def get(self):
        """Get a list of user"""
        users = facade.get_all_user()
        return [user.to_dict() for user in users], 200
             

@api.route("/<user_id>")
class UserRessource(Resource):
    @api.response(200, "User details retrieved successfully")
    @api.response(404, "User not found")
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404
        return user.to_dict(), 200
    
    @api.response(200, "OK")
    @api.response(404, "Not Found")
    @api.response(400, "Bad Request")
    @api.expect(user_model, validate=True)
    @jwt_required()
    def put(self, user_id):
        """Update the data of user"""
        current_user_id = get_jwt_identity()

        if str(current_user_id) != str(user_id):
            return {"error": "Unauthorized action"}, 403

        user_data = api.payload

        if "email" in user_data or "password" in user_data:
            return {"error": "You cannot modify email or password"}, 400
        try:
            updated_user = facade.put_user(user_id, user_data)
            if not updated_user:
                return {"error": "User not found"}, 404
            return updated_user.to_dict(), 200
        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            print(e)
            return {"error": "Bad Request"}, 400
