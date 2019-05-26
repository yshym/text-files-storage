def validate_file_extensions(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.txt', '.doc', '.odt', '.md']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')
