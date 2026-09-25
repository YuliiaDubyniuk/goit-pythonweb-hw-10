from datetime import date, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import extract
from sqlalchemy.orm import Session
from database.db import get_db
from database.models import Contact, User
from schemas.contact import ContactCreate, ContactResponse, ContactUpdate
from services.auth import get_current_user


router = APIRouter(
    prefix="/contacts",
    tags=["Contacts"],
)


@router.get("/", response_model=list[ContactResponse])
def get_contacts(
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Contact).filter(
        Contact.user_id == current_user.id
    )

    if first_name:
        query = query.filter(Contact.first_name.ilike(f"%{first_name}%"))

    if last_name:
        query = query.filter(Contact.last_name.ilike(f"%{last_name}%"))

    if email:
        query = query.filter(Contact.email == email.lower())

    return query.all()


@router.post("/", response_model=ContactResponse, status_code=201)
def create_contact(
    contact: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_contact = Contact(
        first_name=contact.first_name,
        last_name=contact.last_name,
        email=contact.email,
        phone=contact.phone,
        birth_date=contact.birth_date,
        additional_data=contact.additional_data,
        user_id=current_user.id,
    )

    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)

    return new_contact


@router.get("/birthdays", response_model=list[ContactResponse])
def get_upcoming_birthdays(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    today = date.today()
    end_date = today + timedelta(days=7)

    start_month = today.month
    start_day = today.day

    end_month = end_date.month
    end_day = end_date.day

    birth_month = extract("month", Contact.birth_date)
    birth_day = extract("day", Contact.birth_date)

    if start_month == end_month:
        contacts = (
            db.query(Contact)
            .filter(
                Contact.user_id == current_user.id,
                birth_month == start_month,
                birth_day > start_day,
                birth_day <= end_day,
            )
            .all()
        )
    else:
        contacts = (
            db.query(Contact)
            .filter(
                Contact.user_id == current_user.id,
                (
                    (birth_month == start_month)
                    & (birth_day > start_day)
                )
                |
                (
                    (birth_month == end_month)
                    & (birth_day <= end_day)
                )
            )
            .all()
        )

    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
def get_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    contact = db.query(Contact).filter(
        Contact.id == contact_id,
        Contact.user_id == current_user.id,
    ).first()

    if contact is None:
        raise HTTPException(
            status_code=404,
            detail="Contact not found",
        )

    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
def update_contact(
    contact_id: int,
    contact_data: ContactUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    contact = db.query(Contact).filter(
        Contact.id == contact_id, Contact.user_id == current_user.id,).first()

    if contact is None:
        raise HTTPException(
            status_code=404,
            detail="Contact not found",
        )

    contact.first_name = contact_data.first_name
    contact.last_name = contact_data.last_name
    contact.email = contact_data.email
    contact.phone = contact_data.phone
    contact.birth_date = contact_data.birth_date
    contact.additional_data = contact_data.additional_data

    db.commit()
    db.refresh(contact)

    return contact


@router.delete("/{contact_id}", status_code=204)
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    contact = db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == current_user.id,).first()

    if contact is None:
        raise HTTPException(
            status_code=404,
            detail="Contact not found",
        )

    db.delete(contact)
    db.commit()
