## API

## Using the API

The .env file needs to be setup first, instructions are in the general README file.

### Creating an account

Step 1: Before accessing the API, you need to create an account in order to get a user token. You can create one on the website, or via the API. <br />

Creating an account via the API (example): <br />
` # $ http POST http://localhost:5000/api/users username=alice password=dog email=alice@example.com `

### Creating the API token

Step 2: Getting a user token. Replace username and password with your own credentials: <br />
` # $ http --auth YOUR_USERNAME:YOUR_PASSWORD POST http://localhost:5000/api/tokens `

### Using the API with user token

Step 3: Replace token with your own user token below. Then everything should work. Keep in mind to use the proper method for each command, as listed in activities.py. <br />

` # $ http -A bearer --auth <token> GET http://localhost:5000/api/activities ` <br />

### Troubleshooting

If it says access denied, please check your username and password or regenerate your token. If you try to delete a user or activity via the API, you need to have admin access. 

## How to make a user admin and test admin functionality:
### Step 1: make a user admin
first start the flask app<br />
⁠`flask shell `<br />
then copy paste the following code<br />
⁠`from app.models import Users ⁠`<br />
⁠`from app import db ⁠`<br />

Replace 'YOUR_USERNAME' with the actual username: <br />
⁠`user = Users.query.filter_by(username='YOUR_USERNAME').first() ⁠`<br />
⁠`user.is_admin = True ⁠`<br />
⁠`db.session.commit() ⁠`<br />
⁠`print(f"{user.username} is_admin: {user.is_admin}”) ⁠`<br />
<br />
⁠`exit() ⁠`<br />

### Step 2: Get authentication token<br />
Replace YOUR_USERNAME and YOUR_PASSWORD with actual credentials:<br />

cURL: ⁠`curl -X POST http://localhost:5001/api/tokens -u YOUR_USERNAME:YOUR_PASSWORD ⁠`<br />
Httpie: ` http --auth YOUR_USERNAME:YOUR_PASSWORD POST http://localhost:5000/api/tokens `
Copy the token from the response<br />

### Step 3: test admin delete functionality:<br />
Replace YOUR_TOKEN with the actual token from step 2<br />
Replace USER_ID with the ID of a user you want to delete<br />
⁠cURL: `curl -v -X DELETE http://localhost:5001/api/delete-user/USER_ID -H "Authorization: Bearer YOUR_TOKEN” ⁠`<br />
Httpie: ` # $ http -A bearer --auth YOUR_TOKEN DELETE http://localhost:5000/api/delete-user/USER-ID ` <br />
<br />
Expected response:<br />
`{"message":"User deleted successfully"}`






