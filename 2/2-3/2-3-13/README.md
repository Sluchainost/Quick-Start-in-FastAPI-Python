# TASK DESCRIPTION

Extend the existing FastAPI application by creating a **POST** endpoint that allows users to submit feedback. The endpoint should accept **JSON** data containing the user *name* and the feedback *message*.

1. Define a **Pydantic** model named "Feedback" with the following fields:
    - `name` (str)
    - `message` (str)

2. Create a new **post** route `/feedback` that accepts **JSON** data according to the `Feedback` model.

3. Implement a function to handle the incoming feedback data and respond with a success *message*.

4. Store the feedback data in a list or data store to keep track of all the feedback received.

Example:

**JSON** Request:

```json
    {
    "name": "Alice",
    "message": "Great course! I'm learning a lot."
    }
```

**JSON** Response:

```json
    {
    "message": "Feedback received. Thank you, Alice!"
    }
```
