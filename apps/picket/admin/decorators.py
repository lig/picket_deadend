from django.contrib.auth.decorators import user_passes_test


def superuser_required(func):
    return user_passes_test(lambda user: user.is_superuser)(func)
