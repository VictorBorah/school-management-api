from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from ..config.database import get_db, TABLE_STUDENTS
from ..models.student import StudentCreate, StudentUpdate, Student
from typing import List, Dict
from xata.client import XataClient
from datetime import datetime

router = APIRouter()

@router.get("/", tags=["home"])
async def home() -> Dict[str, str]:
    """
    Home page route that provides basic API information
    """
    return {
        "message": "Welcome to School Management System API",
        "version": "1.0.0",
        "documentation": "/docs",
        "health_check": "/health",
        "timestamp": datetime.now().isoformat()
    }

@router.get("/health", tags=["system"])
async def health_check(db: XataClient = Depends(get_db)) -> Dict[str, str]:
    """
    Health check route that tests database connectivity.
    Tests connection to tbl_students table.
    """
    try:
        # Try to perform a simple database query on tbl_students
        response = db.data().query(TABLE_STUDENTS, {
            "page": {
                "size": 1
            }
        })
        
        return {
            "status": "healthy",
            "database": "connected",
            "table": TABLE_STUDENTS,
            "timestamp": datetime.now().isoformat(),
            "message": "System is operational"
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "database": "disconnected",
                "table": TABLE_STUDENTS,
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "message": "Database connection failed"
            }
        )

@router.post("/students/", response_model=None,response_model_exclude_unset=True)
async def create_student(student: StudentCreate, db: XataClient = Depends(get_db)):
    """
    Create a new student record in tbl_students
    """
    try:
        # Create record in tbl_students
        result = db.records().insert(TABLE_STUDENTS, {
            "std_name": student.std_name,
            "std_class": student.std_class,
            "std_registration_no": student.std_registration_no,
            "std_phone": student.std_phone
        })
        return result
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=f"Failed to create student in {TABLE_STUDENTS}: {str(e)}"
        )

@router.get("/students/", response_model=List[Student])
async def get_students(db: XataClient = Depends(get_db)):
    """
    Get all students from tbl_students
    """
    try:
        results = db.data().query(TABLE_STUDENTS)
        return results["records"]
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=f"Failed to fetch students from {TABLE_STUDENTS}: {str(e)}"
        )

@router.get("/students/{reg_no}", response_model=Student)
async def get_student(reg_no: str, db: XataClient = Depends(get_db)):
    """
    Get a specific student by registration number from tbl_students
    """
    try:
        result = db.data().query(TABLE_STUDENTS, {
            "filter": {
                "std_registration_no": reg_no
            }
        })
        
        if not result["records"]:
            raise HTTPException(
                status_code=404, 
                detail=f"Student not found in {TABLE_STUDENTS}"
            )
        return result["records"][0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=f"Failed to fetch student from {TABLE_STUDENTS}: {str(e)}"
        )

@router.put("/students/{reg_no}", response_model=Student)
async def update_student(reg_no: str, student: StudentUpdate, db: XataClient = Depends(get_db)):
    """
    Update a student's information in tbl_students
    """
    try:
        # First find the record in tbl_students
        existing = db.data().query(TABLE_STUDENTS, {
            "filter": {
                "std_registration_no": reg_no
            }
        })
        
        if not existing["records"]:
            raise HTTPException(
                status_code=404, 
                detail=f"Student not found in {TABLE_STUDENTS}"
            )
        
        # Update the record in tbl_students
        result = db.data().update(TABLE_STUDENTS, existing["records"][0]["id"], {
            "std_name": student.std_name,
            "std_class": student.std_class,
            "std_registration_no": student.std_registration_no,
            "std_phone": student.std_phone
        })
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=f"Failed to update student in {TABLE_STUDENTS}: {str(e)}"
        )

@router.delete("/students/{reg_no}")
async def delete_student(reg_no: str, db: XataClient = Depends(get_db)):
    """
    Delete a student record from tbl_students
    """
    try:
        # First find the record in tbl_students
        existing = db.data().query(TABLE_STUDENTS, {
            "filter": {
                "std_registration_no": reg_no
            }
        })
        
        if not existing["records"]:
            raise HTTPException(
                status_code=404, 
                detail=f"Student not found in {TABLE_STUDENTS}"
            )
        
        # Delete the record from tbl_students
        db.data().delete(TABLE_STUDENTS, existing["records"][0]["id"])
        return {
            "message": f"Student deleted successfully from {TABLE_STUDENTS}",
            "registration_no": reg_no
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=f"Failed to delete student from {TABLE_STUDENTS}: {str(e)}"
        )