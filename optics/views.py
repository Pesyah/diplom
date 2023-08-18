from django.views.generic import DetailView, ListView
from .models import Optics
from django.shortcuts import render

class OpticsDetailView(DetailView):
    model = Optics
    template_name = 'optics_detail_view.html'  

class OpticsListView(ListView):
    model = Optics
    template_name = 'optics_list.html'  
    
def mainPage(request):
    return render(request, 'index.html',)