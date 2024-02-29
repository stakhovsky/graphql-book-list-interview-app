import importlib_metadata


__app__ = "graphql-book-list-interview-app"
try:
    __version__ = importlib_metadata.version(__app__)
except importlib_metadata.PackageNotFoundError:
    __version__ = "0.0.0"
