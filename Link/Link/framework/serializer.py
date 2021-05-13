from mongoengine import Document
from mongoengine import QuerySet
from Link.helper.mongo_to_dict import mongo_to_dict
import json


class Serializer:

    def __init__(self, document_cls):
        self.document_cls = document_cls

    def _post_processing(self, obj, result_dict):
        # Use this as a postprocessor to parse more information like from Reference Fields
        pass

    def serialize(self, data, exclude_fields=[]):
        if not data:
            return None
        if isinstance(data, QuerySet):
            # parse through every field in fields and convert to python object.
            result = []
            for obj in data:
                conv_to_dict = self._to_dict(obj=obj, exclude_fields=exclude_fields)
                # add a function to do post processing functionalities.
                self._post_processing(obj, conv_to_dict)
                result.append(conv_to_dict)
        elif isinstance(data, Document):
            # do something
            conv_to_dict = self._to_dict(obj=data, exclude_fields=exclude_fields)
            self._post_processing(data, conv_to_dict)
            result = conv_to_dict
        elif isinstance(data, list):
            result = []
            for obj in data:
                conv_to_dict = self._to_dict(obj=obj, exclude_fields=exclude_fields)
                self._post_processing(obj, conv_to_dict)
                result.append(conv_to_dict)
        else:
            raise ValueError("Invalid value to Serializer")

        return json.dumps(result)

    @staticmethod
    def _to_dict(obj, exclude_fields=[]):
        return mongo_to_dict(obj, exclude_fields)
