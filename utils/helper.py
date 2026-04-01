
import hashlib, logging
from sqlalchemy import inspect

logger = logging.getLogger(__name__)

@staticmethod
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


@staticmethod
def to_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}