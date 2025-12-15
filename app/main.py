import os
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request, BackgroundTasks
from dotenv import load_dotenv

from app.data_sources import load_from_excel, load_from_sql
from email_templates import render_email
from app.senders.gmail_sender import send_gmail_html
from app.senders.outlook_sender import send_outlook_html

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/send")
def send(
    background: BackgroundTasks,
    provider: str = Form(...),          # "gmail" or "outlook"
    to_email: str = Form(...),
    subject: str = Form(...),
    source: str = Form(...),            # "excel" or "sql"
    excel_path: str = Form(""),
    sql_query: str = Form(""),
):
    # 1) Load data
    if source == "excel":
        df = load_from_excel(excel_path)
    else:
        df = load_from_sql(sql_query)

    # 2) Render email
    html = render_email(subject, df)

    # 3) Send in background
    if provider == "gmail":
        background.add_task(send_gmail_html, to_email, subject, html)
    else:
        background.add_task(send_outlook_html, to_email, subject, html)

    return {"status": "queued"}
