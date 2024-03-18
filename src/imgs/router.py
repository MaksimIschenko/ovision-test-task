import cv2
import numpy as np
import base64

from sqlalchemy import select, desc, insert
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import RedirectResponse

from database import get_async_session
from .models import image
from .schemas import ImageData

import os

router = APIRouter(
    prefix="/images",
    tags=["images"],
)


@router.post("/negative_image")
async def negative_image(session: AsyncSession = Depends(get_async_session),
                         file: UploadFile = File(...)):
    """
    Функция для загрузки изображения, приведение его к негативу и загрузка в базу данных в формате base64
    :param session: сессия базы данных
    :param file: файл изображения
    :return:
    """

    # Проверка расширения файла
    ext = os.path.splitext(file.filename)[1]
    if ext not in ['.jpg', '.jpeg', '.png']:
        raise HTTPException(status_code=400, detail="Invalid file extension. Only .jpg, .jpeg, .png are allowed")

    # Чтение файла
    contents = await file.read()

    # Преобразование изображения в негатив
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    negative = 255 - img

    # Преобразование изображений в base64
    _, original_encoded = cv2.imencode('.jpg', img)
    _, negative_encoded = cv2.imencode('.jpg', negative)

    # Загрузка изображений в базу данных
    original_base64 = base64.b64encode(original_encoded).decode('utf-8')
    negative_base64 = base64.b64encode(negative_encoded).decode('utf-8')
    stmt = insert(image).values(original_image=original_base64, negative_image=negative_base64).returning(image.c.id)
    await session.execute(stmt)
    await session.commit()

    # Перенаправление на главную страницу
    return RedirectResponse(url='http://localhost:8000', status_code=302)


@router.get("/get_last_images")
async def get_last_images(session: AsyncSession = Depends(get_async_session)) -> list[ImageData]:
    """
    Функция для получения последних 3 изображений из базы данных
    :param session: сессия базы данных
    :return: список изображений в формате ImageData (см. schemas.py)
    """
    stmt = select(image).order_by(desc(image.c.id)).limit(3)
    result = await session.execute(stmt)
    return [ImageData(id=el[0], original=el[1], negative=el[2]) for el in result]
