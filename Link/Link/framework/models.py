from Link import db
import datetime
from Link.helper.mongo_to_dict import mongo_to_dict
from flask_mongoengine import Document, DynamicDocument


class NubDocument(Document):

    def to_dict(self, excluded_fields):
        return mongo_to_dict(self, excluded_fields)


class DynamicNubDocument(DynamicDocument):

    def to_dict(self, excluded_fields):
        return mongo_to_dict(self, excluded_fields)
