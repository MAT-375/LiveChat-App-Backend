# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin


db = SQLAlchemy()

# association table for the many-to-many relationship between users and chat rooms.
user_chatroom = db.Table(
    "user_chatroom",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column(
        "chat_room_id", db.Integer, db.ForeignKey("chat_room.id"), primary_key=True
    ),
)


# models for users, chatroom and messages
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    # many-to-many relationship with chat rooms.
    chat_rooms = db.relationship(
        "ChatRoom", secondary=user_chatroom, back_populates="users"
    )


class ChatRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    descp = db.Column(db.String(200), nullable=False)

    # many-to-many relationship with users.
    users = db.relationship(
        "User", secondary=user_chatroom, back_populates="chat_rooms"
    )


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey("chat_room.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Add timestamp

    sender = db.relationship("User", backref="messages_sent")
    room = db.relationship("ChatRoom", backref="messages")
