from django.shortcuts import render


def index(request):
    return render(request, 'vital_records/index.html')
