from typing import Optional, List
from pydantic import BaseModel


#{"page":1,"limit":20,"filePath":"C:\\Users\\Lion\\Desktop\\log"}
class LogListItem(BaseModel):
    page: int
    limit: int
    filePath: str


#{"path":"C:\\Users\\Lion\\Desktop\\log","selectedLog":[{"{"name":"&pgm..log","modified_time":"2020-05-29 08:36:43","filepath":"C:\\Users\\Lion\\Desktop\\log"}
class logfileInfo(BaseModel):
    name: str
    modified_time: str
    filepath: str


class LogAnaItem(BaseModel):
    path: str
    selectedLog: List[logfileInfo] = None


#{"fullpath":"C:\\Users\\Lion\\Desktop\\log\\&pgm..log","errIndex":"221"}
class LogErrDetail(BaseModel):
    fullpath: str
    errIndex: str


class DataSetListItem(BaseModel):
    page: int
    limit: int
    basePath: str
    cmpPath: str


class sDataset(BaseModel):
    base: str
    cmp: str


class DataSetCMPItem(BaseModel):
    basePath: str
    cmpPath: str
    selectedDataset: List[sDataset] = None


class CMP_ResultStatus(BaseModel):
    ticket_id: str


class CMP_Single_Detail(BaseModel):
    base: str
    cmp: str


