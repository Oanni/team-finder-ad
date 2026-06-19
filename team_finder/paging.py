from django.core.paginator import Paginator


def slice_for_page(http_request, queryset, chunk_size):
    """Возвращает страницу queryset с учётом GET-параметра page."""

    pager = Paginator(queryset, chunk_size)
    requested_index = http_request.GET.get('page')
    return pager.get_page(requested_index)
