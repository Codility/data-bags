from django import template
from django.utils.html import format_html
from .jsonify import jsonify

register = template.Library()


DEFAULT_FORMATTED_VALUE = jsonify(None)


def render_data_bag(name, data, is_data_formatted=False):
    id = 'data-bag-' + name

    return format_html(
        '<script type="application/json" id="{}">{}</script>',
        id, data if is_data_formatted else jsonify(data)
    )


class DataBagNode(template.Node):
    def __init__(self, name, data_name, default_value):
        self.name = name
        self.data_name = data_name
        self.default_value = default_value

    def render(self, context):
        if self.data_name in context:
            data = context[self.data_name]
            formatted_data = jsonify(data)
        else:
            formatted_data = self.default_value

        return render_data_bag(self.name, formatted_data, is_data_formatted=True)


@register.tag
def data_bag(parser, token):
    args = token.split_contents()

    if len(args) < 3:
        raise template.TemplateSyntaxError(
            'Data bag requires at least two arguments'
        )

    if len(args) > 4:
        raise template.TemplateSyntaxError(
            'Data bag requires at most three arguments'
        )

    name = args[1]
    data_name = args[2]
    default_value = args[3] if len(args) == 4 else DEFAULT_FORMATTED_VALUE

    if not (name[0] == name[-1] and name[0] in ('"', "'") and len(name) > 2):
        raise template.TemplateSyntaxError(
            'The first argument (data bag id) should be a non-empty quoted string'
        )

    return DataBagNode(name[1:-1], data_name, default_value)
