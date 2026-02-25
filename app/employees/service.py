from app.core.security import Security
from app.employees.model import Employee
from app.employees.repository import EmployeeRepository
from app.employees.schema import EmployeeCreate, EmployeeUpdate


class EmployeeService:
    """
    Service layer responsible for employee business logic.

    This class acts as an intermediary between API routes and the
    repository layer. It handles validation, password hashing,
    and application-level rules before interacting with the database.
    """

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

    def update_employee(self, employee_id: int, data: EmployeeUpdate):
        employee = self.repository.get_by_id(employee_id)
        if not employee:
            raise ValueError("employee not found")

        update_data = data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            if key == "password":
                if value:
                    value = Security.hash_password(value)
                else:
                    continue
            setattr(employee, key, value)

        return self.repository.update(employee)

    def delete_employee(self, employee_id: int):
        employee = self.repository.get_by_id(employee_id)
        if not employee:
            raise ValueError("employee not found")
        self.repository.delete(employee)
