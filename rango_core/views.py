from django.shortcuts import render, redirect
from django.urls import reverse

from . import forms
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


def add_category(request):
    form = forms.CategoryForm()

    if request.method == 'POST':
        form = forms.CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            return index(request)

        else:
            print(form.errors)

    return render(request, 'rango_core/add_category.html', {'form': form})


def add_page(request, category_name_slug):
    try:
        category = models.Category.objects.get(slug=category_name_slug)
    except models.Category.DoesNotExist:
        category = None

    form = forms.PageForm()
    if request.method == "POST":
        print(f'my method {request.method}!')
        form = forms.PageForm(request.POST)

        if form.is_valid():
            print('im valid, lol!')
            if category:
                page = form.save(commit=False)

                page.category = category
                page.views = 0

                page.save()

                return redirect(reverse('rango_core:show-category',
                                        kwargs={'category_name_slug': category_name_slug}))

        else:
            print(form.errors)

    context = {'form': form, 'category': category}
    return render(request, 'rango_core/add_page.html', context=context)


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
