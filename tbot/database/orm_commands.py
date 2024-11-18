from sqlalchemy.ext.asyncio import AsyncSession
from .models import Product, Category
from sqlalchemy import select, delete, update



async def orm_create_categories(session: AsyncSession, categories: list):
    query = select(Category)
    result = await session.execute(query)
    if result.first():
        return
    session.add_all([Category(name=name) for name in categories]) 
    await session.commit()

async def orm_get_categories(session: AsyncSession):
    queryset = select(Category)
    result = await session.execute(queryset)
    return result.scalars().all()

### CRUD for Admin ###

async def orm_add_product(session: AsyncSession, data):
    obj = Product(
        name = data['name'],
        description = data['description'],
        price = float(data['price']),
        img = data['img'],
        category_id = data['category']
    )
    session.add(obj)
    await session.commit()

async def orm_get_products(session: AsyncSession, category_id):
    queryset = select(Product).where(Product.category_id == int(category_id))
    result = await session.execute(queryset)
    return result.scalars().all()

async def orm_get_product(session: AsyncSession, product_id):
    product = select(Product).where(Product.id == product_id)
    result = await session.execute(product)
    return result.scalar()

async def orm_update_product(session: AsyncSession, product_id, data):
    queryset = update(Product).where(Product.id == product_id).values(
        name = data['name'],
        description = data['description'],
        price = float(data['price']),
        img = data['img'],
        category_id = data['category'] 
    )
    await session.execute(queryset)
    await session.commit()

async def orm_delete_product(session: AsyncSession, product_id):
    product = delete(Product).where(Product.id == product_id)
    await session.execute(product)
    await session.commit()