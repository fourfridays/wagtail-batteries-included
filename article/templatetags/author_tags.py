from django import template
from article.models import Author

register = template.Library()


# Authors snippets
@register.inclusion_tag('article/tags/authors.html', takes_context=True)
def authors(context):
    return {
        'authors': Author.objects.all(),
        'context': context,
        'request': context['request'],
    }
