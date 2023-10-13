from django.core.paginator import Paginator
import logging


def create_logger(logger_name):
    logger = logging.getLogger(logger_name)
    if not logger.handlers:
        logger.addHandler(logging.StreamHandler())

    class Logger:

        def __enter__(self):
            logger.setLevel(logging.DEBUG)
            return logger

        def __exit__(self, exc_type, exc_val, exc_tb):
            logger.setLevel(logging.CRITICAL)

    return Logger()


def get_paginator(request, post_list, num_post_per_page):
    paginator = Paginator(post_list, num_post_per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
