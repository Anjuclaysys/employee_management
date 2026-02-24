from app.employees.repository import EmployeeRepository
from app.employees.model import Employee
from app.employees.schema import EmployeeCreate
from app.core.security import Security


class EmployeeService:
    def __init__(self, db):
        self.repository = EmployeeRepository(db)

    def create_employee(self, data: EmployeeCreate):
        if self.repository.get_by_username(data.username):
            raise ValueError("username already exists")
        data_dict = data.model_dump()
        data_dict["password"] = Security.hash_password(data.password)
        employee = Employee(**data_dict)
        return self.repository.create(employee)

    def get_all_employees(self):
        return self.repository.get_all()

    def get_employee(self, employee_id: int):
        employee = self.repository.get_by_id(employee_id)
        if not employee:
            raise ValueError("employee not found")
        return employee

    def update_employee(self, employee_id: int, data: EmployeeCreate):
        employee = self.repository.get_by_id(employee_id)
        if not employee:
            raise ValueError("employee not found")

        for key, value in data.model_dump().items():
            setattr(employee, key, value)

        return self.repository.update(employee)

    def delete_employee(self, employee_id: int):
        employee = self.repository.get_by_id(employee_id)
        if not employee:
            raise ValueError("employee not found")
        self.repository.delete(employee)
