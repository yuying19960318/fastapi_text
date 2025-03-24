from passlib.context import CryptContext
from sqlalchemy.orm import Session
from  database import User,Role,Resource,Base,engine,AsyncSession,get_db
from  schemas import UserCreate
from fastapi import Depends
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCRUD:
    async def create_user(self,user:UserCreate,db:AsyncSession = Depends(get_db)):

        db_user=User(
            username=user.username,
            hashed_password=pwd_context.hash(user.password),
        )
        db_user.roles=[]
        db.add(db_user)
        await db.commit()

        stmt = select(User).options(joinedload(User.roles)).where(User.id == db_user.id)
        result = await db.execute(stmt)
        unique_result = result.unique()
        db_user = unique_result.scalar_one()

        # 新增的异步查询角色列表部分，通过角色ID去查询角色对象
        role_ids = [role.id for role in db_user.roles]
        if role_ids:  # 确保有角色ID才进行查询
            role_stmt = select(Role).where(Role.id.in_(role_ids))
            role_result = await db.execute(role_stmt)
            roles = role_result.scalars().all()
            db_user.roles = roles  # 将查询到的角色列表设置回用户对象的角色属性

        return db_user

    async def authenticate_user(self, username:str,password:str,db:AsyncSession = Depends(get_db)):
        query = select(User).filter(User.username==username)
        result = await db.execute(query)
        user = result.scalars().first()
        if not user or not pwd_context.verify(password,user.hashed_password):
            return None
        return user

class MenuCRUD:
    def get_menu(self,user:User):
        seen = set()
        result =[
            {"menu_name":res.menu_name,"path":res.path}
            for role in user.roles
            for res in role.resources
            if not (res.id in seen or seen.add(res.id))]


