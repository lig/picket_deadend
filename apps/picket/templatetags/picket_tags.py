from django.conf import settings
from django.template import Library, Node, Variable, TemplateSyntaxError
from django.template.loader import get_template

register = Library()

class IncludeJoinNode(Node):
    def __init__(self, template_name_chunks):
        self.template_name_chunks = [Variable(template_name_chunk) for
            template_name_chunk in template_name_chunks]

    def render(self, context):
        try:
            template_name = ''.join(template_name_chunk.resolve(context) for
                template_name_chunk in self.template_name_chunks)
            t = get_template(template_name)
            return t.render(context)
        except TemplateSyntaxError, e:
            if settings.TEMPLATE_DEBUG:
                raise
            return ''
#        except:
#            return '' # Fail silently for invalid included templates.

def do_include_join(parser, token):
    """
    Loads a template from joined path and renders it with the current context.

    Example::

        {% include "foo/_include" %}
        {% include "foo/" some "_include" %}
    """
    bits = token.contents.split()
        
    return IncludeJoinNode(bits[1:])

register.tag('includejoin', do_include_join)
