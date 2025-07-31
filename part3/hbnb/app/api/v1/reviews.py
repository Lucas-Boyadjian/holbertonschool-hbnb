from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('reviews', description='Review operations')

review_model = api.model('PlaceReview', {
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user'),
    'place_id': fields.String(description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Bad Request')
    @api.response(500, 'An unexpected error occurred')
    @jwt_required()
    def post(self):
        """Register a new review."""
        current_user_id = get_jwt_identity()
        try:
            review_data = request.json
            place = facade.get_place(review_data['place_id'])

            if place.owner_id == current_user_id:
                return {'error': 'You cannot review your own place'}, 400

            for review in place.reviews:
                if review.user_id == current_user_id:
                    return {'error': 'You have already reviewed this place'}, 400

            review_data['user_id'] = current_user_id
            new_review = facade.create_review(review_data)

            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': str(new_review.user_id),
                'place_id': str(new_review.place_id)
            }, 201

        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': "An unexpected error occurred: {}".format(str(e))}, 500

    @api.response(200, 'List of reviews retrieved successfully')
    @api.response(500, 'An unexpected error occurred')
    def get(self):
        """Retrieve a list of all reviews."""
        try:
            reviews = facade.get_all_reviews()
            return [
                {
                    'id': review.id,
                    'text': review.text,
                    'rating': review.rating,
                    'first_name': review.user.first_name,
                    'last_name': review.user.last_name
                }
                for review in reviews
            ], 200
        except Exception as e:
            return {'error': "An unexpected error occurred: {}".format(str(e))}, 500

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Not found')
    @api.response(500, 'An unexpected error occurred')
    def get(self, review_id):
        """Get review details by ID."""
        try:
            review = facade.get_review(review_id)
            if not review:
                return {'error': 'Review not found'}, 404
            return {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'first_name': review.user.first_name,
                'last_name': review.user.last_name,
                'user_id': str(review.user_id),
                'place_id': str(review.place_id)
            }, 200
        except Exception as e:
            return {'error': "An unexpected error occurred: {}".format(str(e))}, 500

    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(400, 'Bad request')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Not found')
    @api.response(500, 'An unexpected error occurred')
    @api.expect(review_model)
    @jwt_required()
    def put(self, review_id):
        current_user_id = get_jwt_identity()
        current_user = facade.get_user(current_user_id)
        
        if not current_user:
            return {'error': 'Invalid user'}, 401

        is_admin = current_user.is_admin

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        if not is_admin and review.user_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        review_data = request.json
        try:
            updated_review = facade.update_review(review_id, review_data)

            return {
                'id': updated_review.id,
                'text': updated_review.text,
                'rating': updated_review.rating,
                'first_name': updated_review.user.first_name,
                'last_name': updated_review.user.last_name,
                'user_id': str(updated_review.user_id),
                'place_id': str(updated_review.place_id)
            }, 200
        except ValueError as e:
             return {"error": "Invalid input data: {}".format(str(e))}, 400
    
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(400, 'Bad request')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Not found')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review (admin can delete any, user only own)."""
        current_user_id = get_jwt_identity()
        current_user = facade.get_user(current_user_id)

        if not current_user:
            return {'error': 'Invalid user'}, 401

        is_admin = current_user.is_admin

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        if not is_admin and review.user_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        try:
            facade.delete_review(review_id)
            return {'message': 'Review deleted successfully'}, 200
        except Exception as e:
             return {"error": "Invalid input data: {}".format(str(e))}, 400
        
@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Not found')
    @api.response(500, 'An unexpected error occurred')
    def get(self, place_id):
        """Get all reviews for a specific place."""
        try:
            reviews = facade.get_reviews_by_place(place_id)
            return [
                {
                    'id': review.id,
                    'text': review.text,
                    'rating': review.rating,
                    'first_name': review.user.first_name,
                    'last_name': review.user.last_name,
                }
                for review in reviews
            ], 200
        except KeyError:
            return {'error': 'Place not found'}, 404
        except Exception as e:
             return {'error': "An unexpected error occurred: {}".format(str(e))}, 500
        