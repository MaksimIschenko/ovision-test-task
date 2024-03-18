from sqlalchemy import MetaData, Table, Integer, Column, String

metadata = MetaData()


""" Модель для таблицы изображений """
image = Table(
    'images',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('original_image', String, nullable=False),
    Column('negative_image', String, nullable=False),
)
