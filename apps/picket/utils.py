def get_attr_display(instance, log_field):
    get_log_field_display = 'get_%s_display' % log_field
    attr_name = get_log_field_display if \
        get_log_field_display in dir(instance) else log_field
    attr = getattr(instance, attr_name)
    return callable(attr) and attr() or attr
