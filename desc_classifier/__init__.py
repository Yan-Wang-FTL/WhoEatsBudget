from typing import List
from abc import ABC, abstractmethod

__all__ = ["BaseDescClassifier"]


class BaseDescClassifier(ABC):
    """
    Base class for description classifiers.
    """
    @staticmethod
    def get_classifier(backend: str, *args, **kwargs) -> 'BaseDescClassifier':
        match backend:
            case "openai":
                from .openai import OpenAIDescClassifier
                return OpenAIDescClassifier(*args, **kwargs)
            case _:
                raise NotImplementedError(f"Classifier backend '{backend}' is not implemented.")
        
    @abstractmethod
    def classify(self, descriptions: List[str]) -> List[str]:
        """
        Classify a list of transaction descriptions into categories.
        
        :param descriptions: List of transaction descriptions to classify.
        :return: List of categories corresponding to the input descriptions.
        """
        pass
    