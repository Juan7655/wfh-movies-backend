class HeyMovieError(AssertionError):
    pass


class InvalidParameter(HeyMovieError):
    status_code = 400
    content = 'The given parameter is invalid'
    docs = {status_code: content}


class ResourceStateConflict(HeyMovieError):
    status_code = 409
    docs = {status_code: 'The is a problem with the state of a resource'}

    def __init__(self, message):
        self.content = message
        self.docs = {self.status_code: message}


class ResourceAlreadyExists(ResourceStateConflict):
    docs = {ResourceStateConflict.status_code: "The given resource already exists"}

    def __init__(self, entity):
        self.content = f"The given {entity} already exists"


class ResourceDoesNotExist(ResourceStateConflict):
    status_code = 404
    docs = {status_code: "The given resource was not found"}

    def __init__(self, entity):
        self.content = f"The given {entity} was not found"
