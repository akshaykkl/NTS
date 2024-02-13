from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    current_user = request.user
    if current_user.is_authenticated and current_user.groups.filter(name= 'Teacher').exists():
        return render(request, 'Notification/home.html')
    else:
        return HttpResponse('hi')

    