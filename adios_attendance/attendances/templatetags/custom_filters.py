from django import template

register = template.Library()

@register.filter
def korean_day(value):
    days = {
        'Monday': '월',
        'Tuesday': '화',
        'Wednesday': '수',
        'Thursday': '목',
        'Friday': '금',
        'Saturday': '토',
        'Sunday': '일',
    }
    return days.get(value, value)