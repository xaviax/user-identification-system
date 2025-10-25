from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
# Create your views here.

@login_required
def dashboard(request):

    user = request.user
    area=user.area

    rooms=area.rooms.all()
    systems=System.objects.filter(room__area=area)

    mappings = user.system_mappings.select_related('system','system__room')

    context = {
        'user': user,
        'area': area,
        'rooms': rooms,
        'systems': systems,
        'mappings': mappings,
    }

    return render(request, 'transaction_app/dashboard.html', context)

