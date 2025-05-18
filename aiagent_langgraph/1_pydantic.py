# Pydantic Basics: Creating and Using Models  
from pydantic import BaseModel  
  
class Person(BaseModel):  
  name:str  
  age:int  
  city:city  
  
person = Person(name="Ryan", age=35,city="Boston")  
# raise validation error  
person = Person(name="Ryan", age=35,city=12)  
    
# Model with Optional Field  
from typing import Optional  
    
class Employee(BaseModel):  
    id: int  
    name: str  
    department: str  
    salary: Optional[float] = None  
    is_active: Optional[bool] = True  
    
emp1 = Employee(id=1, name="John", department="IT")  
    
from typing import List  
    
class Classroom(BaseModel):  
    room_number: str  
    students: List[str]  
    
# Model with Nested Model  
class Address(BaseModel):  
    street: str  
    city: str  
    zipcode: str  
    
class Customer(BaseModel):  
    name:str  
    address: Address  
    
customer = Customer(name="John",  address={"street": "main street", "city": "Boston", "zipcode": "01981"})  
    
#Pydantic Fields: Customization and Constraints  
from pydantic import BaseModel, Field  
class Item(BaseModel):  
    name:str=Field(min_length=2, max_length=50)  
    price:float=Field(gt=0, le=1000) # >0 and <=1000  
    quantity:int=Field(default=1, description="item description") 
