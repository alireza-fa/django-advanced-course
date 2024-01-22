from abc import ABC, abstractmethod


class Log(ABC):
    @abstractmethod
    def debug(self, message: str, category: str, sub_category: str):
        pass

    @abstractmethod
    def info(self, message: str, category: str, sub_category: str):
        pass

    @abstractmethod
    def warn(self, message: str, category: str, sub_category: str):
        pass

    @abstractmethod
    def error(self, message: str, category: str, sub_category: str):
        pass
