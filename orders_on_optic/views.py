from django.views.generic import DetailView, ListView
from .models import Optics_order
from django.shortcuts import render, HttpResponse 
from optics.models import Optics
from django.views.decorators.csrf import csrf_exempt
import re
from django.core.mail import send_mail

@csrf_exempt
def create_order(request):
    if request.method == "POST":
        optic = Optics.objects.get(id=request.POST['optic_id'])
        result = re.match(r'[0-9]{10,10}', request.POST['phone'])
        if result:
            pass
        res = Optics_order.objects.create_order(optic, request.POST['phone'], request.POST['email'])
        response = HttpResponse('Запись успешно создана, номер - ' + str(res.id))
        send_mail(
            'Ирисc',
            f'Ваша почта была указана в заказе на "{optic.name}"\nНомер вашего заказа - {res.id}',
            'iriy.online@gmail.com',
            [request.POST['email']],
            fail_silently=False,
        )
        return response
    optic = Optics.objects.get(id=request.GET.get("opticId"))
    return render(request, 'optics_order_create_view.html',
                  {'name': optic.name,
                   'picture': optic.picture,
                   'description': optic.description,
                   'price': optic.price,
                   'id': optic.id})
    
class OpticsOrderDetailView(DetailView):
    model = Optics_order
    template_name = 'optics_order_detail_view.html'