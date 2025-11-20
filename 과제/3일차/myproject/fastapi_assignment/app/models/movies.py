# app/models/movies.py

from __future__ import annotations

from typing import Any, List


class MovieModel:
    _data: List["MovieModel"] = []
    _id_counter: int = 1

    def __init__(self, title: str, playtime: int, genre: list[str]) -> None:
        self.id = MovieModel._id_counter
        MovieModel._id_counter += 1

        self.title = title
        self.playtime = playtime
        self.genre = genre

        MovieModel._data.append(self)

    @classmethod
    def create(cls, title: str, playtime: int, genre: list[str]) -> "MovieModel":
        return cls(title=title, playtime=playtime, genre=genre)

    @classmethod
    def get(cls, **kwargs: Any) -> "MovieModel | None":
        for movie in cls._data:
            if all(getattr(movie, key) == value for key, value in kwargs.items()):
                return movie
        return None

    @classmethod
    def filter(cls, **kwargs: Any) -> list["MovieModel"]:
        result: list["MovieModel"] = []
        for movie in cls._data:
            matched = True
            for key, value in kwargs.items():
                if getattr(movie, key) != value:
                    matched = False
                    break
            if matched:
                result.append(movie)
        return result

    def update(self, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            if value is not None and hasattr(self, key):
                setattr(self, key, value)

    def delete(self) -> None:
        if self in MovieModel._data:
            MovieModel._data.remove(self)

    @classmethod
    def all(cls) -> list["MovieModel"]:
        return cls._data

    @classmethod
    def clear(cls) -> None:
        cls._data = []

    @classmethod
    def create_dummy(cls) -> None:
        cls(title="Inception", playtime=148, genre=["sci-fi", "action"])
        cls(title="Interstellar", playtime=169, genre=["sci-fi", "drama"])
        cls(title="The Dark Knight", playtime=152, genre=["action"])
