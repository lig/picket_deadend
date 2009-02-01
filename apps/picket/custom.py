def order_by_FIELD(query_set, direction='ASC'):
    return query_set.order_by('%sFIELD' % ('-' if direction=='DESC' else ''))
