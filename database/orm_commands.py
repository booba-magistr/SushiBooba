from sqlalchemy.ext.asyncio import AsyncSession
from .models import Product
from sqlalchemy import select, delete, update


async def orm_add_product(session: AsyncSession, data):
    obj = Product(
        name = data['name'],
        description = data['description'],
        price = float(data['price']),
        img = data['img']
    )
    session.add(obj)
    await session.commit()

async def orm_get_products(session: AsyncSession):
    queryset = select(Product)
    result = await session.execute(queryset)
    return result.scalar().all()

async def orm_get_product(session: AsyncSession, product_id):
    product = select(Product).where(Product.id == product_id)
    result = await session.execute(product)
    return result.scalar()

async def orm_update_product(session: AsyncSession, product_id, data):
    queryset = update(Product).where(Product.id == product_id).values(
        name = data['name'],
        description = data['description'],
        price = float(data['price']),
        img = data['img']
    )
    await session.execute(queryset)
    await session.commit()

async def orm_delete_product(session: AsyncSession, product_id):
    product = delete(Product).where(Product.id == product_id)
    await session.execute(product)
    await session.commit()