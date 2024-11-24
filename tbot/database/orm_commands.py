from sqlalchemy.ext.asyncio import AsyncSession
from .models import Product, Category, Banner
from sqlalchemy import select, delete, update
from math import ceil


##################### Paginator #####################

class Paginator:
    def __init__(self, lst, page=1, per_page=1) -> None:
        self.lst = lst
        self.page = page
        self.per_page = per_page
        self.length = len(lst)
        self.pages = ceil(self.length / self.per_page)

    def get_slice(self):
        start = (self.page - 1) * self.per_page
        stop = start + self.per_page
        return self.lst[start: stop]

    def get_page(self):
        page_items = self.get_slice()
        return page_items

    def has_next(self):
        if self.page < self.length:
            return self.page + 1
        return False
        
    def has_previous(self):
        if self.page > 1:
            return self.page - 1
        return False


#################### CRUD for banners ####################

async def orm_add_banners(session: AsyncSession, data):
    obj = Banner(
        img = data['img'],
        banner_name = data['banner_name'],
        title = data['title'],
    )
    session.add(obj)
    await session.commit()

async def orm_get_banners(session: AsyncSession):
    queryset = select(Banner)
    result = await session.execute(queryset)
    return result.scalars().all()

async def orm_get_banner(session: AsyncSession, banner_name):
    queryset = select(Banner).where(Banner.banner_name == banner_name)
    result = await session.execute(queryset)
    return result.scalar()

async def orm_delete_banner(session: AsyncSession, banner_name):
    query = delete(Banner).where(Banner.banner_name == banner_name)
    await session.execute(query)
    await session.commit()

async def orm_update_banner(session: AsyncSession, banner_id, data: dict):
    query = update(Banner).where(Banner.id == int(banner_id)).values(
        banner_name = data['banner_name'],
        title = data['title'],
        img = data['img']
    )
    await session.execute(query)
    await session.commit()

#################### CRUD for categories ####################

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

#################### CRUD for Products ####################

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
    product = delete(Product).where(Product.id == int(product_id))
    await session.execute(product)
    await session.commit()