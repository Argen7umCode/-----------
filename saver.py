from abc import ABC, abstractmethod
from json import dump
from csv import csv


class Saver(ABC):

    @abstractmethod
    def save(data, path):
        pass

class JSONSaver(Saver):
    
    @staticmethod
    def save(data, path) -> None:
        with open(path, 'w', encoding='utf-8') as file:
            dump(data, file, indent=4, ensure_ascii=False)

class CSVSaver(Saver):
    
    @staticmethod
    def save(data, path) -> None:
        with open(path, 'w', newline='\n') as file:
            csv.writer(file).writerows(data)
