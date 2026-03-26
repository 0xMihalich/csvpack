from re import compile

from . import (
    dtype,
    ptype,
)


__DTYPE_PATTERN = compile(r"^(\w+)(?:\(([^)]*)\)|\[([^\]]*)\])?$")


def __find_ptype(
    dtype: str,
    associator: dict[str, str],
    is_none: bool = False,
) -> str:
    """Associate DType with csvlib data type."""

    match = __DTYPE_PATTERN.match(dtype)

    if not match:
        return ptype.STR

    parent_ptype = associator.get(match.group(1))
    child_dtype = match.group(2) or match.group(3)

    if parent_ptype is ptype.LIST:
        child_ptype = __find_ptype(child_dtype, associator, True)

        if not child_ptype:
            return parent_ptype

        return f"list[{child_ptype}]"

    if parent_ptype is ptype.NONTYPE:
        return __find_ptype(child_dtype, associator)

    if is_none:
        return parent_ptype

    return parent_ptype or ptype.STR


def from_dtypes(
    source: str,
    source_types: list[str],
) -> list[str]:
    """Associate dtypes with csvlib data types."""

    associator = dtype.__dict__.get(source.upper()) or {}
    return [
        __find_ptype(dtype, associator)
        for dtype in source_types
    ]
