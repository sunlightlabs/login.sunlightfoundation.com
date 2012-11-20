from django import template
import datetime as dt
import humanize

register = template.Library()


def human_posix(posix):
    posix = int(posix)
    d = dt.date.fromtimestamp(posix)
    return humanize.naturaltime(d)

register.filter('human_posix', human_posix)
register.filter('hp', human_posix)
