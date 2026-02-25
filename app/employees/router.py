from pathlib import Path

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.core.database import get_db
from app.employees.schema import (EmployeeCreate, EmployeeResponse,
                                  EmployeeUpdate)
from app.employees.service import EmployeeService

BASE_DIR = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

router = APIRouter(prefix="/employees", tags=["Employees"])


def get_employee_service(db: Session = Depends(get_db)) -> EmployeeService:
    return EmployeeService(db)


@router.get("/page", response_class=None)
def employee_page(
    request: Request, service: EmployeeService = Depends(get_employee_service)
):
    employees = service.get_all_employees()
    return templates.TemplateResponse(
        "employees.html",
        {"request": request, "employees": employees},
    )


@router.get("/create")
def create_employee_page(request: Request):
    return templates.TemplateResponse(
        "create_employee.html",
        {"request": request, "errors": None},
    )


@router.post("/create")
def create_employee(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    phone_number: str = Form(...),
    age: int = Form(...),
    role: str = Form(...),
    salary: float = Form(...),
    employment_type: str = Form(...),
    contract_end_date: str = Form(None),
    service: EmployeeService = Depends(get_employee_service),
):
    try:
        data = EmployeeCreate(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            age=age,
            role=role,
            salary=salary,
            employment_type=employment_type,
            contract_end_date=contract_end_date or None,
        )

        service.create_employee(data)

        return RedirectResponse("/employees/page", status_code=303)

    except Exception as e:
        return templates.TemplateResponse(
            "create_employee.html",
            {"request": request, "errors": [str(e)]},
        )


@router.get("/edit/{employee_id}")
def edit_employee_page(
    employee_id: int,
    request: Request,
    service: EmployeeService = Depends(get_employee_service),
):
    try:
        employee = service.get_employee(employee_id)
        return templates.TemplateResponse(
            "edit_employee.html",
            {"request": request, "employee": employee, "errors": None},
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/edit/{employee_id}")
def update_employee(
    employee_id: int,
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    phone_number: str = Form(...),
    age: int = Form(...),
    role: str = Form(...),
    salary: float = Form(...),
    employment_type: str = Form(...),
    contract_end_date: str = Form(None),
    service: EmployeeService = Depends(get_employee_service),
):
    try:
        data = EmployeeUpdate(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            age=age,
            role=role,
            salary=salary,
            employment_type=employment_type,
            contract_end_date=contract_end_date or None,
        )

        service.update_employee(employee_id, data)

        return RedirectResponse("/employees/page", status_code=303)

    except Exception as e:
        employee = service.get_employee(employee_id)
        return templates.TemplateResponse(
            "edit_employee.html",
            {
                "request": request,
                "employee": employee,
                "errors": [str(e)],
            },
        )


@router.post("/delete/{employee_id}")
def delete_employee(
    employee_id: int,
    service: EmployeeService = Depends(get_employee_service),
):
    try:
        service.delete_employee(employee_id)
        return RedirectResponse("/employees/page", status_code=303)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
