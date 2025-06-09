# TASK DESCRIPTION

For this programming task, you need to implement custom error responses in your **FastAPI** application to provide more useful and informative feedback to your users.

**Requirements:**

1. Create a **FastAPI** application with at least two endpoints that perform different tasks (e.g. one endpoint handles user registration, and the other endpoint retrieves user data).

2. Define custom error response models using **Pydantic** for common types of errors that may occur in your application (e.g. `ErrorResponseModel` with fields for `status_code`, `message`, and `error_code`).

3. Implement custom exception classes for specific scenarios (e.g. `UserNotFoundException`, `InvalidUserDataException`) that throw appropriate **HTTPExceptions** with status codes and custom error messages.

4. Add a custom `"X-ErrorHandleTime"` header that indicates the *time it took to handle the error*, *internationalize error responses* (second optional).

5. Create custom exception handlers using the `@app.exception_handler` decorator to catch and handle custom exceptions. Handlers should generate custom error responses using the defined response models.

6. Test custom error responses by sending requests to endpoints with invalid data or non-existent resources. Ensure that error responses contain the expected status codes, error messages, and error code codes.

**Summary:**

After completing the task, you should have a **FastAPI** application that provides custom error responses for different exception types. When users encounter errors, they should receive informative error messages that enhance their understanding of the problem and improve the overall user experience.
