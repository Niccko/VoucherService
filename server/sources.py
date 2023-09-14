import os

import requests


def get_ofd_info(voucher_qr_raw: str):
    token = os.getenv("OFD_TOKEN")
    url = 'https://proverkacheka.com/api/v1/check/get'
    r = requests.post(url, data={"qrraw": voucher_qr_raw, "token": token})

    if not r.status_code == 200:
        raise Exception("OFD_ERROR", r.status_code, "Error while getting voucher info")
    data = r.json().get("data")
    if not isinstance(data, dict):
        raise Exception("OFD_ERROR", r.status_code, str(data))
    return data.get("json")
