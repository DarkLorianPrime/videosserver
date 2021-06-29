from django import template

register = template.Library()


@register.filter
def joiner(values_list, separator):
    return separator.join(values_list)
