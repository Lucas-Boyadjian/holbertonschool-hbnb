from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        data_amenity = api.payload
        try:
            new_amenity = facade.create_amenity(data_amenity)
        except ValueError as e:
            api.abort(400, str(e))
        return {"id": new_amenity.id, "name":new_amenity.name}, 201
    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        
        amenities = facade.get_all_amenities()
        return[amenity.to_dict() for amenity in amenities],200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
       
        amenity = facade.get_amenity(amenity_id)
        if amenity is None:
            api.abort(404, "Amenity not found")
        return amenity.to_dict(),200
    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        
        data_amenity = api.payload

        amenity=facade.get_amenity(amenity_id)
        if amenity is None:
            api.abort(404,"Amenity not found")
        try:
            updated_amenity = facade.update_amenity(amenity_id, data_amenity)
        except ValueError as e:
            api.abort(400, str(e))
        return updated_amenity.to_dict(), 200