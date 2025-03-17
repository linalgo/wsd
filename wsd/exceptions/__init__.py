"""Custom exception for handling document availability errors"""
class NoDocumentsAvailableException(Exception):
    """Exception raised when no documents are available."""

    def __init__(self, message="No documents are available."):
        self.message = message
        super().__init__(self.message)
