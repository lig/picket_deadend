from django.conf import settings
from django.template import Library, Node, Variable, TemplateSyntaxError
from django.template.loader import get_template

from apps.picket import custom
from apps.picket.models import Bug

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
        except:
            return '' # Fail silently for invalid included templates.

class ColumnHeaderNode(Node):
    def __init__(self, column_name):
        self.column_name = Variable(column_name)
    
    def render(self, context):
        try:
            column_name = self.column_name.resolve(context)
            """ @todo: refactor template names """
            if Bug.field_is_sortable(column_name):
                t = get_template('picket/bugs_list_header_sortable_inc.html')
            else:
                t = get_template('picket/bugs_list_header_unsortable_inc.html')
            return t.render(context)
        except TemplateSyntaxError, e:
            if settings.TEMPLATE_DEBUG:
                raise
            return ''

def do_include_join(parser, token):
    """
    Loads a template from joined path and renders it with the current context.

    Example::

        {% include "foo/_include" %}
        {% include "foo/" some "_include" %}
    """
    bits = token.contents.split()
        
    return IncludeJoinNode(bits[1:])

def do_column_header(parser, token):
    
    bits = token.contents.split()
    
    if len(bits) != 2:
        raise TemplateSyntaxError('column_header accepts exactly one argument')
    
    return ColumnHeaderNode(bits[1])

register.tag('include_join', do_include_join)
register.tag('column_header', do_column_header)
