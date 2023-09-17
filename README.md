
# Real-Time Multi-User Chat Application

This is a real-time multi-user chat application built using Python and Flask. It allows users to create accounts, log in, and participate in chat rooms with real-time messaging capabilities. The application also incorporates a database to store chat messages and user data.

## Table of Contents
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Running the Application](#running-the-application)
  - [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Features

- User Registration: Users can create accounts with unique usernames and passwords.
- User Authentication: Users can log in and log out of their accounts securely.
- Chat Rooms: Users can create, join, and list available chat rooms.
- Real-Time Messaging: Users can send and receive messages in chat rooms in real time.
- Message History: Chat messages are stored in the database, allowing users to view previous messages in a chat room.

## Getting Started

### Prerequisites

Before running the application, you need to have the following installed on your system:

- Python (3.6 or higher)
- pip (Python package manager)
- virtualenv (optional but recommended)

### Installation

1. Clone this repository to your local machine:

```bash
git clone https://github.com/yourusername/flask-chat-app.git
```
Change to the project directory:
```
cd flask-chat-app
```

Create a virtual environment (optional but recommended):
```
python -m venv venv
```
Activate the virtual environment:
#### On macOS and Linux
```source venv/bin/activate```

#### On Windows
```venv\Scripts\activate```

Install the required dependencies:
```pip install -r requirements.txt```

Usage
Running the Application
To run the chat application, follow these steps:

1. Ensure you are in the project directory and your virtual environment is activated.

2. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

Start the Flask development server:
```
flask run
```

The application should now be running locally at http://localhost:5000.

API Endpoints
The chat application exposes the following API endpoints:
```
POST /api/register: Allows a user to create an account.
POST /api/login: Allows a user to log in to their account.
POST /api/logout: Allows a user to log out of their account.
GET /api/chat/rooms: Returns a list of all available chat rooms.
GET /api/chat/rooms/:id: Returns the details of a specific chat room.
POST /api/chat/rooms/:id/messages: Allows a user to send a message to a specific chat room.
GET /api/chat/rooms/:id/messages: Returns a list of messages for a specific chat room.
```
Refer to the API documentation for more details on how to use these endpoints.

## Contributing
Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

#### Fork the repository.
Create a new branch for your feature or bug fix: `git checkout -b feature/your-feature-name` or `git checkout -b bugfix/your-bug-fix`.
Make your changes and commit them: `git commit -m "Your commit message here"`.
Push your changes to your forked repository: `git push origin feature/your-feature-name or git push origin bugfix/your-bug-fix`.
Create a pull request to the main repository.

### License
This project is licensed under the MIT License
