# TASK DESCRIPTION

Your task is to extend the existing FastAPI application by adding a new **POST** endpoint that accepts **JSON** data representing a user and returns the same data with an additional field indicating whether the user is an adult or not.

1. Define a Pydantic model named "User" with the following fields:

    - `name` (str)

    - `age` (int)

2. Create a new route `/user` that accepts **POST** requests and accepts a **JSON** payload containing user data corresponding to the `User` model.

3. Implement a function to check whether the user is an adult (*age* >= 18) or a minor (*age* < 18).

4. Return the user data along with an additional `is_adult` field in the **JSON** response indicating whether the user is an adult (*True*) or a minor (*False*).

## Example

Request in **JSON** format:

```json
    {
    "name": "John Doe",
    "age": 25
    }
```

Response in **JSON** format:

```json
    {
    "name": "John Doe",
    "age": 25,
    "is_adult": true
    }
```
