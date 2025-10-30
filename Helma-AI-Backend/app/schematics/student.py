from pydantic import BaseModel, Field
from bson import ObjectId

class StudentBase(BaseModel):
    name: str
    surname: str
    school: str
    school_id: str
    Tc_no: str
    birth_date: str  # Doğum tarihi (YYYY-MM-DD formatında)
    tel_no: str
    address: str
    age: int
    grade: int
    average: float
    classroom: str
    parent_id: str
    bus_id: str | None = None  # Otobüs ID'si opsiyon
    is_turc: bool
    gender: str


class StudentCreate(StudentBase):
    pass

class StudentRead(StudentBase):
    id: str = Field(alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True