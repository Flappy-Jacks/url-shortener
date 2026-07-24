import os
import secrets
import string

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import select

import models
import schemas
from database import engine, get_db, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortener")

# Allow the local Vite dev server to call this API.
extra_origins = os.environ.get("ALLOWED_ORIGINS", "")
allowed_origins = ["http://localhost:5173"] + [
    o.strip() for o in extra_origins.split(",") if o.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ALPHABET = string.ascii_letters + string.digits

# create a random code. retry if it already exists
def generate_code(db: Session, length: int = 6) -> str:
    for _ in range(10):
        code = "".join(secrets.choice(ALPHABET) for _ in range(length))
        exists = db.execute(
            select(models.Link).where(models.Link.code == code)
        ).scalar_one_or_none()
        if not exists:
            return code
    raise HTTPException(500, "Could not generate a unique code, try again")

# create a link. if a custom code is entered, check. otherwise create a fresh random one
@app.post("/api/links", response_model=schemas.LinkOut)
def create_link(payload: schemas.LinkCreate, db: Session = Depends(get_db)):
    if payload.custom_code:
        existing = db.execute(
            select(models.Link).where(models.Link.code == payload.custom_code)
        ).scalar_one_or_none()
        if existing:
            raise HTTPException(409, "That custom code is already taken")
        code = payload.custom_code
    else:
        code = generate_code(db)

    link = models.Link(code=code, original_url=str(payload.original_url))
    db.add(link)
    db.commit()
    db.refresh(link)
    return link

# fetches a complete list of links
@app.get("/api/links", response_model=list[schemas.LinkOut])
def list_links(db: Session = Depends(get_db)):
    return db.execute(
        select(models.Link).order_by(models.Link.created_at.desc())
    ).scalars().all()

# fetches a specific link based off its code
@app.get("/api/links/{code}", response_model=schemas.LinkOut)
def get_link_stats(code: str, db: Session = Depends(get_db)):
    link = db.execute(
        select(models.Link).where(models.Link.code == code)
    ).scalar_one_or_none()
    if not link:
        raise HTTPException(404, "No link found for that code")
    return link

# redirects to the original url
@app.get("/{code}")
def redirect_to_original(code: str, db: Session = Depends(get_db)):
    link = db.execute(
        select(models.Link).where(models.Link.code == code)
    ).scalar_one_or_none()
    if not link:
        raise HTTPException(404, "No link found for that code")
    link.click_count += 1
    db.commit()
    return RedirectResponse(url=link.original_url)
