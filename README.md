# DDWT_final_project
Final project databases where we design Meet &amp; Go Groningen, an app where people can meet eachother to do activities

Meet & Go Groningen is a web-based social platform designed to help people in Groningen connect through shared activities.
Users can browse activities, join events, and create their own activities, all organised by categories and activity types.

The platform lowers the barrier to social interaction by bringing people together around everyday interests such as sports, studying, leisure, and social events.
Each activity includes participant management, capacity limits, and user profiles to create a safe and structured environment.

# Installation Guide
Follow the steps below to set up and run the project locally.

### 1 - Clone the repository
git clone <your-repository-url> <br>
cd <project-folder>

### 2 - Create and activate a virtual environment
Using a virtual environment is strongly recommended to avoid dependency conflicts.

python -m venv .venv <br>
source .venv/bin/activate        # macOS / Linux <br>
.venv\Scripts\activate           # Windows

### 3 - Install dependencies
Install all required packages using pip:
<li>flask</li>
<li>flask-login</li>
<li>flask-wtf</li>
<li>python-dotenv</li>
<li>flask-sqlalchemy</li>
<li>flask-migrate</li>
<li>flask-avatars</li>
<li>flask-httpauth</li>
<li>email-validator</li>

### 4 - Set environment variables
Create a .env file in the project root and add the following:

FLASK_APP=app.py <br>
FLASK_ENV=development <br>
SECRET_KEY=your-secret-key

Put the .env file at the same level as your app.

### 5 - Initialize the database
The database for this project is already initialized, so you can use that directly in you project if you want.

If you intend to initialize a new database, you can use the following:

flask db init <br>
flask db migrate <br>
flask db upgrade

### 6 - run the application
Start the development server, via terminal: <br>
python run.py


Click on the link or open your browser and navigate to:
http://127.0.0.1:5000

### How to make a user admin and test admin functionality:
#### Step 1: make a user admin
first start the flask app
⁠ `flask shell `
then copy paste the following code
⁠ `from app.models import Users ⁠`
⁠ `from app import db ⁠`

`# Replace 'YOUR_USERNAME' with the actual username:`
⁠ `user = Users.query.filter_by(username='YOUR_USERNAME').first() ⁠`
⁠ `user.is_admin = True ⁠`
⁠ `db.session.commit() ⁠`
⁠ `print(f"{user.username} is_admin: {user.is_admin}”) ⁠`

⁠ `exit() ⁠`

#### Step 2: Get authentication token
`# Replace YOUR_USERNAME and YOUR_PASSWORD with actual credentials:`
⁠ `curl -X POST http://localhost:5001/api/tokens -u YOUR_USERNAME:YOUR_PASSWORD ⁠`
Copy the token from the response

#### Step 3: test admin delete functionality:
`# Replace YOUR_TOKEN with the actual token from step 2`
`# Replace USER_ID with the ID of a user you want to delete`
⁠ `curl -v -X DELETE http://localhost:5001/api/delete-user/USER_ID -H "Authorization: Bearer YOUR_TOKEN” ⁠`

expected response:
`{"message":"User deleted successfully"}`