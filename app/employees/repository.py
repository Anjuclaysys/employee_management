from sqlalchemy.orm import Session
from sqlalchemy import select
from app.employees.model import Employee


class EmployeeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, employee: Employee):
        self.db.add(employee)
        self.db.commit()
        self.db.refresh(employee)
        return employee

    def get_all(self):
        return self.db.execute(select(Employee)).scalars().all()

    def get_by_id(self, employee_id: int):
        return self.db.get(Employee, employee_id)

    def get_by_username(self, username: str):
        return self.db.execute(
            select(Employee).where(Employee.username == username)
        ).scalar_one_or_none()

    def update(self, employee: Employee):
        self.db.commit()
        self.db.refresh(employee)
        return employee

    def delete(self, employee: Employee):
        self.db.delete(employee)
        self.db.commit()
