from sqlalchemy import Column,Integer,String,ForeignKey,Table,DateTime
from sqlalchemy.orm import relationship,declarative_base ,sessionmaker
#from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine ,AsyncSession


Base = declarative_base()

# 创建中间表
user_role=Table(
    "user_role",
    Base.metadata,
    Column("user_id",Integer),
    Column("role_id",Integer)
)

role_resource=Table(
    "role_resource",
    Base.metadata,
    Column("role_id",Integer,ForeignKey("role.id")),
    Column("resource_id",Integer,ForeignKey("resource.id"))
)

class User(Base):
    __tablename__="user"
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String(50),unique=True,index=True)
    hashed_password=Column(String(200))
    roles = relationship(
        "Role",
        secondary=user_role,
        primaryjoin="User.id == user_role.c.user_id",
        secondaryjoin="Role.id == user_role.c.role_id",
        back_populates="users",
        lazy="selectin"  # 添加加载策略
    )
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    create_user = Column(String(50), nullable=True)
    update_user = Column(String(50), nullable=True)

class Role(Base):
    __tablename__="role"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(50),unique=True,index=True)
    description=Column(String(200))
    users = relationship(
        "User",
        secondary=user_role,
        primaryjoin="Role.id == user_role.c.role_id",
        secondaryjoin="User.id == user_role.c.user_id",
        back_populates="roles",
        lazy="selectin"  # 添加加载策略
    )
    resources=relationship("Resource",secondary="role_resource",back_populates="roles")
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    create_user = Column(String(50), nullable=True)
    update_user = Column(String(50), nullable=True)


class Resource(Base):
    __tablename__="resource"
    id=Column(Integer,primary_key=True,index=True)
    menu_name=Column(String(50),unique=True)
    path = Column(String(100))
    roles=relationship("Role",secondary="role_resource",back_populates="resources")
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    create_user = Column(String(50), nullable=True)
    update_user = Column(String(50), nullable=True)


# 数据库配置
DATABASE_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "test",
    "database": "financial_date",
    "port": 3306
}

# 使用asyncmy异步驱动（需要安装asyncmy）
DATABASE_URL = f"mysql+asyncmy://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"

# 创建异步引擎
engine = create_async_engine(DATABASE_URL, echo=True)

# 创建异步会话工厂
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            #await session.commit()
        except Exception as e:
            await session.rollback()
            raise
        finally:
            await session.close()




