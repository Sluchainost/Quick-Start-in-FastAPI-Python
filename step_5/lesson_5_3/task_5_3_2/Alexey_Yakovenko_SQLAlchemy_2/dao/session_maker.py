"""
This module provides a decorator for managing asynchronous SQLAlchemy sessions
and transactions in a scientific and reusable manner.

Features:
- Automatic session creation and cleanup for each decorated function.
- Optional transaction isolation level control.
- Automatic commit/rollback logic based on function success or failure.
- Ensures that the session is always closed, preventing resource leaks.

Usage:
    @connection(isolation_level="SERIALIZABLE", commit=True)
    async def some_db_operation(..., session: AsyncSession):
        ...

This pattern ensures robust, reproducible, and maintainable database operations.
"""

from functools import wraps

from typing import Optional

from sqlalchemy import text

from .database import async_session_maker


def connection(isolation_level: Optional[str] = None, commit: bool = True):
    """
    Decorator factory for managing an asynchronous SQLAlchemy session and transaction.

    Args:
        isolation_level (Optional[str]): If provided, sets the transaction isolation level
            for the session (e.g., "SERIALIZABLE", "READ COMMITTED").
        commit (bool): If True, commits the transaction after the decorated function
            completes successfully. If False, no commit is performed.

    Returns:
        Callable: A decorator that wraps an async function, injecting a managed session.

    The decorated function must accept a 'session' keyword argument of type AsyncSession.
    """

    def decorator(method):
        """
        Decorator that wraps an async function to provide session management.

        Args:
            method (Callable): The async function to wrap. Must accept 'session' as a kwarg.

        Returns:
            Callable: The wrapped async function with session management.
        """

        @wraps(method)
        async def wrapper(*args, **kwargs):
            """
            Wrapper that manages session lifecycle, transaction isolation, and commit/rollback.

            - Creates a new async session for each call.
            - Optionally sets the transaction isolation level.
            - Commits if 'commit' is True and the function succeeds.
            - Rolls back on exception.
            - Always closes the session at the end.
            """

            async with async_session_maker() as session:
                try:
                    # Optionally set the transaction isolation level for this session.
                    if isolation_level:
                        await session.execute(
                            text(
                                f"SET TRANSACTION ISOLATION LEVEL {isolation_level}"
                            )
                        )

                    # Inject the session into the decorated function.
                    result = await method(*args, session=session, **kwargs)

                    # Commit the transaction if requested.
                    if commit:
                        await session.commit()

                    return result
                except Exception as e:
                    # Roll back the transaction on any exception.
                    await session.rollback()
                    raise e
                finally:
                    # Ensure the session is always closed to free resources.
                    await session.close()

        return wrapper

    return decorator
