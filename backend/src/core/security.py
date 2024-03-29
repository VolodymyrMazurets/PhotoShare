from src.services.roles import RoleRights

allowed_operation_admin = RoleRights(["admin"])
allowed_operation_any_user = RoleRights(["user", "moderator", "admin"])
allowed_operation_admin_moderator = RoleRights(["admin", "moderator"])