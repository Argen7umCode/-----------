from abc import ABC, abstractmethod
from typing import Any
from dataclasses import asdict, astuple


class Converter(ABC):

    @abstractmethod
    def _convert_one(data: Any):
        pass            

    @abstractmethod
    def _convert_many(data: Any):
        pass
    
    @classmethod
    def convert(cls, data: Any, *args, **kwargs):
        return cls._convert_many(data) if isinstance(data, list)\
            else cls._convert_one(data)

class ConverterDataclassToJSON(Converter):
    
    @staticmethod
    def _convert_one(data_object: Any) -> dict:
        return asdict(data_object)
    
    @classmethod
    def _convert_many(cls, data_objects: [Any]) -> [dict]:
        return [cls._convert_one(obj) for obj in data_objects]


class ConverterDataclassToCSV(Converter):
    
    @staticmethod
    def _convert_one(data_object: Any, sep : str = ',') -> str:
        return sep.join(map(str, astuple(data_object)))     

    @classmethod
    def _convert_many(cls, data_objects: [Any], sep : str = ',') -> str:
        return '\n'.join(cls._convert_one(data_object, sep) 
                          for data_object in data_objects)
    @classmethod
    def convert(cls, data: Any, sep : str = ',', *args, **kwargs):
        return cls._convert_many(data, sep) if isinstance(data, list)\
            else cls._convert_one(data, sep)
    