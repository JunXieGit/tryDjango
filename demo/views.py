from django.shortcuts import render


def home(request):
    context_dict = dict()
    return render(request, 'home.html', context_dict)
