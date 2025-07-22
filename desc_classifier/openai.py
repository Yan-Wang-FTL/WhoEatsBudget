from openai import OpenAI

from desc_classifier import BaseDescClassifier


class OpenAIDescClassifier(BaseDescClassifier):

    def __init__(self, model: str):
        self._model = model
        self._instructions = \
        """
        # Identity

        You are a financial transaction classifier. 
        You will receive a transaction description.
        Your task is to categorize the transaction description into one of the predefined categories.
        
        # Instructions

        * The transaction description is a string which contains multiple fields, separated by spaces.
        * First you need to find the merchant name, city, and province from the transaction description. The merchant name may span multiple fields.
        * Classify the transaction description based on the merchant type. For example, if the description is "Starbucks Toronto ON", classify it as "dining".
        * Classify the transaction description into the most appropriate category from the following list:
            - groceries
            - dining
            - transportation
            - utilities
            - entertainment
            - healthcare
            - travel
            - one-time expenses
        * If the description does not fit any of the categories, classify it as "other".

        # Example
        <user_query>
        The transaction description to be classified is: Rogers Communications Toronto ON
        </user_query>
        
        <assistant_response>
        utilities
        </assistant_response>
        """

    def classify(self, description: str) -> str:
        responses = OpenAI().responses.create(
            model=self._model,
            instructions=self._instructions,
            input=f"The transaction description to be classified is: {description}",
        )

        return responses.output_text