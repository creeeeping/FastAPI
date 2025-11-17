from fastapi import APIRouter
from fastapi_assignment.app.schemas.users import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

fake_users = []
user_id = 1

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate):
    global user_id
    new_user = {"id": user_id, **user.dict()}
    user_id += 1
    fake_users.append(new_user)
    return new_user

@router.get("/", response_model=list[UserResponse])
def get_users():
    return fake_users
