from django import template
from django.utils.translation import ugettext_lazy as _


register = template.Library()


@register.simple_tag
def join_strings(strs, last_join_word, join_word):
    """
        Joins a list of strings with 'join_word' and the last one
        'last_join_word' and the returns the string
    """

    if not join_word:
        join_word = ', '

    if not last_join_word:
        last_join_word = join_word

    join_word = _(join_word)
    last_join_word = _(last_join_word)

    final_str = join_word.join(strs[:-1])  # Join except last one
    if len(strs) > 1:
        final_str = final_str + "{last_join_word}{error}".format(
            last_join_word=last_join_word,
            error=strs[-1]
        )
    else:
        final_str = strs[0]

    return final_str
