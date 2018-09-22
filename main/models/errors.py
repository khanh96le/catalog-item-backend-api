class UnauthorizedError(Exception):
    def __init__(self, error, status_code=401, description=None, headers=None):
        self.error = error
        self.description = description
        self.status_code = status_code
        self.headers = headers

    def __repr__(self):
        pass

    def __str__(self):
        pass