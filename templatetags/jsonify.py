# http://djangosnippets.org/snippets/201/
from django.conf import settings
from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.template import Library
import json
from django.utils.text import mark_safe

register = Library()


@register.filter
def jsonify_html(object):
    # Allow for safe embedding in HTML content and attributes.
    if isinstance(object, QuerySet):
        result = serialize('json', object)
    else:
        result = json.dumps(object, indent=2 if settings.DEBUG else None)
    return result


@register.filter
def jsonify(object):
    jsonified = jsonify_html(object)

    # Allow for safe embedding in <script> tags,
    # see http://stackoverflow.com/questions/4176511/embedding-json-objects-in-script-tags
    jsonified = jsonified.replace('<', '\\u003c').replace('>', '\\u003e')

    return mark_safe(jsonified)
