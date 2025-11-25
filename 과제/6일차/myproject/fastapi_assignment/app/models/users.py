# app/models/users.py

from __future__ import annotations

import random
from typing import Any, ClassVar, List


class UserModel:
    """Simple in-memory user model for the assignment.

    This is not a real database, but it behaves similarly for demo/testing.
    """

    _data: ClassVar[List["UserModel"]] = []
    _id_counter: ClassVar[int] = 1

    def __init__(
        self,
        username: str,
        password: str,
        age: int,
        gender: str,
        profile_image_url: str | None = None,
    ) -> None:
        self.id = UserModel._id_counter
        UserModel._id_counter += 1

        self.username = username
        self.password = password
        self.age = age
        self.gender = gender
        self.profile_image_url = profile_image_url

        UserModel._data.append(self)

    # --------- CRUD-like helpers ---------
    @classmethod
    def create(
        cls,
        username: str,
        password: str,
        age: int,
        gender: str,
        profile_image_url: str | None = None,
    ) -> "UserModel":
        return cls(
            username=username,
            password=password,
            age=age,
            gender=gender,
            profile_image_url=profile_image_url,
        )

    @classmethod
    def get(cls, id: int) -> "UserModel" | None:
        return next((u for u in cls._data if u.id == id), None)

    @classmethod
    def all(cls) -> list["UserModel"]:
        return list(cls._data)

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel" | None:
        return next((u for u in cls._data if u.username == username), None)

    def update(self, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            if value is None:
                continue
            if hasattr(self, key):
                setattr(self, key, value)

    def delete(self) -> None:
        type(self)._data = [u for u in type(self)._data if u.id != self.id]

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "username": self.username,
            "age": self.age,
            "gender": self.gender,
            "profile_image_url": self.profile_image_url,
        }

    # --------- Utilities for seeding/clearing ---------
    @classmethod
    def clear(cls) -> None:
        cls._data = []
        cls._id_counter = 1

    @classmethod
    def create_dummy(cls) -> None:
        """Populate with some demo users."""
        cls.clear()
        for i in range(1, 6):
            cls.create(
                username=f"user{i}",
                password=f"password{i}",
                age=20 + i,
                gender=random.choice(["male", "female"]),
            )
