from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Bad Request')
    @api.response(403, 'Aunauthorized action')
    @jwt_required()
    def post(self):
        """Register a new amenity (admin only)"""
        current_user_id = get_jwt_identity()
        current_user = facade.get_user(current_user_id)
        
        if not current_user:
            return {'error': 'Invalid user'}, 401
    
        if not current_user.is_admin:
            return {'error': 'Admin privileges required'}, 403

        data_amenity = api.payload
        try:
            new_amenity = facade.create_amenity(data_amenity)
        except ValueError as e:
            return {"error": "Invalid input data: {}".format(str(e))}, 400
        return {"id": new_amenity.id, "name": new_amenity.name}, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities], 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if amenity is None:
            api.abort(404, "Amenity not found")
        return amenity.to_dict(), 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(400, 'Bad Request')
    @api.response(403, 'Aunauthorized action')
    @api.response(404, 'Not found')
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity's information (admin only)"""
        current_user_id = get_jwt_identity()
        current_user = facade.get_user(current_user_id)

        if not current_user:
            return {'error': 'Invalid user'}, 401
        
        if not current_user.is_admin:
            return {'error': 'Admin privileges required'}, 403
        
        data_amenity = api.payload
        amenity = facade.get_amenity(amenity_id)
        if amenity is None:
            api.abort(404, "Amenity not found")
        try:
            updated_amenity = facade.update_amenity(amenity_id, data_amenity)
        except ValueError as e:
            return {"error": "Invalid input data: {}".format(str(e))}, 400
        return updated_amenity.to_dict(), 200
