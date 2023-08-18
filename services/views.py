from django.views.generic import DetailView, ListView
from .models import Services

class ServicesDetailView(DetailView):
    model = Services
    template_name = 'Services_detail_view.html'  

class ServicesListView(ListView):
    model = Services
    template_name = 'Services_list.html'