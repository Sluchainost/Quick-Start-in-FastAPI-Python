"""This module defines enumerations for use with SQLAlchemy models.

Currently, it provides the ProductStatus enum, which represents the possible
states of a product in the system. This is intended for use as a field in
the Product ORM model and helps enforce valid product status values.
"""

import enum


class ProductStatus(str, enum.Enum):
    """
    Enumeration of possible product statuses.

    This enum is used to represent the state of a product in the database.
    The values are stored as strings for compatibility with SQLAlchemy and
    database storage.

    Members:
        DRAFT: The product is in draft state and not visible to customers.
        PUBLISHED: The product is published and visible to customers.
        ARCHIVED: The product is archived and no longer actively listed.
        DEPRECATED: The product is deprecated and should not be used or sold.
    """

    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"
    DEPRECATED = "DEPRECATED"
