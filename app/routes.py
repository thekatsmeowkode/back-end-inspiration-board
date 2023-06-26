from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card
import requests
import os

# example_bp = Blueprint('example_bp', __name__)
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"details": "invalid data"}, 400))
    
    item = cls.query.get(model_id)
    
    if not item:
        abort((make_response({"message":f"{item} not found"})))
    
    return item

####### POST CARD TO SPECIFIC BOARD ##########
@cards_bp.route("/<board_id>", methods=["POST"])
def create_card(board_id):
    board_to_post = validate_model(Board, board_id)
    request_body = request.get_json()
    try:
        new_card = Card.from_dict(request_body)
        Card.board = board_to_post
    except:
        return jsonify({'details': 'Invalid card request body data'}), 400
    
    db.session.add(new_card)
    db.session.commit()
    
    return jsonify({"task": f"{new_card.to_dict()} successfully created"}), 200

###### DELETE CARD ###############
@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card_to_delete = validate_model(Card, card_id)
    
    db.session.delete(card_to_delete)
    db.session.commit()
    
    return jsonify({"message": f"{card_to_delete} has been successfully deleted"}), 200

######## UPDATE CARD TO INCREASE LIKES ################
@cards_bp.route("/<card_id>", methods=["PUT"])
def update_card(card_id):
    card = validate_model(Card, card_id)
    
    request_body = request.get_json()
    
    card.likes_count = request_body["likes_count"]
    
    db.session.commit()
    
    return jsonify({"message": f"Increased like count on card {card.card_id}"}), 200
    