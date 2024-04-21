from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
def home(request: Request) -> Response:
    """Home page."""
    return templates.TemplateResponse("home.jinja", {"request": request})


@app.get("/ticket/")
async def buy_ticket(request: Request) -> Response:
    """Buy ticket page."""
    return templates.TemplateResponse("buy-ticket.jinja", {"request": request})
