from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from server.database import (
    add_voucher
)
from server.models import (
    response_error,
    response_success,
    Voucher
)

import requests, os

router = APIRouter()


@router.post("/", response_description="Voucher data added into the database")
async def add_voucher_data(voucher_qr_raw: str):
    token = os.getenv("OFD_TOKEN")
    url = 'https://proverkacheka.com/api/v1/check/get'
    r = requests.post(url, data={"qrraw": voucher_qr_raw, "token": token})

    if not r.status_code == 200:
        return response_error("OFD_ERROR", r.status_code, "Error while getting voucher info")
    data = r.json().get("data")
    if not isinstance(data, dict):
        return response_error("OFD_ERROR", r.status_code, str(data))
    voucher = {
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
