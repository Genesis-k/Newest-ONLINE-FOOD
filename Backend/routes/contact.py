from fastapi import APIRouter, HTTPException
from database import db
from schemas import ContactForm

router = APIRouter(prefix="/api/contact", tags=["Contact"])

@router.post("/")
async def submit_contact_form(contact: ContactForm):
    """Submit a contact form message."""
    try:
        # Insert the contact form data into the database
        await db.contact.insert_one(contact.dict())
        return {"message": "Your message has been received. We'll get back to you soon."}
    except Exception as e:
        # Handle any errors that occur during the database operation
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")