# import allure
# import functools
#
# def auto_step(func):
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         with allure.step(func.__name__):
#             return func(*args, **kwargs)
#     return wrapper
#
# def auto_step_class(cls):
#     for attr_name, attr in cls.__dict__.items():
#         if callable(attr) and not attr_name.startswith("__"):
#             setattr(cls, attr_name, auto_step(attr))
#     return cls