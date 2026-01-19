import requests
import json

def main():
    print("This is to test the api")
    LOGIN_URL = "http://127.0.0.1:5000/api/tokens"

    BASIC_AUTH_CREDENTIALS = ("Lars", "hello123")

    response = requests.post(LOGIN_URL, auth=BASIC_AUTH_CREDENTIALS)

    data = response.json()
    
    token = data.get("token")

    if token:
        print("Token retrieved succesfully!")
    else:
        print("Token creation failed!")


    HEADERS = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print("--- Testing retrieving activities without a token ---")
    response = requests.get("http://127.0.0.1:5000/api/activities")
    print(response.json())

    print("--- Testing retrieving activities with a token ---")
    response = requests.get("http://127.0.0.1:5000/api/activities", headers=HEADERS)
    print(response.json())

    print("--- Testing retrieving a specific activity without a token ---")
    response = requests.get("http://127.0.0.1:5000/api/activities/1")
    print(response.json())

    print("--- Testing retrieving a specific activity with a token---")
    response = requests.get("http://127.0.0.1:5000/api/activities/1", headers=HEADERS)
    print(response.json())

    print("--- Testing retrieving from the Sport & Fitness category without a token ---")
    response = requests.get("http://127.0.0.1:5000/api/categories/1")
    print(response.json())

    print("--- Testing retrieving from the Sport & Fitness category with a token---")
    response = requests.get("http://127.0.0.1:5000/api/categories/1", headers=HEADERS)
    print(response.json())

    print("--- Testing retrieving all activities from the type Tennis without a token ---")
    response = requests.get("http://127.0.0.1:5000/api/categories/activity_type/Tennis")
    print(response.json())

    print("--- Testing retrieving all activities from the type Tennis with a token---")
    response = requests.get("http://127.0.0.1:5000/api/categories/activity_type/Tennis", headers=HEADERS)
    print(response.json())

    print("--- Testing retrieving all activities created by a specific user without a token ---")
    response = requests.get("http://127.0.0.1:5000/api/profile/activities_created/Lars")
    print(response.json())

    print("--- Testing retrieving all activities created by a specific user with a token---")
    response = requests.get("http://127.0.0.1:5000/api/profile/activities_created/Lars", headers=HEADERS)
    print(response.json())

    new_activity = {
        "title": "football",
        "location": "Groningen",
        "activity_date": "20/01/2026",
        "activity_time": "10:00",
        "max_participants": "15",
        "category_id": "1",
        "activity_type_id": "5"
    }

    print("--- Testing creating a new activity without a token ---")
    response = requests.post("http://127.0.0.1:5000/api/create_activities", json=new_activity)
    print(response.json())

    print("--- Testing creating a new activity with a token---")
    response = requests.post("http://127.0.0.1:5000/api/create_activities", headers=HEADERS, json=new_activity)
    print(response.json())

    edit_activity = {
        "description": "Lets go!"
    }
    print("--- Testing editing an activity without a token ---")
    response = requests.put("http://127.0.0.1:5000/api/edit_activity/1", json=edit_activity)
    print(response.json())

    print("--- Testing editing an activity with a token---")
    response = requests.put("http://127.0.0.1:5000/api/edit_activity/1", headers=HEADERS, json=edit_activity)
    print(response.json())

    new_user = {
        "email": "hello123@example.com",
        "username": "Test_subject_102",
        "password": "Bonjour179",

    }
    print("--- Testing creating a new user without a token. No token necessary---")
    response = requests.post("http://127.0.0.1:5000/api/users", json=new_user)
    print(response.json())
    
    edit_user = {
        "bio": "LETS GOOOOOO!"
    }
    print("--- Testing editing a user without a token ---")
    response = requests.put("http://127.0.0.1:5000/api/users/1", json=edit_user)
    print(response.json())

    print("--- Testing editing a user with a token---")
    response = requests.put("http://127.0.0.1:5000/api/users/1", headers=HEADERS, json=edit_user)
    print(response.json())
    
    print("--- Testing retrieving all users without a token ---")
    response = requests.get("http://127.0.0.1:5000/api/profiles")
    print(response.json())

    print("--- Testing retrieving all users with a token---")
    response = requests.get("http://127.0.0.1:5000/api/profiles", headers=HEADERS)
    print(response.json())
    
    print("--- Testing retrieving a specific user without a token ---")
    response = requests.get("http://127.0.0.1:5000/api/profile/Lars")
    print(response.json())

    print("--- Testing retrieving a specific user with a token---")
    response = requests.get("http://127.0.0.1:5000/api/profile/Lars", headers=HEADERS)
    print(response.json())






   








    

if __name__ == "__main__":
    main()