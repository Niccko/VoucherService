import os

import motor.motor_asyncio

log = os.getenv("MONGO_LOGIN")
pwd = os.getenv("MONGO_PWD")

MONGO_DETAILS = f"mongodb:{log}:{pwd}//localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

voucher_collection = client.finances.get_collection("Vouchers")


# Add a new student into to the database
async def add_voucher(student_data: dict) -> bool:
    student = await voucher_collection.insert_one(student_data)
    new_student = await voucher_collection.find_one({"_id": student.inserted_id})
    return True
