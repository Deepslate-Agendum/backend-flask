from mongoengine.errors import ValidationError

from db_python_util.db_helper import ConnectionManager
from db_python_util.db_exceptions import EntityNotFoundException

@ConnectionManager.requires_connection
def get_document_by_id(collection: type, id: str, allow_none: bool=False):
    try:
        document = collection.objects.with_id(id)
    except ValidationError: # An ObjectId "must be a 12-byte input or a 24-character hex string", but front-end shouldn't need to care about that
        document = None

    if document is None and not allow_none:
        raise EntityNotFoundException(
            collection,
            f"No {collection.__name__} with id '{id}' could be found"
        )

    return document
