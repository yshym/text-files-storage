from django_elasticsearch_dsl import DocType, Index, fields
from .models import File


textfile = Index('textfiles')

textfile.settings(
    number_of_shards=1,
    number_of_replicas=0
)

@textfile.doc_type
class FileDocument(DocType):
    class Meta:
        model = File

        fields = (
            'name',
            'description',
        )
