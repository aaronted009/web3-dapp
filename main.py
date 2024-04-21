from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os
from web3 import Web3

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")
infura_api = os.getenv("INFURA_API")
wallet_address = os.getenv("WALLET_ADDRESS")
private_key = os.getenv(
    "PRIVATE_KEY"
)  # That key should be provided by user but as this is a demo project, we don't want any trust issue from users as this info is confidential.


@app.get("/")
def home(request: Request) -> Response:
    """Home page."""
    return templates.TemplateResponse("home.jinja", {"request": request})


@app.get("/ticket/")
async def buy_ticket(request: Request) -> Response:
    """Buy ticket page."""
    return templates.TemplateResponse("buy-ticket.jinja", {"request": request})


@app.post("/ticket/")
async def buy_tickett(request: Request) -> Response:
    """Proceed with ticket buy."""
    w3 = Web3(Web3.HTTPProvider(infura_api))
    nonce = w3.eth.get_transaction_count(wallet_address)
    transaction = {
        "nonce": nonce,
        "to": wallet_address,
        "value": w3.to_wei(1, "ether"),
        "gasPrice": w3.eth.gas_price,
    }
    gas = w3.eth.estimate_gas(transaction)
    transaction.update({"gas": gas})
    if w3.is_connected():
        signed_transaction = w3.eth.account.sign_transaction(transaction, private_key)
        transaction_hash = w3.eth.send_raw_transaction(signed_transaction)
        receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)
    else:
        receipt = "No transaction done."
    return templates.TemplateResponse(
        "buy-ticket.jinja", {"request": request, "transaction_receipt": receipt}
    )
