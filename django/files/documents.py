from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import File


@registry.register_document
class FileDocument(Document):
    class Index:
        name = 'textfiles'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = File

        fields = (
            'name',
            'description',
        )
