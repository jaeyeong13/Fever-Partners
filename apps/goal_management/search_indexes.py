from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Goal

@registry.register_document
class GoalDocument(Document):
    class Index:
        name = 'goals'
        settings = {'number_of_shards': 1, 'number_of_replicas': 0}

    tags = fields.NestedField(properties={
        'name': fields.TextField(),
    })

    activityTags = fields.NestedField(properties={
        'name': fields.TextField(),
    })

    class Django:
        model = Goal
        fields = [
            'favor_offline',
            'title',
            'content',
        ]
