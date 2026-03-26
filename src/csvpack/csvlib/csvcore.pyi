
from io import BufferedReader
from typing import Any


class RustCsvReader:
    """High-performance CSV reader with buffering (8KB).
    Returns rows as tuples. Implements Python iterator protocol."""

    def __init__(
        self,
        fileobj: BufferedReader,
        metadata: dict[str, str] | None = None,
        has_header: bool = True,
        delimiter: str = ",",
        quote_char: str = '"',
        encoding: str = "utf-8",
    ) -> None:
        """Class initialization."""
        ...

    def __iter__(self) -> "RustCsvReader":
        """Return self as iterator."""
        ...

    def __next__(self) -> tuple[Any, ...] | None:
        """Return next row as tuple, or None if EOF.

        Returns:
            Tuple of values with types converted according to metadata,
            or None if no more rows."""
        ...

    def tell(self) -> int:
        """Return current position in the file.

        Returns:
            Current file position in bytes (accounts for buffered data)."""
        ...

    def close(self) -> None:
        """Close the underlying file object."""
        ...

    def get_headers(self) -> list[str]:
        """Get column names from header row.

        Returns:
            List of column names if has_header=True, otherwise empty list."""
        ...

    def row_count(self) -> int:
        """Get number of rows read so far.

        Returns:
            Number of rows returned by __next__ (excluding header)."""
        ...


class RustCsvWriter:
    """High-performance CSV writer that returns bytes for each row.
    Does NOT write to file directly."""

    def __init__(
        self,
        metadata: dict[str, str] | None = None,
        has_header: bool = True,
        delimiter: str = ",",
        quote_char: str = '"',
        encoding: str = "utf-8",
    ) -> None:
        """Class initialization."""
        ...

    def write_row(self, row: tuple[Any, ...]) -> bytes:
        """Convert a single row to CSV bytes."""
        ...

    def tell(self) -> int:
        """Return total bytes written across all rows."""
        ...
