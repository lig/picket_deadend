"""
Copyright 2008-2009 Serge Matveenko

This file is part of Picket.

Picket is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Picket is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Picket.  If not, see <http://www.gnu.org/licenses/>.
"""

from django.conf import settings
from django.contrib.sites.models import Site
from django.template import Library, Node, Variable, TemplateSyntaxError
from django.template.defaultfilters import stringfilter
from django.template.loader import get_template

""" @note: relative import will not work here """
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
                bugs = Variable('bugs').resolve(context)
                if len(bugs.query.order_by) > 0:
                    context['column_sort'] = {
                        column_name: 'ASC',
                        '-%s' % column_name: 'DESC',
                    }.get(bugs.query.order_by[0], None)
                else:
                    context['column_sort'] = None
                context['column_link_sort'] = {
                    'ASC': 'DESC',
                    'DESC': 'ASC',
                    None: 'ASC',
                }[context['column_sort']]
            else:
                t = get_template('picket/bugs_list_header_unsortable_inc.html')
            return t.render(context)
        except TemplateSyntaxError, e:
            if settings.TEMPLATE_DEBUG:
                raise
            return ''

class FieldValueNode(Node):
    def __init__(self, field):
        self.field = Variable(field)
        
    def render(self, context):
        try:
            field = self.field.resolve(context)
            if hasattr(field.field, 'choices'):
                field_choices = dict(field.field.choices)
                field_data = field.data or []
                field_values = (field_choices[int(key)] for key in field_data)
                return ', '.join(field_values)
            else:
                return field.data or ''
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

def do_field_value(parser, token):
    
    bits = token.contents.split()
    
    if len(bits) != 2:
        raise TemplateSyntaxError('field_value accepts exactly one argument')
    
    return FieldValueNode(bits[1])

register.tag('include_join', do_include_join)
register.tag('column_header', do_column_header)
register.tag('field_value', do_field_value)


@stringfilter
def site_url_filter(value):
    return 'http://%s%s' % (Site.objects.get_current().domain, value)

register.filter('site_url', site_url_filter)
