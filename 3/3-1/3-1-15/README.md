# TASK DESCRIPTION

Your task is to create a **FastAPI** endpoint that accepts a **POST** request with user data in the request body. The user data must include the following fields:

- `name` (str): The username (*required*).
- `email` (str): The user's email address (*required* and must be in a valid email format).
- `age` (int): The user's age (*optional*, but must be a positive integer if specified).
- `is_subscribed` (bool): A flag indicating whether the user is subscribed to the newsletter (*optional*).

1. Define a **Pydantic** model named `UserCreate` to represent the user data. Apply appropriate validation rules to ensure that the data is correct.

2. Create a **POST** route `/create_user` that accepts **JSON** data according to the `UserCreate` model.

3. Implement a function to process the incoming user data and return a response with the received user information.

## Example

JSON request:

```json
    {
     "name": "Alice",
     "email": "alice@example.com",
     "age": 30,
     "is_subscribed": true
    }
```

JSON response:

```json
    {
     "name": "Alice",
     "email": "alice@example.com",
     "age": 30,
     "is_subscribed": true
    }
```
