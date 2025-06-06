# TASK DESCRIPTION

For this programming task, you need to implement request data validation and custom validation error handling in a **FastAPI** application.

**Requirements:**

1. Create a **FastAPI** application with at least one endpoint that accepts a **JSON** payload representing user data (e.g. `"name"`, `"age"`, `"e-mail"`, etc. as per the example below, or feel free to use your own example).

2. Define a **Pydantic** model for the user data to perform validation on the incoming **JSON** payload.

    ```python
    class User(BaseModel):
        username: str
        age: conint(gt=18)
        email: EmailStr
        password: constr(min_length=8, max_length=16)
        phone: Optional[str] = 'Unknown'
    ```

    A few comments to give you more background than we've covered so far:

    - In username - a **string check**, nothing fancy;

    - **conint** is an int with constraints (from "add constraints");

    - **gt=18** - greater than; read about other abbreviations in **FastAPI**;

    - **EmailStr** - checks if the string meets the requirements for email (or you can write your own regular expression);

    - **constr** - similar to the previous one, but a string with restrictions (length restrictions - minimum and maximum lengths are specified);

    - **Optional[str]** - the variable is of type str, but this is "optional". And also specified a default value.

3. Implement custom validation error handling with the `@app.exception_handler` decorator to provide informative error responses when validation fails.

4. Test the custom validation error handling by sending requests with invalid user data to the endpoint and ensuring that the error responses contain appropriate status codes and error messages.

> Note: You can use `fastapi.testclient.TestClient` to make test requests to your **FastAPI** application and check the responses (we'll cover this in the next block).
