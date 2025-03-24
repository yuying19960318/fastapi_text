from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from crud  import UserCRUD,MenuCRUD
from schemas  import UserCreate ,UserOut,UserLogin,MenuItem,userMenuResponse
from database import get_db


router = APIRouter()
#用户注册路由
@router.post('/register',response_model=UserOut)
async def register(
        user: UserCreate,
        db: AsyncSession = Depends(get_db)
):
    try:
        db_user = await UserCRUD().create_user(user, db)
        roles = []
        for role in db_user.roles:
            roles.append(role.name)
        return {
            "username": db_user.username,
            "roles": roles
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
#用户登录路由
@router.post('/login',response_model=UserOut)
async def login(
        form_data: UserLogin,
        db: AsyncSession = Depends(get_db)
):
    user = await UserCRUD.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="用户名或密码错误")
    return user

#获取菜单信息路由
@router.get('/menu',response_model=userMenuResponse)
def get_menu(
        db: Session = Depends(get_db),
        menu_crud:MenuCRUD = Depends()
):
    menus = menu_crud.get_menus()
    return {"menu":menus}


