from django import template
import locale

register = template.Library()


def digit_separate(value):
    """
    Add space between three zeros
    Example: 1000000.00 -> 1 000 000.00
    """
    str_val = str(value)
    len_val = len(str_val)
    number = int(str_val[0:len_val - 3])
    remainder = str_val[len_val - 3:len_val]
    locale.setlocale(locale.LC_ALL, '')
    return locale.format('%d', number, grouping=True) + remainder


def reverse_slicing(s):
    return s[::-1]


register.filter('digit_separate', digit_separate)
