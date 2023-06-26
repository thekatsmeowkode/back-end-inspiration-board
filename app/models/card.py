from app import db

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer)
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id', nullable=False))
    
    #ON BOARD
    # cards = db.relationship('Card', back_populates='cards')
    
    @classmethod
    def from_dict(cls, card_data):
        new_card = Card(message=card_data["message"],
                        likes_count=card_data["likes_count"],
                        board_id=card_data["board_id"])
        return new_card
    
    def to_dict(self):
        card_as_dict = {}
        card_as_dict["card_id"] = self.card_id
        card_as_dict["message"] = self.message
        card_as_dict["likes_count"] = self.likes_count
        
        if self.board_id:
            card_as_dict["board_id"] = self.board_id
            
        return card_as_dict