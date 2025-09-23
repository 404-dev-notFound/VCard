from pydantic import BaseModel, EmailStr, HttpUrl, field_validator, Field
from typing import Optional, List
import re

class BusinessCardData(BaseModel):
    """Pydantic model for structured business card data"""
    first_name: str = Field(..., description="First name of the person")
    middle_name: Optional[str] = Field(None, description="Middle name of the person")
    last_name: str = Field(..., description="Last name of the person")
    company_name: str = Field(..., description="Company name")
    position: str = Field(..., description="Job position/title")
    department: Optional[str] = Field(None, description="Department")
    mobile: Optional[List[str]] = Field(None, description="Mobile phone numbers")
    telephone: Optional[List[str]] = Field(None, description="Work phone numbers")
    email: Optional[List[EmailStr]] = Field(None, description="Email addresses")
    website: Optional[List[HttpUrl]] = Field(None, description="Website URLs")
    address: Optional[str] = Field(None, description="Business address")
    extension: Optional[str] = Field(None, description="Phone extension")
    notes: Optional[str] = Field(None, description="Additional information")

    # MODIFIED: Updated validator to handle lists of strings
    @field_validator("mobile", "telephone", mode='before')
    @classmethod
    def clean_phone_numbers(cls, v):
        if not v:
            return v
        if not isinstance(v, list):
            # If for some reason we still get a string, wrap it in a list
            v = [v]
        
        cleaned_numbers = []
        for number in v:
            if isinstance(number, str):
                # Keep only digits and the '+' symbol
                digits = re.sub(r'[^\d+]', '', number)
                if digits:
                    cleaned_numbers.append(digits)
        return cleaned_numbers if cleaned_numbers else None

class OCRResponse(BaseModel):
    """Response model for OCR results"""
    success: bool
    raw_text: str
    structured_data: Optional[BusinessCardData] = None
    vcard: Optional[str] = None
    error_message: Optional[str] = None

class OCRRequest(BaseModel):
    """Request model for OCR processing"""
    include_vcard: bool = Field(True, description="Whether to generate vCard")
    include_raw_text: bool = Field(True, description="Whether to include raw OCR text")
