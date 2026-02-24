from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import Security
from app.auth.schema import EmployeeLogin, TokenResponse
from app.employees.model import Employee


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
def login(data: EmployeeLogin, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.username == data.username).first()

    if not employee:
        raise HTTPException(detail="Invalid credentials")

    if not Security.verify_password(data.password, employee.password):
        raise HTTPException(detail="Invalid credentials")

    token = Security.create_token({"sub": employee.username})
    return {"access_token": token}
