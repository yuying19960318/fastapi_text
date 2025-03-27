from passlib.context import CryptContext
from sqlalchemy.orm import Session
from  database import User,Role,Resource,Base,engine,AsyncSession,get_db
from  schemas import UserCreate
from fastapi import Depends
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, Security


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCRUD:
    async def create_user(self,user:UserCreate,db:AsyncSession = Depends(get_db)):
        # 获取角色对象
        role_stmt = select(Role).where(Role.name.in_([r.value for r in user.role_name]))
        role_result = await db.execute(role_stmt)
        roles = role_result.scalars().all()

        # 验证角色是否存在
        if len(roles) != len(user.role_name):
            found_roles = {role.name for role in roles}
            missing = [r.value for r in user.role_name if r.value not in found_roles]
            raise ValueError(f"以下角色不存在: {missing}")

        # 创建用户并关联角色
        db_user = User(
            username=user.username,
            hashed_password=pwd_context.hash(user.password),
            roles=roles  # 直接赋值角色对象列表
        )

        db.add(db_user)
        await db.commit()

        # 关键修改：重新加载关联数据
        await db.refresh(db_user, ["roles"])  # 显式刷新关联字段

        # 更安全的加载方式
        result = await db.execute(
            select(User)
            .options(selectinload(User.roles))  # 显式预加载
            .where(User.id == db_user.id)
        )
        return result.scalar_one()

    @staticmethod  # 静态方法
    async def authenticate_user( username:str,password:str,db:AsyncSession ):

        query = select(User).filter(User.username==username)
        result = await db.execute(query)
        user = result.scalars().first()
        if not user or not pwd_context.verify(password,user.hashed_password):
            return None
        return user


class MenuCRUD:
    async def get_all_menu(self, db: AsyncSession):  # 添加async关键字
        """异步获取所有菜单"""
        # 使用select查询代替query
        stmt = select(Resource)
        result = await db.execute(stmt)
        resources = result.scalars().all()

        seen = set()
        return [
            {"menu_name": res.menu_name, "path": res.path}
            for res in resources
            if not (res.id in seen or seen.add(res.id))
        ]

