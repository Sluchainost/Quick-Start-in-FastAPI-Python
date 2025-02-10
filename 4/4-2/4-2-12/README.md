# TASK DESCRIPTION

For this programming task, you need to implement **JWT-based** authentication in a **FastAPI** application. Use the `PyJWT` library to generate and validate tokens.
Requirements:

1. Create a **FastAPI** `/login` endpoint that accepts **POST** requests with a **JSON** payload containing *user_name* and *password* fields. The endpoint must authenticate the user based on the provided credentials.
2. If the credentials are valid, generate a **JWT** token with an appropriate expiration date and return it in the response.
3. If the credentials are invalid, return an appropriate error response.
4. Create a protected **FastAPI** `/protected_resource` endpoint that requires authentication using **JWT**. Users must include the generated token in the `Authorization` header of their requests to access this endpoint.
5. Check the **JWT** token in the `Authorization` header for each request to `/protected_resource`. If the token is valid, allow access to the endpoint and return a response indicating successful access.
6. If the token is invalid, expired, or missing, return an appropriate error response.

>Note: You can hypothetically assume the existence of a function `authenticate_user(username: str, password: str) -> bool` that checks the provided "*username*" and "*password*" against the user database and returns `True` if the credentials are valid and `False` otherwise (or stub such a function that returns True or False using the *random.choice* module).*

## Sample request

    POST /login
    Content-Type: application/json

```json
    {
    "username": "john_doe",
    "password": "securepassword123"
    }
```

## Sample response (200 OK)

```json
    {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    }
```

## Response example (401 Unauthorized)

```json
    {
    "detail": "Invalid credentials"
    }
```

>**!!!! Note: Since this is a simplified programming task, it is extremely important to take additional security measures and follow best practices for real applications. Also, token handling, refresh mechanisms, and token revocation are important aspects to consider when creating a production-ready authentication system !!!!**
