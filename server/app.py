from .auth import security, auth
from fastapi import FastAPI, Depends
from dotenv import load_dotenv

from server.routes.voucher import router as StudentRouter

app = FastAPI(dependencies=[Depends(security)])
load_dotenv()

app.include_router(StudentRouter, tags=["Voucher"], prefix="/voucher", dependencies=[Depends(auth)])


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
