def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        key: str = payload.get("sub")
        if key is None:
            raise credentials_exception
        token_data = TokenData(key=key, role=payload.get("role"), admin=payload.get("admin"))
    except JWTError:
        raise credentials_exception
    return token_data

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

def admin_required(current_user: TokenData = Depends(get_current_user)):
    if not current_user.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )