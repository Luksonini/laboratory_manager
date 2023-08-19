from django.shortcuts import render, redirect, reverse
from django.http import FileResponse
from .models import Reagents
from .forms import ReagentForm, ReagentUsageForm
from .filters import OrderFilter
import qrcode
from io import BytesIO
import base64
from django.http import HttpResponseForbidden

def reagents(request):
    reagents = Reagents.objects.all()
    my_filter = OrderFilter(request.GET, queryset=reagents)
    reagents = my_filter.qs
    return render(request, 'reagentsapp/reagents.html', {'reagents': reagents, 'my_filter': my_filter})

def create_reagent(request):
    if request.method == 'POST':
        reagent_form = ReagentForm(request.POST)
        if reagent_form.is_valid():
            new_reagent = reagent_form.save()
            return redirect('reagentsapp:reagents_list')
    reagent_form = ReagentForm()
    return render(request, 'reagentsapp/create_reagent.html', {'reagent_form': reagent_form})

def edit_reagent(request, id):
    reagent = Reagents.objects.get(id=id)
    reagent_form = ReagentForm(request.POST or None, instance=reagent)
    if request.method == 'POST' and reagent_form.is_valid():
        reagent_form.save()
        return redirect('reagentsapp:reagents_list')
    return render(request, 'reagentsapp/edit_reagent.html', {'reagent_form': reagent_form})

def delete_reagent(request, id):
    reagent = Reagents.objects.get(id=id)
    reagent.delete()
    return redirect('reagentsapp:reagents_list')

import matplotlib.pyplot as plt
# matplotlib.use('agg')

def reagent_details(request, id, access_key=None):
    reagent = Reagents.objects.get(id=id)
    
    error_message = None
    usage_form = ReagentUsageForm()

    if request.method == "POST":
        usage_form = ReagentUsageForm(request.POST)
        
        if usage_form.is_valid():
            used_amount = usage_form.cleaned_data.get('used_amount')
            
            if reagent.remained - used_amount >= 0:
                reagent.remained -= used_amount
                reagent.save()
            else:
                error_message = "Próba zużycia większej ilości odczynnika niż dostępna!"
        else:
            error_message = "Nieprawidłowe dane w formularzu!"

    pie_chart_data = generate_pie_chart(reagent.remained, reagent.quantity)
    qr_code_data = generate_qr_code_url(request, reagent)

    return render(request, 'reagentsapp/reagent_detail.html', {
        'reagent': reagent,
        'usage_form': usage_form,
        'error_message': error_message,
        'qr_data': qr_code_data,
        'pie_chart_data': pie_chart_data
    })



# def generate_pie_chart(remained, quantity):
#     labels = ['Pozostało', 'Zużyte']
#     sizes = [remained, quantity - remained]
#     colors = ['#12af83', '#ff6666']

#     plt.figure(figsize=(5, 5))
#     plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
#     plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
#     buffer = BytesIO()
#     plt.savefig(buffer, format="png", transparent=True)
#     plt.close()
    
#     pie_chart_data = base64.b64encode(buffer.getvalue()).decode()
#     return pie_chart_data

def generate_qr_code_url(request, reagent):
    reagent_url = request.build_absolute_uri(reverse('reagentsapp:reagent_details', args=[reagent.id, reagent.access_key]))
    img = qrcode.make(reagent_url)
    buffer = BytesIO()
    img.save(buffer)
    img_data = base64.b64encode(buffer.getvalue()).decode()
    return img_data


import matplotlib
matplotlib.use('agg')  # Zmiana back-endu

import matplotlib.pyplot as plt
import base64
from io import BytesIO

def generate_pie_chart(remained, quantity):
    labels = ['Pozostało', 'Zużyte']
    sizes = [remained, quantity - remained]
    colors = ['#12af83', '#ff6666']

    plt.figure(figsize=(5, 5))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    buffer = BytesIO()
    plt.savefig(buffer, format="png", transparent=True)
    plt.close()
    
    pie_chart_data = base64.b64encode(buffer.getvalue()).decode()
    return pie_chart_data