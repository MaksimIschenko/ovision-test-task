import pytest
from httpx import AsyncClient
from sqlalchemy import insert
from starlette.datastructures import UploadFile as StarletteUploadFile
import os
from io import BytesIO

from src.imgs.models import image
from tests.conftest import async_session_maker


def create_test_upload_file(filename: str):
    """
    Создание тестового файла изображения
    :param filename: имя файла
    :return:
    """
    data = BytesIO(b"fake image data")  # Имитация данных изображения
    return StarletteUploadFile(filename=filename, file=data)  # Используется Starlette UploadFile


@pytest.mark.asyncio
async def test_negative_image_valid_file(ac: AsyncClient):
    # Создание тестового файла изображения
    file = create_test_upload_file(filename="tests/images/test.jpg")
    files = {'file': (file.filename, file.file.read(), "image/jpeg")}  # Используются данные изображения

    response = await ac.post("/images/negative_image", files=files)

    assert response.status_code == 302
    assert "Location" in response.headers
    assert response.headers["Location"] == "http://localhost:8000"


@pytest.mark.asyncio
async def test_negative_image_invalid_file_extension(ac: AsyncClient):
    # Создание тестового файла с неверным расширением
    file = create_test_upload_file(filename="tests/images/test.txt")
    files = {'file': (file.filename, file.file, file.content_type)}

    response = await ac.post("images/negative_image", files=files)

    assert response.status_code == 400
    assert "detail" in response.json()
    assert response.json()["detail"] == "Invalid file extension. Only .jpg, .jpeg, .png are allowed"


@pytest.mark.asyncio
async def test_negative_image_no_file(ac: AsyncClient):
    response = await ac.post("images/negative_image")
    assert response.status_code == 422  # Ожидание кода ошибки валидации FastAPI


async def test_add_get_last_images():
    """
    Тестирование добавления изображений в тестовую базу данных.
    """
    async with async_session_maker() as session:
        for _ in range(3):
            stmt = insert(image).values(original_image="test", negative_image="test")
            await session.execute(stmt)
        await session.commit()


@pytest.mark.asyncio
async def test_get_last_images(ac):
    # Отправка GET-запроса к API для получения последних трех изображений
    response = await ac.get("images/get_last_images")

    # Проверка статуса ответа
    assert response.status_code == 200, "Неверный статус код ответа"

    # Проверка структуры ответа
    data = response.json()
    assert isinstance(data, list), "Ответ должен быть списком"
    assert len(data) <= 3, "В ответе должно быть не более трех изображений"

    # Проверка наличия ключевых полей в каждом объекте изображения
    required_keys = {"id", "original", "negative"}
    for img in data:
        assert isinstance(img, dict), "Каждый элемент в списке должен быть словарем"
        assert required_keys.issubset(img.keys()), "Некоторые ключи отсутствуют в изображении"

