from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class Student(BaseModel):
    name: str
    section: str='F'                #default value set to F
    age: Optional[int]=None         #if not option/default than consider required
    email:Optional[EmailStr]=None   #in-built validation for email, 
    cgpa:float= Field(gt=0,le=10,default=5,description="CGPA of students")

new_student={"name":"Somu", "age":'32',"cgpa":9.9}  #pydantic is smart enough to do implicit conver. 32 to int
st=Student(**new_student) #st is an object of class Student all fields are its method access by dot
print(st)
print(st.age)

#convert to json
student_json=st.model_dump_json()
print(student_json)
