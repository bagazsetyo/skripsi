from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from app.auth import authenticate_admin, create_access_token, get_current_admin
from app.schemas import LoginRequest, LoginResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def auth_login(request: LoginRequest):
    admin = authenticate_admin(request.username, request.password)
    if admin is None:
        raise HTTPException(status_code=401, detail="Username atau password salah")
    token = create_access_token(admin)
    return LoginResponse(
        access_token=token,
        username=admin["username"],
        role=admin["role"],
    )


@router.get("/me")
def auth_me(current_admin: dict = Depends(get_current_admin)):
    return current_admin
