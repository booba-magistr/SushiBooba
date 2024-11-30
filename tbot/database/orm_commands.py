from sqlalchemy.ext.asyncio import AsyncSession
from .models import Product, Category, Banner, User, Cart
from sqlalchemy import select, delete, update
from math import ceil
from sqlalchemy.orm import joinedload


#################### Create user ####################

async def orm_add_user(session:AsyncSession, user_id, first_name, last_name,phone):
    query = select(User).where(User.user_id == user_id)
    result = await session.execute(query)
    if result.first() is None:
        obj = User(user_id = user_id, first_name=first_name, last_name=last_name, phone=phone)
        session.add(obj)
        await session.commit()

################### CRUD cart ###################

async def orm_add_to_cart(session: AsyncSession, user_id, product_id):
    queryset =  select(Cart).where(Cart.user_id == user_id, Cart.product_id == product_id)
    cart = await session.execute(queryset)
    cart = cart.scalar()
    if cart:
        cart.quantity += 1
        await session.commit()
        return cart
    else:
        obj = Cart(user_id=user_id, product_id=product_id, quantity=1)
        session.add(obj)
        await session.commit()

async def orm_delete_from_cart(session: AsyncSession, user_id, product_id):
    queryset = delete(Cart).where(Cart.user_id == user_id, Cart.product_id == product_id)
    await session.execute(queryset)
    await session.commit()

async def orm_get_user_carts(session: AsyncSession, user_id:int):
    queryset = select(Cart).filter(Cart.user_id == user_id).options(joinedload(Cart.product))
    result = await session.execute(queryset)
    return result.scalars().all()

async def orm_reduce_product_in_cart(session: AsyncSession, user_id: int, product_id: int):
    query = select(Cart).where(Cart.user_id == user_id, Cart.product_id == product_id)
    cart = await session.execute(query)
    cart = cart.scalar()

    if not cart:
        return
    if cart.quantity > 1:
        cart.quantity -= 1
        await session.commit()
        return True
    else:
        await orm_delete_from_cart(session, user_id, product_id)
        await session.commit()
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