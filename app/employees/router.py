from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.employees.schema import EmployeeCreate, EmployeeResponse
from app.employees.service import EmployeeService
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/employees", tags=["Employees"])


def get_employee_service(db: Session = Depends(get_db)) -> EmployeeService:
    return EmployeeService(db)


@router.post("/", response_model=EmployeeResponse)
def create_employee(
    data: EmployeeCreate, service: EmployeeService = Depends(get_employee_service)
):

    try:
        return service.create_employee(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/")
def get_all_employees(
    current_user=Depends(get_current_user),
    service: EmployeeService = Depends(get_employee_service),
):

    return service.get_all_employees()


@router.get("/{employee_id}")
def get_employee(
    employee_id: int, service: EmployeeService = Depends(get_employee_service)
):
    try:
        return service.get_employee(employee_id)
    except ValueError as e:
        raise HTTPException(detail=str(e))


@router.put("/{employee_id}")
def update_employee(
    employee_id: int,
    data: EmployeeCreate,
    service: EmployeeService = Depends(get_employee_service),
):
    try:
        return service.update_employee(employee_id, data)
    except ValueError as e:
        raise HTTPException(detail=str(e))


@router.delete("/{employee_id}")
def delete_employee(
    employee_id: int, service: EmployeeService = Depends(get_employee_service)
):
    try:
        service.delete_employee(employee_id)
        return {"message": "Employee deleted successfully"}
    except ValueError as e:
        raise HTTPException(detail=str(e))
