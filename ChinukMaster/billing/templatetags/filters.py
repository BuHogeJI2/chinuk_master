from django import template

register = template.Library()

@register.filter(name='times')
def times(value):
    return range(1, value+1)

@register.filter(name='pos_3_times')
def pos_3_times(value):
    return range(1, 4)

@register.filter(name='neg_3_times')
def neg_3_times(value):
    return range(-3, 0)