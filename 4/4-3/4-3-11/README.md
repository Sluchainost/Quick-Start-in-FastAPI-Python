# TASK DESCRIPTION

For this programming task, you need to implement **role-based access control** in a **FastAPI** application. Let's assume that **JWT**-based authentication is already implemented and users are assigned roles during the registration process.

Requirements:

1. Create at least three roles: `admin`, `user`, `guest`. Define the appropriate permissions for each role. For example, `admin` can have full **CRUD** permissions, while `user` can *read* and *update* resources and `guest` has limited *read-only* access.

2. Implement role-based authorization for your **FastAPI** endpoints. Use dependency injection or decorator-based authorization to check the user's role before allowing access to certain endpoints.

3. Create a **FastAPI** endpoint `/protected_resource` that requires authentication. Ensure that only users with the appropriate role (e.g. `admin` or `user`) can access this endpoint.

4. For each role, create specific **API** endpoints that demonstrate the permissions of that role. For example, the `admin` role might have an endpoint to create a resource, while the `user` role can only read and update existing resources.

5. Test your **RBAC** implementation by sending requests to different endpoints with different user roles. Ensure that access is appropriately restricted based on the user's role.

> **Note:** For this task, you can use Python dictionaries or a simple in-memory data store to store roles and their associated permissions. In a real-world scenario, you would typically integrate **RBAC** with your application's database.
