from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from app.models.card import Card

board_bp = Blueprint("boards", __name__, url_prefix="/boards")
cards_bp = Blueprint("cards", __name__, url_prefix="/cards")


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"details": "Invalid data"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response(
            {"details": f"{cls.__name__} {model_id} is not found"}, 404))

    return model

####### POST A BOARD ##########
@board_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()

    new_board = Board.from_dict(request_body)

    db.session.add(new_board)
    db.session.commit()

    return {"Boards": new_board.to_dict()}, 201

####### GET ALL BOARD ##########
@board_bp.route("", methods=["GET"])
def read_all_boards():
    boards = Board.query.all()
    boards_response = []

    for board in boards:
        boards_response.append(board.to_dict())

    return jsonify(boards_response), 200

####### GET A SINGLE BOARD ##########
@board_bp.route("/<board_id>", methods=["GET"])
def read_single_board(board_id):

    board = validate_model(Board, board_id)

    return board.to_dict(), 200

# ####### POST CARD TO SPECIFIC BOARD ##########
@board_bp.route("/<board_id>/cards", methods=["POST"])
def create_card_of_board(board_id):
    board_to_post = validate_model(Board, board_id)
    request_body = request.get_json()

    try:
        new_card = Card.from_dict(request_body)
        if len(new_card.message) > 40:
            return jsonify({'details': 'Please enter a message within 40 characters!'}), 400
        new_card.board = board_to_post
    except:
        return jsonify({'details': 'Invalid card request body data'}), 400

    db.session.add(new_card)
    db.session.commit()

    return jsonify({"Cards": f"{new_card.to_dict()} successfully created"}), 201


####### GET ALL CARDS OF A SELECTED BOARD ##########
@board_bp.route("/<board_id>/cards", methods=["GET"])
def read_cards_of_board(board_id):
    board = validate_model(Board, board_id)
    card_response = []

    for card in board.cards:
        card_dict = card.to_dict()
        card_dict["board_id"] = board.board_id
        card_response.append(card_dict)

    return jsonify(card_response), 200


###### DELETE CARD ###############
@cards_bp.route("/<card_id>", methods=["DELETE"])
def delete_card(card_id):
    card_to_delete = validate_model(Card, card_id)

    db.session.delete(card_to_delete)
    db.session.commit()

    return jsonify({"message": f"{card_to_delete} has been successfully deleted"}), 200

######## UPDATE CARD TO INCREASE LIKES ################
@cards_bp.route("/<card_id>/like", methods=["PATCH"])
def update_card(card_id):
    card = validate_model(Card, card_id)

    if not card.likes_count:
        card.likes_count = 0
    
    card.likes_count += 1

    db.session.commit()

    return card.to_dict(), 200
