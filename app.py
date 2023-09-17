from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from models import db, User, ChatRoom, Message


app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET@1234"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chat_app.db"
db.init_app(app)
socketio = SocketIO(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# user registration, login, and logout routes.
@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201


@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if user and user.password == password:
        login_user(user)
        return jsonify({"message": "Logged in successfully"}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401


@app.route("/api/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200


# routes for fetching chat rooms.
@app.route("/api/chat/rooms", methods=["GET"])
@login_required
def list_chat_rooms():
    chat_rooms = ChatRoom.query.all()
    rooms_data = [
        {
            "id": room.id,
            "name": room.name,
            # "users": [user.username for user in room.users],
        }
        for room in chat_rooms
    ]
    return jsonify(rooms_data), 200


# routes for fetching chat rooms description.
@app.route("/api/chat/rooms/<int:id>", methods=["GET"])
@login_required
def list_chat_room_detail(id):
    chat_rooms = ChatRoom.query.filter_by(id=id).all()
    rooms_data = [
        {
            "id": room.id,
            "name": room.name,
            "users": [user.username for user in room.users],
            "descp": [room.descp],
        }
        for room in chat_rooms
    ]
    return jsonify(rooms_data), 200


@socketio.on("join_room")
def join_room(data):
    # Handle user joining a chat room
    room_id = data["room_id"]
    join_room(room_id)  # Add the user to the specified chat room
    emit(
        "joined",
        {"message": f"User {current_user.username} has joined the room."},
        room=room_id,
    )


@socketio.on("leave_room")
def leave_room(data):
    # Handle user leaving a chat room
    room_id = data["room_id"]
    leave_room(room_id)  # Remove the user from the specified chat room
    emit(
        "left",
        {"message": f"User {current_user.username} has left the room."},
        room=room_id,
    )


@socketio.on("send_message")
def send_message(data):
    # Handle sending a new message to a chat room
    room_id = data["room_id"]
    message_text = data["message"]
    message = Message(text=message_text, sender=current_user, room_id=room_id)
    # Add the message to the database
    db.session.add(message)
    db.session.commit()
    # Emit the new message to the chat room
    emit(
        "new_message",
        {"message": message.text, "username": current_user.username},
        room=room_id,
    )


# routes for fetching messages from chat rooms.
@app.route("/api/chat/rooms/<int:room_id>/messages", methods=["GET"])
@login_required
def get_room_messages(room_id):
    messages = Message.query.filter_by(room_id=room_id).all()
    messages_data = [
        {
            "id": msg.id,
            "text": msg.text,
            "sender_id": msg.sender_id,
            "room_id": msg.room_id,
            "created_at": msg.created_at,
        }
        for msg in messages
    ]
    return jsonify(messages_data), 200


# routes for posting messages in chat rooms.
@app.route("/api/chat/rooms/<int:room_id>/messages", methods=["POST"])
@login_required
def send_room_message(room_id):
    data = request.json
    message_text = data.get("message")
    message = Message(text=message_text, sender=current_user, room_id=room_id)
    db.session.add(message)
    db.session.commit()
    return (
        jsonify(
            {
                "message": "Message sent successfully",
                "id": message.id,
                "text": message.text,
                "sender_id": message.sender_id,
                "room_id": message.room_id,
                "created_at": message.created_at,
            }
        ),
        201,
    )


if __name__ == "__main__":
    app.run(debug=True)
