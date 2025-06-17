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
            transformed_data = {
                'name': place_data.get('title'),
                'description': place_data.get('description', ''),
                'price_per_night': place_data.get('price'),
                'latitude': place_data.get('latitude'),
                'longitude': place_data.get('longitude'),
                'user_id': place_data.get('owner_id'),
                'city_id': place_data.get('city_id', '')
            }
            
            if 'amenities' in place_data and place_data['amenities']:
                transformed_data['amenity_ids'] = place_data['amenities']
            
            new_place = facade.create_place(transformed_data)
            
            return {'id': new_place.id, 'message': 'Place successfully created'}, 201
            
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': "An unexpected error occurred:{}".format(str(e))}, 500

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
                api.abort(404, "Place with id {} not found".format(place_id))
            return place, 200
        except Exception as e:
            return {'error': "An unexpected error occurred: {}".format({str(e)})}, 500

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        try:
            place_data = request.json
            
            transformed_data = {}
            
            field_mapping = {
                'title': 'name',
                'price': 'price_per_night',
                'owner_id': 'user_id'
            }
            
            for key in ['description', 'latitude', 'longitude']:
                if key in place_data:
                    transformed_data[key] = place_data[key]
            
            for api_field, model_field in field_mapping.items():
                if api_field in place_data:
                    transformed_data[model_field] = place_data[api_field]
            
            if 'amenities' in place_data:
                transformed_data['amenity_ids'] = place_data['amenities']
            
            updated_place = facade.update_place(place_id, transformed_data)
            return {'id': updated_place.id, 'message': 'Place updated successfully'}, 200
            
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            if 'not found' in str(e).lower():
                return {'error': str(e)}, 404
            return {'error': "An unexpected error occurred: {}".format(str(e))}, 500
    