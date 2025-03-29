# TASK DESCRIPTION

For this programming task, you need to integrate **FastAPI** with a database and perform basic **CRUD** operations on a specific resource.

## Requirements

1. Select any supported database (e.g. **SQLite**, **PostgreSQL**, **MySQL** or **MongoDB**) and install the required database driver for **FastAPI** (it is recommended to choose the one that is most likely to work with in the future, or the one that you do not yet know how to work with).

2. Create a data model (schema) for a simple resource (e.g. a Todo item) that includes fields such as *id*, *title*, *description*, and *completed*.

3. Implement a **FastAPI** endpoint to create a new Todo item. The endpoint should accept a **JSON** payload containing the *title* and *description* fields via a **POST** request. Upon successful creation, return the created Todo item in the response (by default, the completed status of a new item is False).

4. Implement a **FastAPI** endpoint to retrieve a single Todo item based on its id. The endpoint should return a matching Todo item on a **GET** request if found, or a matching error response if the item does not exist.

5. Implement a **FastAPI** endpoint to update an existing Todo item on based on its *"id"*. The endpoint should accept a **JSON** payload (**PUT**/**POST** request) containing *"title"*, *"description"*, and *"completed"* fields. Update the corresponding "Todo" item in the database and return the updated item in the response.

6. Implement a **FastAPI** endpoint to delete a "Todo" item based on its *"id"*. If the item is successfully deleted, return a success message in the response.

Example of **POST** request create (Create Todo):

```markdown
POST /todos
Content-Type: application/json
```

```json
{
"title": "Buy groceries",
"description": "Milk, eggs, bread"
}
```

Example response (201 Created):

```json
{
"id": 1,
"title": "Buy groceries",
"description": "Milk, eggs, bread",
"completed": false
}
```

Example of **GET** request read (Get Todo - ID: 1):

```markdown
GET /todos/1
```

Example response (200 OK):

```json
{
"id": 1,
"title": "Buy groceries",
"description": "Milk, eggs, bread",
"completed": false
}
```
