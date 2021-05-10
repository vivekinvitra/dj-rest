import json

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from home.forms import SearchForm, SignUpForm
from home.models import Setting, ContactForm, ContactFormMessage, UserProfile
from product.models import Product, Category, Images, Comment


def index(request):
    sliderData = Product.objects.all()[:3]
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    ourFavorites = Product.objects.all().order_by('-rate')[:3]
    ourLatestDeliciousFoods = Product.objects.all().order_by('-id')[:3]
    current_user = request.user
    if current_user.id is not None:
        profile = UserProfile.objects.get(user_id=current_user.id)
    else:
        profile = None
    context = {
        'setting': setting,
        'category': category,
        'page': 'home',
        'sliderData': sliderData,
        'ourFavorites': ourFavorites,
        'ourLatestDeliciousFoods': ourLatestDeliciousFoods,
        'profile': profile,
    }
    return render(request, 'index.html', context)


def aboutus(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    if current_user.id is not None:
        profile = UserProfile.objects.get(user_id=current_user.id)
    else:
        profile = None
    context = {'setting': setting, 'category': category, 'profile': profile, 'page': 'aboutus'}
    return render(request, 'aboutus.html', context)


def references(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    if current_user.id is not None:
        profile = UserProfile.objects.get(user_id=current_user.id)
    else:
        profile = None
    context = {'setting': setting, 'category': category, 'profile': profile, 'page': 'references'}
    return render(request, 'references.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactFormMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Your message sent successfully. Thanks.")
            return HttpResponseRedirect('/contact')

    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    if current_user.id is not None:
        profile = UserProfile.objects.get(user_id=current_user.id)
    else:
        profile = None
    form = ContactForm()
    context = {'setting': setting, 'category': category, 'profile': profile, 'form': form}
    return render(request, 'contact.html', context)


def faq(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    if current_user.id is not None:
        profile = UserProfile.objects.get(user_id=current_user.id)
    else:
        profile = None
    context = {'setting': setting, 'category': category, 'profile': profile, 'page': 'faq'}
    return render(request, 'faq.html', context)


def category_products(request, id, slug):
    setting = Setting.objects.get(pk=1)
    products = Product.objects.filter(category_id=id)
    category = Category.objects.all()
    current_user = request.user
    if current_user.id is not None:
        profile = UserProfile.objects.get(user_id=current_user.id)
    else:
        profile = None
    categorydata = Category.objects.get(pk=id)
    context = {'setting': setting, 'products': products, 'category': category, 'profile': profile, 'categorydata': categorydata}
    return render(request, 'products.html', context)


def product_detail(request, id, slug):
    setting = Setting.objects.get(pk=1)
    product = Product.objects.get(pk=id)
    category = Category.objects.all()
    current_user = request.user
    if current_user.id is not None:
        profile = UserProfile.objects.get(user_id=current_user.id)
    else:
        profile = None
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id, status='True')
    context = {'setting': setting, 'category': category, 'product': product, 'profile': profile, 'images': images, 'comments': comments}
    return render(request, 'product_detail.html', context)


def product_search(request):
    setting = Setting.objects.get(pk=1)
    current_user = request.user
    if current_user.id is not None:
        profile = UserProfile.objects.get(user_id=current_user.id)
    else:
        profile = None
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query']
            catid = form.cleaned_data['catid']
            if catid == 0:
                products = Product.objects.filter(title__icontains=query)
            else:
                products = Product.objects.filter(title__icontains=query, category_id=catid)
            context = {'setting': setting, 'products': products, 'profile': profile, 'category': category}
            return render(request, 'product_search.html', context)
    return HttpResponseRedirect('/')


def product_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        product = Product.objects.filter(title__icontains=q)
        results = []
        for rs in product:
            product_json = {}
            product_json = rs.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Your username or password is incorrect.")
            return HttpResponseRedirect('/login')
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    if current_user.id is not None:
        profile = UserProfile.objects.get(user_id=current_user.id)
    else:
        profile = None
    context = {'setting': setting, 'category': category, 'profile': profile, 'page': 'login'}
    return render(request, 'login.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password1 = request.POST['password1']
            user = authenticate(request, username=username, password=password1)
            login(request, user)
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "images/users/user.png"
            data.save()
            return HttpResponseRedirect('/')

    form = SignUpForm()
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    if current_user.id is not None:
        profile = UserProfile.objects.get(user_id=current_user.id)
    else:
        profile = None
    context = {'setting': setting, 'category': category, 'profile': profile, 'form': form, 'page': 'login'}
    return render(request, 'signup.html', context)
