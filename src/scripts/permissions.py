from typing import List

from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials

from src.scripts.jwt import decode_access_token


def get_current_user(token: HTTPAuthorizationCredentials = Depends(auth_schema)):
    return decode_access_token(token)


class PermissionChecker:

    def __init__(self, required_permissions: List[str]) -> None:
        self.required_permissions = required_permissions

    def __call__(self, user=Depends(get_current_user)) -> bool:
        if user['role'] in self.required_permissions:
            return True
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='The user does not have access to the resource'
            )