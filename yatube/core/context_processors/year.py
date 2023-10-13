from datetime import datetime, date


def year(request):
    """Функция возвращает текущий год"""
    return {
        'year': datetime.utcnow().year
    }


def get_author_age(request):
    # По идее, теперь возраст должен считаться по UTC
    today = datetime.utcnow().date()
    birthday = date(1993, 7, 10)
    age = (today.year - birthday.year
           - ((today.month, today.day) < (birthday.month, birthday.day)))
    return {
        'age': age
    }
