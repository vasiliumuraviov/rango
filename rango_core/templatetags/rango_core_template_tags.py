from django import template

from rango_core import models

register = template.Library()


@register.inclusion_tag('rango_core/categories.html')
def get_category_query(current_category=None):
	return {'categories': models.Category.objects.all(), 'current_category': current_category}
