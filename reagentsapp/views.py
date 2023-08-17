from django.shortcuts import render, redirect, reverse
from django.http import FileResponse
from .models import Reagents
from .forms import ReagentForm, ReagentUsageForm
from .filters import OrderFilter
import qrcode
from io import BytesIO
import base64

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

def reagent_details(request, id):
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

    reagent_url = request.build_absolute_uri()
    img = qrcode.make(reagent_url)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_data = base64.b64encode(buffer.getvalue()).decode()

    return render(request, 'reagentsapp/reagent_detail.html', {
        'reagent': reagent,
        'usage_form': usage_form,
        'error_message': error_message,
        'qr_data': img_data
    })
