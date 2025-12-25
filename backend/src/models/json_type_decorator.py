import json
from sqlalchemy.types import TypeDecorator, JSON
from typing import Type, Any
from pydantic import BaseModel


class JSONType(TypeDecorator):
    """
    A generic JSON TypeDecorator that works with multiple Pydantic models and supports nullable fields.
    """

    impl = JSON

    def __init__(self, model_class: Type[BaseModel], *args, **kwargs):
        """
        :param model_class: The Pydantic model class to serialize/deserialize.
        """
        super().__init__(*args, **kwargs)
        self.model_class = model_class

    def process_bind_param(self, value: Any, dialect):
        """
        Serialize the Pydantic object or dict to a JSON string before storing it in the database.
        """
        if not value:
            return dict()
        if isinstance(value, BaseModel):
            return value.model_dump()
        return value

    def process_result_value(self, value: Any, dialect):
        """
        Deserialize JSON string from the database into the specified Pydantic model.
        """
        if not value:
            return None
        if isinstance(value, str):
            value = json.loads(value)
        return self.model_class(**value)
