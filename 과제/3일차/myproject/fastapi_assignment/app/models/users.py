# app/models/users.py

from __future__ import annotations

import random
from typing import Any


class UserModel:
    _data: list["UserModel"] = []
    _id_counter: int = 1

    def __init__(self, username: str, password: str, age: int, gender: str) -> None:
        self.id = UserModel._id_counter
        UserModel._id_counter += 1

        self.username = username
        self.password = password  # 지금 단계는 비밀번호 해시 X
        self.age = age
        self.gender = gender
        self.last_login = None

        UserModel._data.append(self)

    @classmethod
    def create(cls, username: str, password: str, age: int, gender: str) -> "UserModel":
        return cls(username=username, password=password, age=age, gender=gender)

    @classmethod
    def get(cls, **kwargs: Any) -> "UserModel | None":
        for user in cls._data:
            if all(getattr(user, key) == value for key, value in kwargs.items()):
                return user
        return None

    @classmethod
    def filter(cls, **kwargs: Any) -> list["UserModel"]:
        result: list["UserModel"] = []
        for user in cls._data:
            matched = True
            for key, value in kwargs.items():
                if getattr(user, key) != value:
                    matched = False
                    break
            if matched:
                result.append(user)
        return result

    def update(self, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            if value is not None and hasattr(self, key):
                setattr(self, key, value)

    def delete(self) -> None:
        if self in UserModel._data:
            UserModel._data.remove(self)

    @classmethod
    def all(cls) -> list["UserModel"]:
        return cls._data

    @classmethod
    def clear(cls) -> None:
        cls._data = []

    @classmethod
    def create_dummy(cls) -> None:
        for i in range(1, 6):
            cls(
                username=f"user{i}",
                password=f"password{i}",
                age=20 + i,
                gender=random.choice(["male", "female"]),
            )
