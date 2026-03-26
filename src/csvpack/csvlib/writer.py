from collections.abc import (
    Generator,
    Iterable,
)
from io import BufferedWriter
from typing import Any

from .csvcore import RustCsvWriter
from ..common.repr import csvlib_repr
from ..common.sizes import BUFFER_SIZE


class CSVWriter:
    """CSV dump writer."""

    fileobj: BufferedWriter | None
    metadata: list[dict[str, str]]
    delimiter: str
    quote_char: str
    encoding: str
    has_header: bool
    num_rows: int
    _chunk_size: int
    _buffer: bytearray
    _writer: RustCsvWriter

    def __init__(
        self,
        fileobj: BufferedWriter | None = None,
        metadata: list[dict[str, str]] | None = None,
        delimiter: str = ",",
        quote_char: str = '"',
        encoding: str = "utf-8",
        has_header: bool = True,
        chunk_size: int = BUFFER_SIZE,
    ) -> None:
        """Class initialization."""

        self.fileobj = fileobj
        self.delimiter = delimiter
        self.quote_char = quote_char
        self.encoding = encoding
        self.has_header = has_header
        self.metadata = metadata or []
        self.num_rows = 0
        self._chunk_size = chunk_size
        self._buffer = bytearray()
        self._writer = RustCsvWriter(
            metadata=self.metadata,
            has_header=self.has_header,
            delimiter=self.delimiter,
            quote_char=self.quote_char,
            encoding=self.encoding,
        )

    @property
    def columns(self) -> list[str]:
        """Get column list."""

        return [
            column
            for dct in self.metadata
            for column, _ in dct.items()
        ]

    @property
    def dtypes(self) -> list[str]:
        """Get data type list."""

        return [
            dtype
            for dct in self.metadata
            for _, dtype in dct.items()
        ]

    @property
    def num_columns(self) -> int:
        """Get number of columns."""

        return len(self.metadata)

    def write_row(
        self,
        row: list[Any] | tuple[Any, ...],
    ) -> Generator[bytes, None, None]:
        """Write single row."""

        yield self._writer.write_row(row, self.metadata)
        self.num_rows += 1

    def from_rows(
        self,
        rows: Iterable[list[Any] | tuple[Any, ...]],
    ) -> Generator[bytes, None, None]:
        """Write all rows."""

        for row in rows:
            self._buffer.extend(next(self.write_row(row)))

            if len(self._buffer) >= self._chunk_size:
                yield bytes(self._buffer[:self._chunk_size])
                self._buffer = self._buffer[self._chunk_size:]

        if self._buffer:
            yield bytes(self._buffer)
            self._buffer.clear()

    def write(
        self,
        rows: Iterable[list[Any] | tuple[Any, ...]],
    ) -> None:
        """Write all rows into file."""

        if self.fileobj is None:
            raise ValueError("File object not defined!")

        for chunk in self.from_rows(rows):
            self.fileobj.write(chunk)

    def tell(self) -> int:
        """Return current position."""

        return self._writer.tell()

    def close(self) -> None:
        """Close file object."""

        if self.fileobj and hasattr(self.fileobj, "close"):
            self.fileobj.close()

    def __repr__(self) -> str:
        """String representation of CSVWriter."""

        return csvlib_repr(
            self.columns,
            self.dtypes,
            self.num_columns,
            self.num_rows,
            "writer",
        )
