from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from . import forms, models


def get_server_side_cookies(request, cookie, default_value=None):
    tweaked_cookie = request.session.get(cookie, default_value)
    return tweaked_cookie


def visitor_cookie_handler(request):
    # getting the number of user's visits from cookie
    # if no such cookie --> user's first visit
    visits = int(get_server_side_cookies(request, 'visits', '1'))

    # getting the datetime of user's visits from cookie
    # if no such cookie --> user's first visit datetime
    last_visit_cookie = get_server_side_cookies(request, 'last_visit', str(datetime.now()))

    last_visit_time = datetime.strptime(last_visit_cookie[:-7],  # getting rid of micro/nano secs
                                        '%Y-%m-%d %H:%M:%S')  # and parsing previous visit time

    # if MORE THAN ONE DAY has passed:
    if (datetime.now() - last_visit_time).days >= 1:
        visits += 1
        request.session['last_visit'] = str(datetime.now())

    else:
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits


def about(request):
    visitor_cookie_handler(request)

    about_context = {
        'visits': request.session.get('visits'),
    }

    return render(request, 'rango_core/about.html', context=about_context)


@login_required
def restricted(request):
    return render(request, 'rango_core/restricted.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(to=reverse('rango_core:index'))


def user_login(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)

                return redirect(reverse('rango_core:index'))

            else:
                return HttpResponse('Your Rango account is disabled.')

        else:
            print(f'Invalid login details: {username}, {password}')
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'rango_core/login.html')


def register(request):
    registered = False

    if request.method == 'POST':

        user_form = forms.UserForm(request.POST)
        profile_form = forms.UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            # SAVING THE USER ---------------------------------
            user = user_form.save(commit=True)

            # set_password hashes the password
            user.set_password(user.password)
            user.save()

            # SAVING THE USER PROFILE --------------------------
            # Since we need to set the user attribute ourselves,
            # we set commit=False. This delays saving the model
            # until we're ready to avoid integrity problems.
            profile: models.UserProfile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES.get('picture')

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = forms.UserForm()
        profile_form = forms.UserProfileForm()

    return render(request, 'rango_core/register.html', {'user_form': user_form,
                                                        'profile_form': profile_form,
                                                        'registered': registered})


def index(request):
    category_query = models.Category.objects.order_by('-likes')[:5]
    pages_query = models.Page.objects.order_by('-views')[:5]

    visitor_cookie_handler(request)

    context_dict = {
        'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!',
        'categories': category_query,
        'pages': pages_query,
    }

    response = render(request, 'rango_core/index.html', context=context_dict)

    return response


def add_category(request):
    form = forms.CategoryForm()

    if request.method == 'POST':
        form = forms.CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            return redirect(to=reverse('rango_core:index'))

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
        form = forms.PageForm(request.POST)

        if form.is_valid():

            if category:
                page = form.save(commit=False)

                page.category = category
                page.views = 0

                page.save()

                return redirect(reverse('rango_core:show-category', kwargs={'category_name_slug': category_name_slug}))

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
