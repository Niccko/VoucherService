import motor.motor_asyncio

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

voucher_collection = client.finances.get_collection("vouchers")


# Add a new student into to the database
async def add_voucher(student_data: dict) -> bool:
    student = await voucher_collection.insert_one(student_data)
    new_student = await voucher_collection.find_one({"_id": student.inserted_id})
    return True


