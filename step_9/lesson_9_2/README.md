# Introduction to Creating a SQLAlchemy Project with PostgreSQL

In the world of database management, the combination of **SQLAlchemy** and **PostgreSQL** stands out for its power, flexibility, and efficiency. **SQLAlchemy**, a powerful SQL toolkit and *object-relational mapping* (**ORM**) library, integrates seamlessly with **PostgreSQL**, a robust open-source relational database management system.

## Alembic

**Alembic** is a lightweight database migration tool for use with **SQLAlchemy**. It provides a simple and effective way to manage database schema changes over time.

### Key Features

1. Version Control:

    - Tracks changes to your database schema, allowing you to apply and revert migrations as needed.

2. Migration Scripts:

    - Generates migration scripts automatically based on changes in your **SQLAlchemy** models.

3. Database Support:

    - Works with multiple database backends, including **PostgreSQL**, **MySQL**, **SQLite**, and others.

4. Flexible Migration Operations:

    - Supports a wide range of migration operations, such as *adding/removing* tables, columns, and constraints.

5. Command-Line Interface:

    - Provides a command-line interface for creating, applying, and managing migrations easily.

6. Integration with **SQLAlchemy**:

    - Seamlessly integrates with **SQLAlchemy**, making it easy to use in projects that already utilize this **ORM**.

### Basic Workflow

1. Install **Alembic**:

    ```bash
        pip install alembic
    ```

2. Initialize a Migration Environment:

    ```bash
        alembic init alembic
    ```

3. Create a Migration Script:

    ```bash
        alembic revision --autogenerate -m "Migration message"
    ```

4. Apply Migrations:

    ```bash
        alembic upgrade head
    ```

5. Revert Migrations:

    ```bash
        alembic downgrade <revision>
    ```

### Conclusion for Alembic

**Alembic** is an essential tool for managing database migrations in **SQLAlchemy**-based applications, making it easier to maintain and evolve your database schema over time.

## Working with the database through a separate layer (repository pattern / DAO pattern)

The next logical step in developing database interactions through an application is to move database interactions into a separate layer.

The **Repository pattern**, also known as the **DAO** (*data access object*) pattern, is a design pattern that abstracts data access logic from the rest of the application. This separation provides a clean and modular architecture that makes it easier to manage database interactions and switch between different data store implementations without affecting the higher-level application logic.

> P.S. Some may disagree that these are the same patterns, but it is more important to understand the concept.

### Key concepts

1. **Separation of concerns:**

    Without the **Repository pattern**:

    - Data access logic is scattered throughout the application. 🔴
    - Changes to the database schema may require updating the entire code base. 🔴

    With the **Repository pattern**:

    - Data access logic is centralized in a repository, isolated from the rest of the application. 🟢
    - Changes to the database schema affect only the repository, minimizing the impact on the application. 🟢

2. **Abstraction:**

    Without the **Repository pattern**:

    - Application code interacts directly with database-specific APIs. 🔴

    With the **Repository pattern**:

    - Application code interacts with the high-level interface of the repository. 🟢

    - The repository handles the database-specific details. 🟢

3. **Flexibility:**

    Without the **Repository pattern**:

    - Switching to a different database requires changes to the entire application. 🔴

    With the **Repository pattern**:

    - Switching databases involves updating only the repository implementation. 🟢

In general, this is a fairly common example of working with a database. But it has a couple of drawbacks:

- if there are several models in the **DB**, a situation may arise where changes in one model should lead to changes in another model. For example, an order and its processing status. When an order is created, a new record is added to the database, and then you need to create a record in the "status" model, in which you specify at what stage the order is, who is the executor for this status, the completion date of the stage, and something like that. With the **repository pattern**, we would have alternately called methods in two models, and if any of the actions caused an error, then it would not be very convenient for us to delete the record added to the **DB**. You can significantly complicate the architecture in the future - then add an order archive, a status archive, and so on... You can imagine how the probability of an error in **saving/changing/deleting** some part of the **DB** increases, which should lead to cancellation in the code...
- each route for each request receives a new session object for working with the database at the factory. Since the session objects are different, a conflict (**data inconsistency**) may arise in the database: one thread has already updated the data, and the second is still working with the old data and then enters the "updated" old data - that is, inconsistent commits.

Unit of Work pattern can eliminate these shortcomings

## Working with the Database through Its Own Asynchronous Context Manager (Unit of Work Pattern) via Services (Controllers)

### Overview of the Unit of Work Pattern

The **Unit of Work** (**UoW**) pattern is a design pattern that maintains a list of objects affected by a business transaction and coordinates the writing out of changes and the resolution of concurrency problems. It acts as a bridge between the domain and data mapping layers, ensuring that all changes to the database are made in a single transaction.

### Key Concepts

1. **Asynchronous Context Manager**:
   - An asynchronous context manager allows you to manage resources (like database connections) in an asynchronous manner. This is especially useful in web applications where non-blocking **I/O operations** are crucial for performance.

2. **Services (Controllers)**:
   - Services or controllers encapsulate the business logic of your application. They interact with the **Unit of Work** to perform operations on the database while maintaining clear separation of concerns.

### How It Works

#### 1. Structure

- **Unit of Work Class**:
  - Manages the database session and tracks changes to entities.
  
- **Service Layer**:
  - Contains business logic and interacts with the Unit of Work to perform operations.

#### 2. Implementation Steps

1. **Define the Unit of Work Class**:
   - This class will manage the database session and provide methods to commit or rollback transactions.

   ```python
   from sqlalchemy.ext.asyncio import AsyncSession
   from sqlalchemy.orm import sessionmaker

   class UnitOfWork:
       def __init__(self, session_factory: sessionmaker):
           self.session_factory = session_factory
           self.session: AsyncSession = None

       async def __aenter__(self):
           self.session = self.session_factory()
           return self

       async def __aexit__(self, exc_type, exc_value, traceback):
           if exc_type:
               await self.session.rollback()
           else:
               await self.session.commit()
           await self.session.close()
   ```

2. **Create a Service Layer**:
   - This layer uses the **Unit of Work** to perform operations. It should not directly interact with the database but rather through the **UoW**.

   ```python
   class UserService:
       def __init__(self, uow: UnitOfWork):
           self.uow = uow

       async def create_user(self, user_data):
           async with self.uow as uow:
               user = User(**user_data)
               uow.session.add(user)
               # More business logic can be added here
   ```

3. **Using the Service in Your Application**:
   - In your application, you can use the service layer to perform operations while ensuring that the database interactions are properly managed.

   ```python
   async def create_new_user(user_data):
       async with UnitOfWork(session_factory) as uow:
           user_service = UserService(uow)
           await user_service.create_user(user_data)
   ```

### Benefits of Using the Unit of Work Pattern

- **Transaction Management**:
  - Ensures that all changes are committed or rolled back together, maintaining data integrity.

- **Separation of Concerns**:
  - Business logic is separated from data access logic, making the codebase cleaner and easier to maintain.

- **Improved Performance**:
  - Reduces the number of database calls by batching operations, which can significantly enhance performance in high-load scenarios.

- **Asynchronous Support**:
  - By leveraging asynchronous context managers, the application can handle multiple requests efficiently without blocking.

### Conclusion for Unit of Work

The **Unit of Work** pattern, when implemented with an asynchronous context manager and service layer, provides a robust architecture for managing database interactions in a clean and efficient manner. This design not only enhances maintainability but also ensures that your application can scale effectively.
