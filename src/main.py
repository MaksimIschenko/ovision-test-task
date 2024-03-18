from fastapi import FastAPI
from imgs.router import router as imgs_router
from pages.router import router as pages_router


app = FastAPI(
    title="Ovision TetsApp",
)

app.include_router(imgs_router)
app.include_router(pages_router)
