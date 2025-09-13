Name : Yogi Modi
email: yogimodi003@gmail.com

Employee Management API (FastAPI + MongoDB)
===========================================

This project is a simple Employee Management API built using FastAPI and MongoDB.
It supports CRUD operations, search, aggregations.

------------------------------------------------------------
1. REQUIREMENTS
------------------------------------------------------------
- Python 3.10 or higher
- MongoDB (local or Atlas)
- Git (to clone the repo)

------------------------------------------------------------
2. INSTALLATION
------------------------------------------------------------
1. Clone the repository:
   git clone https://github.com/yogi0398/fastapi_assessment.git

2. Create a virtual environment:
   python -m venv venv

3. Activate the environment:
   Windows:
       venv\Scripts\activate
   Linux/Mac:
       source venv/bin/activate

4. Install dependencies:
   pip install -r requirements.txt

------------------------------------------------------------
3. RUNNING THE SERVER
------------------------------------------------------------
Start the FastAPI app with:

   uvicorn main:app --reload

The server will run at:
   http://127.0.0.1:8000

API documentation:
   Swagger UI: http://127.0.0.1:8000/docs
   ReDoc:      http://127.0.0.1:8000/redoc
