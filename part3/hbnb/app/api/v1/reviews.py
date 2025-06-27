#!/usr/bin/env python3
"""API endpoints for Review resources."""

from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask import request

api = Namespace('reviews', description='Review operations')

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})


@api.route('/')
class ReviewList(Resource):
    """Resource for collection of reviews."""

    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review."""
        try:
            review_data = request.json
            new_review = facade.create_review(review_data)

            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': new_review.user.id,
                'place_id': new_review.place.id
            }, 201

        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': f"An unexpected error occurred: {str(e)}"}, 500

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews."""
        try:
            reviews = facade.get_all_reviews()

            return [
                {
                    'id': review.id,
                    'text': review.text,
                    'rating': review.rating
                }
                for review in reviews
            ], 200

        except Exception as e:
            return {'error': f"An unexpected error occurred: {str(e)}"}, 500


@api.route('/<review_id>')
class ReviewResource(Resource):
    """Resource for individual review operations."""

    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID."""
        try:
            try:
                review = facade.get_review(review_id)
            except KeyError:
                return {'error': 'Review not found'}, 404

            return {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user.id,
                'place_id': review.place.id
            }, 200

        except Exception as e:
            return {'error': f"An unexpected error occurred: {str(e)}"}, 500

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information."""
        try:
            review_data = request.json

            try:
                review = facade.get_review(review_id)
            except KeyError:
                return {'error': 'Review not found'}, 404

            facade.update_review(review_id, review_data)

            return {
                'message': 'Review updated successfully'
            }, 200

        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': f"An unexpected error occurred: {str(e)}"}, 500

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review."""
        try:
            try:
                facade.get_review(review_id)
            except KeyError:
                return {'error': 'Review not found'}, 404

            facade.delete_review(review_id)

            return {
                'message': 'Review deleted successfully'
            }, 200

        except Exception as e:
            return {'error': f"An unexpected error occurred: {str(e)}"}, 500


@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    """Resource for retrieving reviews by place."""

    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place."""
        try:
            try:
                reviews = facade.get_reviews_by_place(place_id)
            except KeyError:
                return {'error': 'Place not found'}, 404

            return [
                {
                    'id': review.id,
                    'text': review.text,
                    'rating': review.rating
                }
                for review in reviews
            ], 200

        except Exception as e:
            return {'error': f"An unexpected error occurred: {str(e)}"}, 500
