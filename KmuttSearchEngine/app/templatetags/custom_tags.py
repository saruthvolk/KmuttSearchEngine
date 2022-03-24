from django import template
register = template.Library()

@register.filter
def in_list(value, the_list):
    for x in the_list:
        if (str(value) == str(x)):
            return True
    else:
        return False

@register.filter
def check(value, check_value):

    if (str(value) == str(check_value)):
        return True
    else:
        return False