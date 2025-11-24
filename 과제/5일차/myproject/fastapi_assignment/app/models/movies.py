# app/models/movies.py

from __future__ import annotations

from typing import Any, ClassVar, List


class MovieModel:
    """Simple in-memory movie model for the assignment."""

    _data: ClassVar[List["MovieModel"]] = []
    _id_counter: ClassVar[int] = 1

    def __init__(
        self,
        title: str,
        playtime: int,
        genre: list[str],
        poster_image_url: str | None = None,
    ) -> None:
        self.id = MovieModel._id_counter
        MovieModel._id_counter += 1

        self.title = title
        self.playtime = playtime
        self.genre = genre
        self.poster_image_url = poster_image_url

        MovieModel._data.append(self)

    @classmethod
    def create(
        cls,
        title: str,
        playtime: int,
        genre: list[str],
        poster_image_url: str | None = None,
    ) -> "MovieModel":
        return cls(
            title=title,
            playtime=playtime,
            genre=genre,
            poster_image_url=poster_image_url,
        )

    @classmethod
    def get(cls, id: int) -> "MovieModel" | None:
        return next((m for m in cls._data if m.id == id), None)

    @classmethod
    def all(cls) -> list["MovieModel"]:
        return list(cls._data)

    def update(self, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            if value is None:
                continue
            if hasattr(self, key):
                setattr(self, key, value)

    def delete(self) -> None:
        type(self)._data = [m for m in type(self)._data if m.id != self.id]

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "playtime": self.playtime,
            "genre": self.genre,
            "poster_image_url": self.poster_image_url,
        }

    @classmethod
    def clear(cls) -> None:
        cls._data = []
        cls._id_counter = 1

    @classmethod
    def create_dummy(cls) -> None:
        cls.clear()
        cls.create(title="Inception", playtime=148, genre=["sci-fi", "action"])
        cls.create(title="Interstellar", playtime=169, genre=["sci-fi", "drama"])
        cls.create(title="The Dark Knight", playtime=152, genre=["action"])
