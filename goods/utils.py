def sort_by_name(obj, sort_direction):
    if sort_direction == 'asc':
        return obj.order_by('name')
    elif sort_direction == 'desc':
        return obj.order_by('-name')


def sort_by_created_at(obj, sort_direction):
    if sort_direction == 'asc':
        return obj.order_by('created_at', 'name')
    elif sort_direction == 'desc':
        return obj.order_by('-created_at', 'name')


def sort_by_price(obj, sort_direction):
    if sort_direction == 'asc':
        return obj.order_by('price', 'purchase_count', 'name')
    elif sort_direction == 'desc':
        return obj.order_by('-price', 'purchase_count', 'name')


def sort_by_purchase_count(obj, sort_direction):
    if sort_direction == 'asc':
        return obj.order_by('purchase_count', 'name')
    elif sort_direction == 'desc':
        return obj.order_by('-purchase_count', 'name')


def sort_util(request, obj):
    sort_by = request.GET.get('sort_by')
    sort_direction = request.GET.get('sort_direction')
    if sort_by == 'name':
        return sort_by_name(obj, sort_direction)
    elif sort_by == 'created_at':
        return sort_by_created_at(obj, sort_direction)
    elif sort_by == 'price':
        return sort_by_price(obj, sort_direction)
    elif sort_by == 'purchase_count':
        return sort_by_purchase_count(obj, sort_direction)
    return obj
