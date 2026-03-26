class CSVPackError(Exception):
    """Base CSVPack error."""


class CSVPackValueError(CSVPackError, ValueError):
    """CSVPack value error."""


class CSVPackTypeError(CSVPackError, TypeError):
    """CSVPack type error."""


class CSVPackHeaderError(CSVPackValueError):
    """Error header signature."""


class CSVPackMetadataError(CSVPackValueError):
    """Error metadata."""


class CSVPackMetadataCrcError(CSVPackMetadataError):
    """Error metadata crc32."""


class CSVPackModeError(CSVPackTypeError):
    """Error fileobject mode."""
