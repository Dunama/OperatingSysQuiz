import os
from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import JSONResponse
import httpx

router = APIRouter()
PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY", "sk_test_5fa702d0bceb131cb2589e0c6b109ba63e709879")  
PAYSTACK_PUBLIC_KEY = os.getenv("PAYSTACK_PUBLIC_KEY", "pk_test_dc4ae26a10a2c1068f61917425a827c1fc70bc5a")  
PAYSTACK_BASE_URL = "https://api.paystack.co"

# Initialize transaction
@router.post("/paystack/initialize")
async def initialize_transaction(data: dict):
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{PAYSTACK_BASE_URL}/transaction/initialize",
            json=data,
            headers=headers
        )
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()

# Callback route (for redirect after payment)
@router.get("/paystack/callback")
async def paystack_callback(reference: str):
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}"
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{PAYSTACK_BASE_URL}/transaction/verify/{reference}",
            headers=headers
        )
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    # You can process the payment status here
    return response.json()

# Webhook endpoint
@router.post("/paystack/webhook")
async def paystack_webhook(request: Request):
    payload = await request.json()
    # Optionally, verify the signature here using request.headers.get('x-paystack-signature')
    # Process the webhook event
    # For demonstration, just return the payload
    return JSONResponse(content=payload, status_code=status.HTTP_200_OK)

# Optional: Route to get public key for frontend
@router.get("/paystack/public-key")
async def get_paystack_public_key():
    if not PAYSTACK_PUBLIC_KEY:
        raise HTTPException(status_code=500, detail="Paystack public key not set")
    return {"public_key": PAYSTACK_PUBLIC_KEY}
