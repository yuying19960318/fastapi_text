from typing import Optional, List
from pydantic import BaseModel
from enum import Enum


#用户模型

# 定义角色枚举
class RoleEnum(str, Enum):
    admin = "admin"
    user = "user"
    guest = "guest"
class UserCreate(BaseModel):
    username: str
    password: str
    role_name: List[RoleEnum]

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    username: Optional[str] = None
    roles:List[str]
    class Config:
        from_attributes = True

#获取用户信息模型——过滤器（填写信息可填可不填写）
class UserFilter(BaseModel):
    username: Optional[str] = None
    roles: Optional[List[str]] = None

#获取用户的相应的模型
class UserResponse(BaseModel):
    username: str
    roles: List[str]



#认证模型
# class Token(BaseModel):
#     access_token: str
#     token_type: str

#菜单模型
class MenuItem(BaseModel):
    menu_name: str
    path: str

class userMenuResponse(BaseModel):
    menu: List[MenuItem]

