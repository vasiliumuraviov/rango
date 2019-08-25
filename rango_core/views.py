from django.shortcuts import render

from . import models


def index(request):
    category_query = models.Category.objects.order_by('-likes')[:5]
    pages_query = models.Page.objects.order_by('-views')[:5]

    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!',
                    'categories': category_query,
                    'pages': pages_query, }

    return render(request, 'rango_core/index.html', context=context_dict)


def about(request):
    return render(request, 'rango_core/about.html', context={})


def show_category(request, category_name_slug):
    context = {}

    try:
        category = models.Category.objects.get(slug=category_name_slug)
        pages = models.Page.objects.filter(category=category)
        context['pages'] = pages
        context['category'] = category

    except models.Category.DoesNotExist:
        context['pages'] = None
        context['category'] = None

    return render(request, 'rango_core/category.html', context=context)
