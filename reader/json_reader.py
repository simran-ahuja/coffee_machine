import json
from marshmallow import ValidationError
from . import IReader
from errors import ReaderException


class JSONReader(IReader):
    """
    JSONReader is a JSON input based implementation of
    IReader
    """

    def __init__(self, schema):
        """
        param:schema - marshmallow schema for input to adhere to
        """
        self.schema = schema

    def read(self, file="./input/input.json"):
        """
        param:file - string for file path to read input from
        """
        try:
            f = open(file)
            input_json = json.loads(f.read())
            f.close()

            return self.schema().load(input_json)

        except Exception as exc:
            raise ReaderException(
                f"Failed to read records from input file: {str(exc)}")
