import math
from django.core.paginator import Paginator

def make_pagination_range(
    page_range,
    qty_pages,
    current_page,
):
    # math.ceil arredonda numero quebrado pra cima
    middle_range = math.ceil(qty_pages / 2)
    start_range = current_page - middle_range
    stop_range = current_page + middle_range
    total_pages = len(page_range)
    # abs transforma número negativo em positivo e vice versa
    start_range_offset = abs(start_range) if start_range < 0 else 0

    if start_range < 0:
        start_range = 0
        stop_range += start_range_offset

    if stop_range >= total_pages:
        start_range = start_range - abs(total_pages - stop_range)
    # o slice ":" faz uma lista com um intervalo do número inical + 1 até o número final - 1
    # Exemplo: [4:8] retorna [5. 6, 7] 
    pagination = page_range[start_range:stop_range]
    return {
        'pagination': pagination,
        'page_range': page_range,
        'qty_pages': qty_pages,
        'current_page': current_page,
        'total_pages': total_pages,
        'start_range': start_range,
        'stop_range': stop_range,
        'first_page_out_of_range': current_page > middle_range,
        'last_page_out_of_range': stop_range < total_pages,
    }   

def make_pagination(request, queryset, per_page, qty_pages=4):
    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1

    paginator = Paginator(queryset, per_page)
    page_obj = paginator.get_page(current_page)

    pagination_range = make_pagination_range(
        paginator.page_range,
        qty_pages,
        current_page
    )

    return page_obj, pagination_range