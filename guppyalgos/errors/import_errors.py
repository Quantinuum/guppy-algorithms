"""Module containing custom exceptions for import errors."""


class NumbaImportError(ImportError):
    """Custom ImportError to indicate that numba is not installed.

    This error is raised when attempting to use functionality that depends on
    numba and if it is not available in the current environment.
    """

    def __init__(self, feature_name: str):
        """Initialize the NumbaImportError.

        Args:
            feature_name: The name of the feature that requires numba.

        """
        super().__init__(
            f"numba is required for {feature_name}. "
            "Please install numba to use this functionality."
        )
