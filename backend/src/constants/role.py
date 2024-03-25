from sqlalchemy import Enum

class UserRole(str, Enum):
    admin = "admin"
    user = "user"
    moderator = "moderator"