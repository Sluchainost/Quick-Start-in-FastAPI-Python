# TASK DESCRIPTION

Your task is to create a **FastAPI** application that implements cookie-based authentication. Follow these steps:

1. Create a simple login route at `/login` that accepts a username and password as form data. If the credentials are valid, set a secure **HTTP-only** cookie named `session_token` with a unique value.

2. Implement a secure route at `/user` that requires authentication using the `session_token` cookie. If the cookie is valid and contains the correct authentication data, return a **JSON** response with the user profile information.

3. If the `session_token` cookie is missing or invalid, the `/user` route should return an error response with a 401 (*Unauthorized*) status code or a `{"message": "Unauthorized"}` message.

## Example

**POST** request to `/login` with form data:

```json
    {
    "username": "user123",
    "password": "password123"
    }
```

The response must contain the `session_token` cookie.

**GET** request to `/user` with the `session_token` cookie:

```json
    session_token: "abc123xyz456"
```

The response must return user profile information.

**GET** request to `/user` without the `session_token` cookie or with an invalid cookie, for example:

```json
    session_token: "invalid_token_value"
```

The response must return an error message with the 401 status code or the message `{"message": "Unauthorized"}`.
