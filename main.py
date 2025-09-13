from bson import ObjectId
from fastapi import FastAPI, APIRouter, HTTPException, Query
from config import collection
from database.schema import all_employees, individual_data
from database.models import Employee, EmployeeUpdate


app = FastAPI()

router = APIRouter()

@router.get("/employees/{employee_id}")
async def get_employees(employee_id: str):
    try:
        existing_employee = collection.find_one({"employee_id": employee_id})
        if not existing_employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        resp = individual_data(existing_employee)
        return {"status code" : 200, "employee" : resp}
    except Exception as e:
        return HTTPException(500, detail = f"Some error occured {e}")


@router.post("/employees")
async def create_employee(new_employee: Employee):
    try:
        existing_employee = collection.find_one({"employee_id": new_employee.employee_id})
        if existing_employee:
            raise HTTPException(status_code=400, detail="Employee ID already exists.")
        resp = collection.insert_one(dict(new_employee))
        return {"status code":200, "id" : str(resp.inserted_id)}
    except Exception as e:
        return HTTPException(500, detail = f"Some error occured {e}")
    

@router.put("/{employee_id}")
async def update_employee(employee_id: str, updated_employee: EmployeeUpdate):
    update_data = {k: v for k, v in dict(updated_employee).items() if v is not None}

    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    updated_employee = collection.find_one_and_update(
        {"employee_id": employee_id},
        {"$set": update_data},
        return_document=True
    )

    if not updated_employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    return individual_data(updated_employee)

@router.delete("/{employee_id}")
async def delete_employee(employee_id: str):
    try:
        id= ObjectId(employee_id)
        existing_employee = collection.find_one({"_id": id})
        if not existing_employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        resp = collection.delete_one({"_id": id})
        return {"status code" : 200, "message" : "Employee Deleted successfully"}
    except Exception as e:
        return HTTPException(500, detail = f"Some error occured {e}")

# ET /employees?department=Engineering
@router.get("/employees")
async def list_employee_by_department(q: str = ""):
    try:
        employee_list = list(collection.find({"department": q}))
        if len(employee_list) == 0:
            return HTTPException(status_code=404, detail="Employee not found")
        resp = all_employees(employee_list)
        return {"status code" : 200, "list" : resp}
    except Exception as e:
        return HTTPException(500, detail = f"Some error occured {e}")



@app.get("/employees/avg-salary")
def avg_salary_by_department():
    try:
        pipeline = [
            {
                "$group": {
                    "_id": "$department",        
                    "avg_salary": {"$avg": "$salary"}  
                }
            },
            {
                "$project": {
                    "_id": 0,                    
                    "department": "$_id",
                    "avg_salary": 1          
                }
            }
        ]

        result = list(collection.aggregate(pipeline)) 

        if len(result) == 0:  
            raise HTTPException(status_code=404, detail="No employees found")

        return result

    except HTTPException:  
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Some error occurred: {e}")
    

@app.get("/employees/search")
def search_employees_by_skill(skill: str = Query(..., description="Skill to search for")):
    try:
        
        employees_cursor = collection.find({"skills": skill})
        employees_list = list(employees_cursor)  

        if len(employees_list) == 0:
            raise HTTPException(status_code=404, detail=f"No employees found with skill '{skill}'")

        
        for emp in employees_list:
            emp["_id"] = str(emp["_id"])

        return {"status_code": 200, "data": employees_list}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Some error occurred: {e}")
    

app.include_router(router)
