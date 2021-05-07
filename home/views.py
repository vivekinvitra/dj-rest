from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Avg

from home.models import Setting, ContactForm, ContactFormMessage
from product.models import Product, Category, Images, Comment


def index(request):
    sliderData = Product.objects.all()[:3]
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    ourFavorites = Product.objects.all()[:3]
    ourLatestDeliciousFoods = Product.objects.all().order_by('-id')[:3]
    context = {
                'setting': setting,
                'category': category,
                'page': 'home',
                'sliderData': sliderData,
                'ourFavorites': ourFavorites,
                'ourLatestDeliciousFoods': ourLatestDeliciousFoods,
    }
    return render(request, 'index.html', context)


def aboutus(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting, 'category': category, 'page': 'aboutus'}
    return render(request, 'aboutus.html', context)


def references(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting, 'category': category, 'page': 'references'}
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
    form = ContactForm()
    context = {'setting': setting, 'category': category, 'form': form}
    return render(request, 'contact.html', context)


def faq(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    context = {'setting': setting, 'category': category, 'page': 'faq'}
    return render(request, 'faq.html', context)


def category_products(request, id, slug):
    setting = Setting.objects.get(pk=1)
    products = Product.objects.filter(category_id=id)
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    context = {'setting': setting, 'products': products, 'category': category, 'categorydata': categorydata}
    return render(request, 'products.html', context)


def product_detail(request, id, slug):
    setting = Setting.objects.get(pk=1)
    product = Product.objects.get(pk=id)
    category = Category.objects.all()
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id, status='True')
    context = {'setting': setting, 'category': category, 'product': product, 'images': images, 'comments': comments}
    return render(request, 'product_detail.html', context)