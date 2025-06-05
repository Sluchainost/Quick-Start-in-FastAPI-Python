# TASK DESCRIPTION

This programming task requires you to implement custom error handling in a **FastAPI** application. Your application must include custom *exception classes*, *exception handlers*, and *error response models*.

**Requirements:**

1. Create a **FastAPI** application and configure custom exception classes for at least two specific exceptions (e.g. `CustomExceptionA` and `CustomExceptionB`). Each custom exception must have a unique status code and a custom error message.

2. Register custom exception handlers for the two custom exceptions. The exception handlers must return error responses with appropriate status codes and error messages.

3. Define error response models using **Pydantic** models to ensure consistent formatting of error responses across the application.

4. Implement at least two **API** endpoints that raise custom exceptions in specific scenarios. For example, one endpoint might throw `CustomExceptionA` when a certain condition is not met, while another endpoint might throw `CustomExceptionB` when a resource is not found.

5. Test your custom error handling by sending requests to the **API** endpoints that throw custom exceptions. Make sure that the error responses contain the correct status codes and error messages.

> Note: For this task, you can use simple print statements to log errors. In a real-world scenario, you would typically use a **logging** library to handle error **logging** efficiently.
