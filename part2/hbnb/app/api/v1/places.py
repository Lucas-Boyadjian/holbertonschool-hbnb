#!/usr/bin/env python3

from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade


api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        try:
            place_data = request.json

            # Prepare data for create_place method
            place_info = {
                'title': place_data.get('title'),
                'description': place_data.get('description'),
                'price': place_data.get('price'),
                'latitude': place_data.get('latitude'),
                'longitude': place_data.get('longitude'),
                'owner_id': place_data.get('owner_id'),
                'amenity_ids': place_data.get('amenities', [])
            }

            new_place = facade.create_place(place_info)

            return {
                'id': new_place.id,
                'title': new_place.title,
                'message': 'Place created successfully'
            }, 201

        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': f"An unexpected error occurred: {str(e)}"}, 500

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        try:
            places = facade.get_all_places()
            return places, 200
        except Exception as e:
            return {'error': "An unexpected error occurred:{}".format(str(e))}, 500

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        try:
            place = facade.get_place(place_id)
            
            if not place:
                return {'error': 'Place not found'}, 404
                
            owner = facade.get_user(place.owner_id)
            owner_data = None
            if owner:
                owner_data = {
                    'id': owner.id,
                    'first_name': owner.first_name,
                    'last_name': owner.last_name,
                    'email': owner.email
                }
                
            amenities_data = []
            for amenity_id in place.amenity_ids:
                amenity = facade.get_amenity(amenity_id)
                if amenity:
                    amenities_data.append({
                        'id': amenity.id,
                        'name': amenity.name
                    })
            
            response = {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner': owner_data,
                'amenities': amenities_data
            }
            
            return response, 200
            
        except Exception as e:
            return {'error': f"An error occurred: {str(e)}"}, 500
   

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        try:
            place_data = request.json

            # Check if place exists
            existing_place = facade.get_place(place_id)
            if not existing_place:
                return {'error': 'Place not found'}, 404

            # Prepare update data
            update_data = {
                'title': place_data.get('title'),
                'description': place_data.get('description'),
                'price': place_data.get('price'),
                'latitude': place_data.get('latitude'),
                'longitude': place_data.get('longitude')
            }

            # Handle amenities separately if provided
            if 'amenities' in place_data:
                update_data['amenity_ids'] = place_data['amenities']

            # Update the place
            updated_place = facade.update_place(place_id, update_data)

            return {
                'id': updated_place.id,
                'title': updated_place.title,
                'message': 'Place updated successfully'
            }, 200

        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': f"An unexpected error occurred: {str(e)}"}, 500
    