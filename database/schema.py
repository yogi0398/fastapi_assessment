from datetime import date

def individual_data(employee):
    return {
        "id": str(employee["_id"]),
        "name" : employee["name"],
        "department" : employee["department"],
        "salary" : employee["salary"],
        "joining_date" : employee["joining_date"],
        "skills" : employee["skills"] 
    }

def all_employees(employees):
    return [individual_data(employee) for employee in employees]