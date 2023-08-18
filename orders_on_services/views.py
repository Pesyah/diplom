from django.views.generic import DetailView, ListView
from .models import Services_order
from django.shortcuts import render, HttpResponse
from services.models import Services
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.utils.dateparse import parse_datetime

@csrf_exempt
def create_order(request):
    if request.method == "POST":
        service = Services.objects.get(id=request.POST['service_id'])
        res = Services_order.objects.create_order(service, request.POST['phone'], request.POST['email'], request.POST['time'])
        response = HttpResponse('Запись успешно создана, номер - ' + str(res.id))
        curTime = str(parse_datetime(res.time).date()).split('-')
        send_mail(
            'Ирисc',
            f'Ваша почта была указана в заказе на "{service.name}"\nНа {curTime[-1]}.{curTime[-2]}.{curTime[-3]} {str(parse_datetime(res.time).time())[:5]}\nНомер вашего заказа - {res.id}',
            'iriy.online@gmail.com',
            [request.POST['email']],
            fail_silently=False,
        )
        return response
    service = Services.objects.get(id=request.GET.get("serviceId"))
    res = render(request, 'service_order_create_view.html',
                  {'name': service.name,
                   'description': service.description,
                   'price': service.price,
                   'id': service.id})
    return res
    
class ServiceOrderDetailView(DetailView):
    model = Services_order
    template_name = 'service_order_detail_view.html'