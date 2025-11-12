import uvicorn
from fastapi import FastAPI

from src.api import main_router


app = FastAPI(title="My First App")
app.include_router(main_router)


def main():
    uvicorn.run("src.main:app", reload=True)

if __name__ == "__main__":
    main()