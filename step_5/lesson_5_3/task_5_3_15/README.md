# TASK DESCRIPTION

> Advanced programming task:
> This is an advanced task. It involves studying additional materials that will help you find a solution. Read the suggested sources, understand the new information, and try to apply it in practice.

We assume that you have completed the previous task and now your **FastAPI** project already has a `Product` model, for which you have performed a migration that creates a product table with the `id`, `title`, `price`, `count`, and `description` fields.

Your goal is to learn how to work with enumeration fields (**Enum**) and manually correct migrations that are “undercompensated” by autogeneration.

## Step 1. Adding an Enum field

### In the models file (models.py), add a new field:

```python
from enum import Enum as PyEnum
from sqlalchemy import Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase): # most likely you have it in database.py
pass

class ProductStatus(PyEnum):
DRAFT = "draft"
PUBLISHED = "published"
ARCHIVED = "archived"

class Product(Base):
# ... existing fields ...
status: Mapped[ProductStatus] = mapped_column(
Enum(ProductStatus, name="product_status"),
nullable=False,
server_default=ProductStatus.DRAFT.value
)
```

### Generate a new migration with the command

```bash
alembic revision --autogenerate -m "Add status enum to product"
```

### Check, change (create enum) and apply migration

```bash
alembic upgrade head
```

Make sure that the `product_status` type and the status column appear in the database schema.

## Step 2. Extending the enumeration and "manually" editing the migration

### Extend ProductStatus by adding a new value

```python
class ProductStatus(PyEnum):
DRAFT = "draft"
PUBLISHED = "published"
ARCHIVED = "archived"
DEPRECATED = "deprecated" # ← new value
```

### Try generating the migration

```bash
alembic revision --autogenerate -m "Extend product_status enum"
```

Note that **Alembic** did not add code to the script to update the **ENUM** type in **PostgreSQL** (or another server DBMS) - autogeneration still thinks that the type has not changed.

Open the created migration file and manually add **SQL** command blocks to **upgrade()** and **downgrade()**. Note that downgrade will be quite complex.

Apply the migration and make sure that you can set status=`'deprecated'` for existing records.

## Additional resources

**SQLAlchemy** Documentation — **Enum** Columns
Official guide to working with enums in models.
<https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Enum>

**Alembic** — Manual revision management
Section on autogenerating scripts.
<https://alembic.sqlalchemy.org/en/latest/autogenerate.html>

PGDoc: ALTER TYPE … ADD VALUE
Description of the **PostgreSQL** command for adding new variants to the **ENUM** type.
<https://www.postgresql.org/docs/current/sql-altertype.html>

We wish you success in completing the task!
