"""
This module defines enumerations (enums) for use in SQLAlchemy models and Pydantic schemas.
Enums provide type safety, semantic clarity, and reproducibility for categorical fields
in the scientific project.

Enumerations:
    - GenderEnum: Biological gender categories.
    - StatusPost: Publication status of posts.
    - RatingEnum: Integer-based rating scale (1–10).
    - ProfessionEnum: Standardized list of professions.
"""

import enum


class GenderEnum(str, enum.Enum):
    """
    Enumeration of biological gender categories.

    Values:
        MALE: Represents male gender.
        FEMALE: Represents female gender.
    """

    MALE = "male"
    FEMALE = "female"


class StatusPost(str, enum.Enum):
    """
    Enumeration of possible publication statuses for a post.

    Values:
        PUBLISHED: The post is publicly visible.
        DELETED: The post has been removed.
        UNDER_MODERATION: The post is pending review.
        DRAFT: The post is saved as a draft and not published.
        SCHEDULED: The post is scheduled for future publication.
    """

    PUBLISHED = "published"
    DELETED = "deleted"
    UNDER_MODERATION = "under_moderation"
    DRAFT = "draft"
    SCHEDULED = "scheduled"


class RatingEnum(int, enum.Enum):
    """
    Enumeration for rating values on a 1–10 integer scale.

    Values:
        ONE to TEN: Integer ratings from 1 (lowest) to 10 (highest).
    """

    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10


class ProfessionEnum(str, enum.Enum):
    """
    Enumeration of standardized professions for user profiles.

    Values:
        DEVELOPER: Software developer or engineer.
        DESIGNER: Graphic or UI/UX designer.
        MANAGER: Project or team manager.
        TEACHER: Educator or instructor.
        DOCTOR: Medical doctor.
        ENGINEER: Non-software engineer (e.g., civil, mechanical).
        MARKETER: Marketing professional.
        WRITER: Author, journalist, or content creator.
        ARTIST: Visual or performing artist.
        LAWYER: Legal professional.
        SCIENTIST: Researcher or scientist.
        NURSE: Nursing professional.
        UNEMPLOYED: Not currently employed.
    """

    DEVELOPER = "developer"
    DESIGNER = "designer"
    MANAGER = "manager"
    TEACHER = "teacher"
    DOCTOR = "doctor"
    ENGINEER = "engineer"
    MARKETER = "marketer"
    WRITER = "writer"
    ARTIST = "artist"
    LAWYER = "lawyer"
    SCIENTIST = "scientist"
    NURSE = "nurse"
    UNEMPLOYED = "unemployed"
