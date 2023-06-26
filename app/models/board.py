from app import db

class Board(db.Model):
    # board_id, int, primary key
    # title, string
    # owner, string
    board_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    title = db.Column(db.String)
    owner = db.Column(db.String)