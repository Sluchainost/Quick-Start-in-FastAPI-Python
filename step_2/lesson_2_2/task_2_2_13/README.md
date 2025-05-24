# TASK DESCRIPTION

1. Define a model named `User` in Pydantic's *models.py* file with the following fields:

    - `name` (str)

    - `id` (int)

2. Import the *models.py* module into the *main* application file and create an instance of the User class in it, with the corresponding fields of the `User` model:

    - `name`: "John Doe"

    - `id`: 1

3. Implement a function that, when receiving a **GET** request via the additional `/users` route, would return **JSON** with user data.
