from django.shortcuts import render

from boats.models import BoatModel, Port
from django.db.models import Count

def home(request):  
    # Most rented boats
    most_rented_boats = (
        BoatModel.objects.annotate(rental_count=Count('instances__order_boats'))
        .order_by('-rental_count')[:3]
    )

    # Most affordable boats
    most_affordable_boats = BoatModel.objects.order_by('price_per_day')[:3]

    # Most recent boats
    most_recent_boats = BoatModel.objects.order_by('-release_date')[:3]

    ports = Port.objects.all()

    context = {
        'most_rented_boats': most_rented_boats,
        'most_affordable_boats': most_affordable_boats,
        'most_recent_boats': most_recent_boats,
        'ports': ports
    }
    return render(request, 'escaparate.html', context)

def about(request):
    return render(request, 'about.html')