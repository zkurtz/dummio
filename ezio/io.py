"""Tools to read and write multiple data objects using a single file path."""

import os
import tempfile
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from types import TracebackType
from typing import Any, Callable, Type


@dataclass
class ArchiveWriter:
    """Manage addition of files to zipfile archive.

    Args:
        tempdir: Temporary directory to write files to.
        writer: Callable to copy files from tempdir into the archive.
        filenames: List of filenames to add to the archive.
    """

    tempdir: Path
    writer: Callable[[str, Any], None]
    filenames: set[str] = field(default_factory=set)

    def __post_init__(self) -> None:
        """Validate inputs."""
        if not self.tempdir.is_dir():
            raise NotADirectoryError(f"Temporary directory {self.tempdir} does not exist.")
        if self.filenames:
            raise ValueError("Do not pass in filenames. This list gets constructed with successive calls of self.file.")

    def file(self, filename: str) -> Path:
        """Declare a file name to add to the archive, and return a temp path to write to."""
        if filename in self.filenames:
            raise ValueError(f"Filename {filename} was already declared.")
        self.filenames.add(filename)
        return self.tempdir / filename

    def zip_files(self, **kwargs: Any) -> None:
        """Write all files to the zip archive.

        Args:
            **kwargs: Additional keyword arguments to pass in to zipfile.ZipFile.write.
        """
        for filename in self.filenames:
            fullpath = os.path.join(self.tempdir, filename)
            if not Path(fullpath).is_file():
                raise FileNotFoundError(f"No file found for writer.file('{filename}'); you must write to the file.")
            self.writer(fullpath, arcname=filename, **kwargs)  # pyright: ignore[reportCallIssue]


class Writer:
    """Context manager to write multiple objects to the same file."""

    def __init__(self, path: Path) -> None:
        """Initialize the reader with a file path."""
        self.path = path

    def __enter__(self) -> ArchiveWriter:
        """Create temporary directory and zip object, return callable."""
        self.tempdir = tempfile.TemporaryDirectory()
        self.zipf = zipfile.ZipFile(self.path, "w")
        self.writer = ArchiveWriter(
            tempdir=Path(self.tempdir.name),
            writer=self.zipf.write,
        )
        return self.writer

    def __exit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Exit the context manager."""
        self.writer.zip_files()
        self.zipf.close()
        self.tempdir.cleanup()


class Reader:
    """Context manager to read multiple objects from the same file."""

    def __init__(self, path: Path) -> None:
        """Initialize zipfile with a file path."""
        self.path = path

    def __enter__(self) -> "Reader":
        """Create temporary directory and zip object, return callable."""
        self.tempdir = tempfile.TemporaryDirectory()
        self.zipf = zipfile.ZipFile(self.path, "r")
        return self

    def file(self, filename: str) -> Path:
        """Unzip the file to a temporary path and return that path."""
        self.zipf.extract(filename, path=self.tempdir.name)
        return Path(self.tempdir.name) / filename

    def __exit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Exit the context manager."""
        self.zipf.close()
        self.tempdir.cleanup()
