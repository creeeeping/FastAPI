class MovieModel:
    _data = []
    _id_counter = 1

    def __init__(self, title, playtime, genre):
        self.id = MovieModel._id_counter
        self.title = title
        self.playtime = playtime
        self.genre = genre

        MovieModel._data.append(self)
        MovieModel._id_counter += 1

    @classmethod
    def create(cls, title, playtime, genre):
        return cls(title, playtime, genre)

    @classmethod
    def all(cls):
        return cls._data

    @classmethod
    def get(cls, **kwargs):
        for movie in cls._data:
            if all(getattr(movie, key) == value for key, value in kwargs.items()):
                return movie
        return None

    @classmethod
    def filter(cls, **kwargs):
        result = []
        for movie in cls._data:
            match = True
            for key, value in kwargs.items():
                if key == "genre":
                    if value not in movie.genre:
                        match = False
                else:
                    if getattr(movie, key) != value:
                        match = False
            if match:
                result.append(movie)
        return result

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if value is not None:
                setattr(self, key, value)

    def delete(self):
        MovieModel._data.remove(self)
