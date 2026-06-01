from datetime import datetime, timedelta, timezone
import hashlib
import os
from collections import defaultdict
import time
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column
from jose import jwt
from pydantic import BaseModel

DATABASE_URL = "sqlite:///blog.db"
SECRET_KEY = "abc123secret"
ALGORITHM = "HS256"

engine = create_engine(DATABASE_URL, echo=False)

class Base(DeclarativeBase):
      pass

class User(Base):
      __tablename__ = "users"
      id: Mapped[int] = mapped_column(primary_key=True)
      username: Mapped[str] = mapped_column(unique=True)
      hashed_password: Mapped[str]

class Article(Base):
      __tablename__ = "articles"
      id: Mapped[int] = mapped_column(primary_key=True)
      title: Mapped[str]
      content: Mapped[str]
      author_id: Mapped[int]
      created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

Base.metadata.create_all(engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

rate_store = defaultdict(list)
RATE_LIMIT = 60

app = FastAPI()


class UserCreate(BaseModel):
      username: str
      password: str

class ArticleCreate(BaseModel):
      title: str
      content: str

class ArticleOut(BaseModel):
      id: int
      title: str
      content: str
      author_id: int
      created_at: datetime

      model_config = {"from_attributes": True}

class Token(BaseModel):
      access_token: str
      token_type: str


def get_db():
      with Session(engine) as db:
          yield db

def create_token(username: str) -> str:
      expire = datetime.now(timezone.utc) + timedelta(hours=2)
      return jwt.encode({"sub": username, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(
      token: str = Depends(oauth2_scheme),
      db: Session = Depends(get_db),
  ) -> User:
      try:
          payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
          username = payload.get("sub")
      except Exception:
          raise HTTPException(status_code=401)
      user = db.execute(select(User).where(User.username == username)).scalar_one_or_none()
      if not user:
          raise HTTPException(status_code=401)
      return user


def load_env():
      env_file = os.path.join(os.path.dirname(__file__), ".env")
      if os.path.exists(env_file):
          with open(env_file, encoding="utf-8") as f:
              for line in f:
                  line = line.strip()
                  if line and not line.startswith("#") and "=" in line:
                      k, v = line.split("=", 1)
                      os.environ.setdefault(k, v)

load_env()


def summarize_with_deepseek(text: str) -> str:
      import json as _json
      import requests as _requests
      api_key = os.getenv("DEEPSEEK_KEY")
      r = _requests.post(
          "https://api.deepseek.com/chat/completions",
          headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
          json={
              "model": "deepseek-chat",
              "messages": [
                  {"role": "system", "content": "用中文一句话总结以下文章内容"},
                  {"role": "user", "content": text}
              ],
              "max_tokens": 100
          },
          timeout=30
      )
      return r.json()["choices"][0]["message"]["content"].strip()


@app.middleware("http")
async def rate_limit(request: Request, call_next):
      ip = request.client.host or "127.0.0.1"
      now = time.time()
      rate_store[ip] = [t for t in rate_store[ip] if now - t < 60]
      if len(rate_store[ip]) >= RATE_LIMIT:
          return JSONResponse(status_code=429, content={"detail": "请求太频繁"})
      rate_store[ip].append(now)
      return await call_next(request)


@app.post("/register", status_code=201)
def register(data: UserCreate, db: Session = Depends(get_db)):
      if db.execute(select(User).where(User.username == data.username)).scalar_one_or_none():
          raise HTTPException(status_code=400, detail="用户名已存在")
      user = User(
          username=data.username,
          hashed_password=hashlib.sha256(data.password.encode()).hexdigest()
      )
      db.add(user)
      db.commit()
      return {"ok": True}


@app.post("/token")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
      user = db.execute(select(User).where(User.username == form.username)).scalar_one_or_none()
      if not user or hashlib.sha256(form.password.encode()).hexdigest() != user.hashed_password:
          raise HTTPException(status_code=401, detail="用户名或密码错误")
      return Token(access_token=create_token(user.username), token_type="bearer")


@app.get("/articles")
def list_articles(db: Session = Depends(get_db)):
      return db.execute(select(Article).order_by(Article.created_at.desc())).scalars().all()


@app.get("/articles/{article_id}")
def get_article(article_id: int, db: Session = Depends(get_db)):
      a = db.execute(select(Article).where(Article.id == article_id)).scalar_one_or_none()
      if not a:
          raise HTTPException(status_code=404, detail="不存在")
      return a


@app.post("/articles", status_code=201)
def create_article(
      data: ArticleCreate,
      user: User = Depends(get_current_user),
      db: Session = Depends(get_db),
  ):
      a = Article(title=data.title, content=data.content, author_id=user.id)
      db.add(a)
      db.commit()
      db.refresh(a)
      return a


@app.delete("/articles/{article_id}")
def delete_article(
      article_id: int,
      user: User = Depends(get_current_user),
      db: Session = Depends(get_db),
  ):
      a = db.execute(select(Article).where(Article.id == article_id)).scalar_one_or_none()
      if not a:
          raise HTTPException(status_code=404, detail="不存在")
      if a.author_id != user.id:
          raise HTTPException(status_code=403, detail="只能删除自己的文章")
      db.delete(a)
      db.commit()
      return {"ok": True}


@app.post("/articles/{article_id}/summarize")
def summarize_article(article_id: int, db: Session = Depends(get_db)):
      a = db.execute(select(Article).where(Article.id == article_id)).scalar_one_or_none()
      if not a:
          raise HTTPException(status_code=404, detail="不存在")
      result = summarize_with_deepseek(a.content)
      return {"article_id": article_id, "summary": result}