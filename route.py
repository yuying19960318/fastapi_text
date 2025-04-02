from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from crud  import UserCRUD,MenuCRUD,UserServer
from schemas  import UserCreate ,UserOut,UserLogin,MenuItem,userMenuResponse,UserFilter,UserResponse
from database import get_db
from typing import Optional,List


router = APIRouter()
#用户注册路由
@router.post('/register',response_model=UserOut)    #返回数据需要用UserOut模型验证（输入和都系要验证）
async def register(
        user: UserCreate,
        db: AsyncSession = Depends(get_db)
):
    try:
        db_user = await UserCRUD().create_user(user, db)
        return {
            "username": db_user.username,
            "roles": [role.name for role in db_user.roles]
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
#用户登录路由
@router.post('/login',response_model=UserOut)
async def login(
        form_data: UserLogin,
        db: AsyncSession = Depends(get_db)
):
    crud = UserCRUD()
    user = await crud.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="用户名或密码错误")
    return user

#获取菜单信息路由
@router.get('/menu')
async def get_all_menu(
    db: AsyncSession = Depends(get_db),  # get路由直接获取数据库会话，取MenuCRUD函数的实例，拿到所有菜单
    menu_crud: MenuCRUD = Depends()
):
    menus = await menu_crud.get_all_menu(db)  # 调用新方法
    return {"menu": menus}


#获取用户信息路由
@router.get('/users',response_model=list[UserResponse])
async def get_users(
        service: UserServer = Depends(),
        db: AsyncSession = Depends(get_db),
        username: Optional[str] = Query(None),
        roles: Optional[List[str]] = Query(None),
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=100)

):
    try:
        filters=UserFilter(username=username,roles=roles)
        users = await service.get_user(db, filters, page, page_size)
        return [
            UserResponse(
                username=user.username,
                roles=[role.name for role in user.roles]
            )
            for user in users
        ]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

