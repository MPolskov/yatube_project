# Для импорта в тесты:
# from .constants import (
#     USER_USERNAME,
#     SIGNUP_URL_NAME,
#     LOGIN_URL_NAME,
#     LOGOUT_URL_NAME,
#     PASSWORD_CHANGE_URL_NAME,
#     PASSWORD_CHANGE_COMPLETE_URL_NAME,
#     PASSWORD_RESET_FORM_URL_NAME,
#     PASSWORD_RESET_DONE_URL_NAME,
#     PASSWORD_RESET_CONFIRM_URL_NAME,
#     PASSWORD_RESET_COMPLETE_URL_NAME,

#     SIGNUP_TEMPLATE,
#     LOGIN_TEMPLATE,
#     LOGOUT_TEMPLATE,
#     PASSWORD_CHANGE_TEMPLATE,
#     PASSWORD_CHANGE_COMPLETE_TEMPLATE,
#     PASSWORD_RESET_FORM_TEMPLATE,
#     PASSWORD_RESET_DONE_TEMPLATE,
#     PASSWORD_RESET_CONFIRM_TEMPLATE,
#     PASSWORD_RESET_COMPLETE_TEMPLATE
# )

USER_USERNAME = 'TestUser'

SIGNUP_URL_NAME = 'users:signup'
LOGIN_URL_NAME = 'users:login'
LOGOUT_URL_NAME = 'users:logout'
PASSWORD_CHANGE_URL_NAME = 'users:password_change'
PASSWORD_CHANGE_COMPLETE_URL_NAME = 'users:password_change_complete'
PASSWORD_RESET_FORM_URL_NAME = 'users:password_reset_form'
PASSWORD_RESET_DONE_URL_NAME = 'users:password_reset_done'
PASSWORD_RESET_CONFIRM_URL_NAME = 'users:password_reset_confirm'
PASSWORD_RESET_COMPLETE_URL_NAME = 'users:password_reset_complete'

SIGNUP_TEMPLATE = 'users/signup.html'
LOGIN_TEMPLATE = 'users/login.html'
LOGOUT_TEMPLATE = 'users/logged_out.html'
PASSWORD_CHANGE_TEMPLATE = 'users/password_change_form.html'
PASSWORD_CHANGE_COMPLETE_TEMPLATE = 'users/password_change_done.html'
PASSWORD_RESET_FORM_TEMPLATE = 'users/password_reset_form.html'
PASSWORD_RESET_DONE_TEMPLATE = 'users/password_reset_done.html'
PASSWORD_RESET_CONFIRM_TEMPLATE = 'users/password_reset_confirm.html'
PASSWORD_RESET_COMPLETE_TEMPLATE = 'users/password_reset_complete.html'
