from django import template
from django.http import QueryDict

register = template.Library()

@register.filter
def update_page_param(request, page_num):
    full_path = request.get_full_path()
    query_string_index = full_path.find('?')
    if query_string_index != -1:
        path, query_string = full_path.split('?', 1)
        params = QueryDict(query_string).copy()
    else:
        path = full_path
        params = QueryDict().copy()
    params['page'] = page_num
    return '{}?{}'.format(path, params.urlencode())