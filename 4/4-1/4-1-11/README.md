# TASK DESCRIPTION

Implement a **Basic Authentication-protected FastAPI** `/login` endpoint that accepts **GET** requests.

1. The endpoint should **authenticate** the user based on the provided credentials.

2. Use a dependency to check if the username and password are correct.

3. If the credentials are incorrect, return an **HTTPException** with a **401** status code (the same is returned if the credentials are not provided).

4. If the credentials are correct, return a secret message `"You got my secret, welcome"`

5. Try logging in with the incorrect credentials first, and then enter the correct credentials. To achieve this (re-login), see the information about the need to add the **WWW-Authenticate** header so that the browser displays the login prompt again.
