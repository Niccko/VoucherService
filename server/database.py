import os

import motor.motor_asyncio

MONGO_DETAILS = os.getenv("MONGO_URI")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

voucher_collection = client.finances.get_collection("Vouchers")


# Add a new voucher into to the database
async def add_voucher(voucher_data: dict) -> bool:
    voucher = await voucher_collection.insert_one(voucher_data)
    new_voucher = await voucher_collection.find_one({"_id": voucher.inserted_id})
    return new_voucher


async def retrieve_vouchers(page=1, limit=10):
    vouchers = []
    async for student in voucher_collection.find().skip((page - 1) * limit).limit(limit):
        vouchers.append(student)
    return vouchers


async def retrieve_voucher_by_fields(**cond) -> dict:
    voucher = await voucher_collection.find_one(cond)
    if voucher:
        return voucher


async def retrieve_voucher(id: str) -> dict:
    voucher = await voucher_collection.find_one({"_id": id})
    if voucher:
        return voucher


# Add a raw data into to the database
async def add_raw(collection_name, data: dict) -> bool:
    collection = client.finances.get_collection(collection_name)
    obj = await collection.insert_one(data)
    return True


# Get raw data from database
async def get_raw(collection_name, **cond) -> bool:
    collection = client.finances.get_collection(collection_name)
    obj = await collection.find_one(cond)
    if obj:
        return obj
