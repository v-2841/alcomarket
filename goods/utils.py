def sort_util(request, obj):
    sort_by = request.GET.get('sort_by')
    sort_direction = request.GET.get('sort_direction')
    if sort_by == 'name':
        if sort_direction == 'asc':
            obj = obj.order_by('name')
        elif sort_direction == 'desc':
            obj = obj.order_by('-name')
    elif sort_by == 'created_at':
        if sort_direction == 'asc':
            obj = obj.order_by('created_at', 'name')
        elif sort_direction == 'desc':
            obj = obj.order_by('-created_at', 'name')
    elif sort_by == 'price':
        if sort_direction == 'asc':
            obj = obj.order_by('price', 'purchase_count', 'name')
        elif sort_direction == 'desc':
            obj = obj.order_by('-price', 'purchase_count', 'name')
    elif sort_by == 'purchase_count':
        if sort_direction == 'asc':
            obj = obj.order_by('purchase_count', 'name')
        elif sort_direction == 'desc':
            obj = obj.order_by('-purchase_count', 'name')
    return obj
