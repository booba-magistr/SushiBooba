from sqlalchemy.ext.asyncio import AsyncSession
from .models import Product


async def orm_add_product(session: AsyncSession, data):
    obj = Product(
        name = data['name'],
        description = data['description'],
        price = float(data['price']),
        img = data['img']
    )
    session.add(obj)
    await session.commit()