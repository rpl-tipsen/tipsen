from django.shortcuts import render

# Create your views here.


def home(request):

    user = request.user

    print(user)
    return render(request, 'home/index.html', {'user': user})
