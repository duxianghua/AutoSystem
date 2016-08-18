from django.shortcuts import render_to_response
from django.shortcuts import render

def page_404(request):
    return render_to_response('page_404.html')


def page_500(request):
    return render_to_response('page_500.html')