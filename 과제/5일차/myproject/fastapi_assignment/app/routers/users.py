from typing import List

from fastapi import APIRouter, HTTPException, UploadFile

from app.models.users import UserModel
from app.schemas.users import UserCreate, UserResponse, UserUpdate
from app.utils.file import upload_file, delete_file, validate_image_extension

router = APIRouter(prefix="/users", tags=["users"])


def _to_response(user: UserModel) -> UserResponse:
    return UserResponse(
        id=user.id,
        username=user.username,
        age=user.age,
        gender=user.gender,
        profile_image_url=user.profile_image_url,
    )


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate):
    new_user = UserModel.create(
        username=user.username,
        password=user.password,
        age=user.age,
        gender=user.gender.value,
    )
    return _to_response(new_user)


@router.get("/", response_model=List[UserResponse])
async def get_users():
    return [_to_response(u) for u in UserModel.all()]


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    user = UserModel.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return _to_response(user)


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, data: UserUpdate):
    user = UserModel.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = data.model_dump(exclude_unset=True)
    # password는 단순 문자열로 유지 (실서비스라면 해시 필요)
    user.update(**update_data)
    return _to_response(user)


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int):
    user = UserModel.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.delete()
    return


def _get_current_user() -> UserModel:
    users = UserModel.all()
    if not users:
        raise HTTPException(status_code=404, detail="No users available")
    # 실서비스라면 JWT 인증을 사용해야 하지만,
    # 과제에서는 가장 첫 번째 유저를 '나(me)'로 가정합니다.
    return users[0]


@router.post("/me/profile_image", response_model=UserResponse, status_code=200)
async def register_profile_image(image: UploadFile):
    """Register or replace the current user's profile image.

    - 확장자 검사
    - 파일 저장
    - 이전 파일이 있으면 삭제
    """
    user = _get_current_user()

    validate_image_extension(image)
    prev_image_url = user.profile_image_url

    try:
        image_url = await upload_file(image, "users/profile_images")
        user.profile_image_url = image_url

        if prev_image_url is not None:
            delete_file(prev_image_url)

        return _to_response(user)
    except Exception as e:  # pragma: no cover - 단순 에러 래핑
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
