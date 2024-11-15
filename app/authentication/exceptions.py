from fastapi import HTTPException, status


credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

permission_error = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this user information.")