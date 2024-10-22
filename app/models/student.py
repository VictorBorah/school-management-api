from pydantic import BaseModel

class StudentBase(BaseModel):           
    std_name: str
    std_class: int
    std_registration_no: str
    std_phone: str

class StudentCreate(StudentBase):    
    pass

class StudentUpdate(StudentBase):
    pass

class Student(StudentBase):
    id:str        
    std_name: str
    std_class: int
    std_registration_no: str
    std_phone: str  

class Config:
    from_attributes = True