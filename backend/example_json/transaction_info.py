from pydantic import BaseModel, Field
from pydantic import BaseModel
import datetime


class TransactionModel(BaseModel):
    State: object = Field(...)
    BankState: object = Field(...)
    ApprovalFY: int = Field(...)
    Term: int = Field(...)
    NoEmp: int = Field(...)
    UrbanRural: int = Field(...)
    RevLineCr: int = Field(...)
    LowDoc: int = Field(...)
    DisbursementGross: float = Field(...)
    GrAppv: float = Field(...)
    Industry: object = Field(...)
    IsFranchise: int = Field(...)
    NewBusiness: int = Field(...)
    DisbursementFY: int = Field(...)
    DaysToDisbursement: int = Field(...)
    SBA_AppvPct: float = Field(...)
    AppvDisbursed: int = Field(...)
    RealEstate: int = Field(...)
    GreatRecession: int = Field(...)


    class Config:
       populate_by_name = True
       arbitrary_types_allowed = True
       json_schema_extra = {
           "example": {
               "State": "AK",
                "BankState" : "AK",
                "ApprovalFY": 1994,
                "Term": 84,
                "NoEmp": 5,
                "UrbanRural": 0 ,
                "RevLineCr": 0,
                "LowDoc":0,
                "DisbursementGross":60000.0	, 
                'GrAppv':60000.0, 
                'Industry':"Retail_trade"	,
                'IsFranchise':0, 
                'NewBusiness':1, 
                'DisbursementFY':1997,
                'DaysToDisbursement':870, 
                'SBA_AppvPct':0.80, 
                'AppvDisbursed':1,
                'RealEstate':0, 
                'GreatRecession':1

           }
       }