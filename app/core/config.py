import os
from dotenv import load_dotenv

load_dotenv()  # .env 읽기 (없어도 에러 안 남)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dev.db")