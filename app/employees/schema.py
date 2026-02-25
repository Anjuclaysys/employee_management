import re
from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator


class EmployeeBase(BaseModel):
    """
    Base schema containing common employee attributes.
    """

    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    age: int
    role: str
    salary: float
    employment_type: str
    contract_end_date: Optional[date] = None

    @field_validator("age")
    def validate_age(cls, v):
        if v <= 0:
            raise ValueError("age must be positive")
        return v

    @field_validator("salary")
    def validate_salary(cls, v):
        if v <= 0:
            raise ValueError("Salary must be positive")
        return v

    @field_validator("phone_number")
    def validate_phone(cls, v):
        if not re.match(r"^\+?[0-9]{10,15}$", v):
            raise ValueError("Invalid phone number")
        return v

    @model_validator(mode="after")
    def validate_contract(self):
        if self.employment_type == "Contract" and not self.contract_end_date:
            raise ValueError("Contract employees must have contract_end_date")
        return self


class EmployeeCreate(EmployeeBase):
    """
    Schema used when creating a new employee.
    """

    username: str
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v.encode("utf-8")) > 72:
            raise ValueError("Password cannot exceed 72 bytes")
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class EmployeeUpdate(EmployeeBase):
    """
    Schema used when updating an existing employee.
    """

    password: Optional[str] = None

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if v is None:
            return v
        if len(v.encode("utf-8")) > 72:
            raise ValueError("Password cannot exceed 72 bytes")
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class EmployeeResponse(EmployeeBase):
    """
    Schema returned in API responses.
    """

    id: int

    class Config:
        from_attributes = True
