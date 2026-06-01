from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
      pass


class User(Base):
      __tablename__ = "users"
      id: Mapped[int] = mapped_column(primary_key=True)
      name: Mapped[str]
      age: Mapped[int]


engine = create_engine("sqlite:///demo.db", echo=False)
Base.metadata.create_all(engine)

with Session(engine) as s:
      s.add(User(name="张三", age=25))
      s.add(User(name="李四", age=30))
      s.commit()

      for u in s.execute(select(User).where(User.age > 23)).scalars():
          print(f"{u.id} | {u.name} | {u.age}")

      zs = s.execute(select(User).where(User.name == "张三")).scalar_one()
      zs.age = 26
      s.commit()
      print(f"\n张三年龄改为: {zs.age}")