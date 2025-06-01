# TASK DESCRIPTION

> This is a basic level assignment. It is intended to reinforce the lecture material and does not require any additional study. Simply apply what you have learned in practice.

To complete this programming task, you will configure **Alembic** to migrate the database in a **FastAPI** application and create a simple migration to change the database schema.

Prerequisites:

1. Install **Alembic** and the required database driver for your chosen database (e.g. SQLite, **PostgreSQL**, MySQL).

2. Set up **Alembic** by initializing it in your **FastAPI** project and configuring it to match your database settings.

3. Create a data model (**SQLAlchemy** model) representing a resource (e.g. a `"Product"` object) with fields such as `"id"`, `"title"`, `"price"`, and `"count"`.

4. Generate an initial migration script using **Alembic** that creates a new table for the `"Product"` object.

5. Apply the initial migration to the database and verify that the `Product` table is created. After that, add two records to the table.

6. Change the data model by adding a new field, for example, `"description"`, to the `"Product"` entity. description should be not null.

7. Generate a new migration script using **Alembic** that reflects the changes to the `"Product"` entity.

8. Apply the new migration to the database and verify that the `"Product"` table now contains the `"description"` field.

> Note: Database migration is an important aspect of database schema change management in real-world applications. This task provides a simplified scenario, and in a production environment you should follow additional best practices, handle data migration, and consider possible data loss scenarios. If you are more comfortable working in a different technology stack, then explore the possibility of performing the task (database migration) in a way that is appropriate for you.
