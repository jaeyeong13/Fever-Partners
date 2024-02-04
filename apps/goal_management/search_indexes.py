from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import *

@registry.register_document
class GoalDocument(Document):
    class Index:
        name = 'goals'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    tags = fields.NestedField(properties={
        'tag_name': fields.KeywordField(),
    })

    activityTags = fields.NestedField(properties={
        'tag_name': fields.KeywordField(),
    })

    class Django:
        model = Goal
        fields = [
            'favor_offline',
            'title',
            'content',
        ]

@registry.register_document
class TagDocument(Document):
    class Index:
        name = 'tags'

    tag_name = fields.TextField()

    class Django:
        model = Tag

@registry.register_document
class ActivityTagDocument(Document):
    class Index:
        name = 'activity_tags'

    tag_name = fields.TextField()

    class Django:
        model = ActivityTag