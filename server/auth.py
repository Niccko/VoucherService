import secrets, os
from typing import Annotated
from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.security import HTTPBasicCredentials, HTTPBasic

security = HTTPBasic()


def auth(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    correct_username = os.getenv("ADMIN_LOGIN")
    correct_password = os.getenv("ADMIN_PWD")

    if not correct_username or not correct_password:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Admin credential are not set",
            headers={"WWW-Authenticate": "Basic"},
        )

    current_username_bytes = credentials.username.encode("utf8")
    current_password_bytes = credentials.password.encode("utf8")

    is_correct_username = secrets.compare_digest(current_username_bytes, correct_username)
    is_correct_password = secrets.compare_digest(current_password_bytes, correct_password)

    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
