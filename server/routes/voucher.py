from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from server.database import (
    add_voucher,
    retrieve_vouchers,
    retrieve_voucher,
    retrieve_voucher_by_fields,
    add_raw,
    get_raw
)
from server.models import (
    response_error,
    response_success,
    Voucher
)

from server.sources import get_ofd_info

from uuid import uuid1

router = APIRouter()


@router.post("/", response_description="Voucher data added into the database")
async def add_voucher_data(voucher_qr_raw: str):
    if await retrieve_voucher_by_fields(raw_code=voucher_qr_raw):
        return response_error("Already exists", 400, f"Voucher {voucher_qr_raw} already processed")
    try:
        data = await get_raw("VouchersRaw", raw_code=voucher_qr_raw)
        if not data:
            data = get_ofd_info(voucher_qr_raw)
    except Exception as e:
        return response_error(*e.args)
    await add_raw("VouchersRaw", {**data, "raw_code": voucher_qr_raw, "_id": uuid1().hex})
    voucher = {
        "raw_code": voucher_qr_raw,
        "code": data.get("code"),
        "user": data.get("user"),
        "operation_dttm": data.get("dateTime"),
        "total_sum": data.get("totalSum") / 100,
        "retail_place": data.get("retailPlace"),
        "address": data.get("retailPlaceAddress")
    }
    items = []
    for item_raw in data.get("items"):
        item = {
            "total": item_raw.get("sum") / 100,
            "price": item_raw.get("price") / 100,
            "name": item_raw.get("name"),
            "quantity": item_raw.get("quantity"),
            "product_type": item_raw.get("productType")}
        if item_raw.get("productCodeNew"):
            if item_raw.get("productCodeNew").get("ean13"):
                ean = item_raw.get("productCodeNew").get("ean13")
                e = {
                    "sernum": ean.get("sernum"),
                    "product_id_type": ean.get("productIdType"),
                    "raw_product_code": ean.get("rawProductCode")}
                item["ean"] = e
        items.append(item)
    voucher["items"] = items
    v = jsonable_encoder(Voucher(**voucher))
    new_voucher = await add_voucher(v)
    return response_success(data=new_voucher, message="Voucher added successfully.")


@router.get("/", response_description="Got list of vouchers")
async def get_vouchers():
    students = await retrieve_vouchers()
    if students:
        return response_success(students, "Voucher data retrieved successfully")
    return response_success(students, "Empty list returned")


@router.get("/{id}", response_description="Voucher data retrieved")
async def get_voucher(id):
    student = await retrieve_voucher(id)
    if student:
        return response_success(student, "Voucher data retrieved successfully")
    return response_error("An error occurred.", 404, "Voucher doesn't exist.")
