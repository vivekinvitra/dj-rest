from django.http import HttpResponse
from django.shortcuts import render

from home.models import Setting, UserProfile
from product.models import Category


def index(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    current_user = request.user
    if current_user.id is not None:
        profile = UserProfile.objects.get(user_id=current_user.id)
    else:
        profile = None
    context = {'setting': setting, 'category': category, 'profile': profile, 'page': 'userprofile'}
    return render(request, 'user_profile.html', context)
