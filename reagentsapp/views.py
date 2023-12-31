from django.shortcuts import render, redirect
from .models import Reagents
from .forms import ReagentForm, ReagentUsageForm
from .filters import OrderFilter
from .utils import generate_pie_chart
from django.urls import reverse
import base64
from io import BytesIO
import qrcode
from calendarapp.decorators import verified_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@verified_required
def reagents(request):
    reagents_list = Reagents.objects.order_by('reagent_name')
    my_filter = OrderFilter(request.GET, queryset=reagents_list)
    reagents_list = my_filter.qs

    # Dodaj paginację
    paginator = Paginator(reagents_list, 10)  # Show 10 reagents per page
    page = request.GET.get('page')
    try:
        reagents = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        reagents = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        reagents = paginator.page(paginator.num_pages)

    return render(request, 'reagentsapp/reagents.html', {'reagents': reagents, 'my_filter': my_filter})

@verified_required
def create_reagent(request):
    if request.method == 'POST':
        reagent_form = ReagentForm(request.POST)
        if reagent_form.is_valid():
            new_reagent = reagent_form.save()
            return redirect('reagentsapp:reagents_list')
    reagent_form = ReagentForm()
    return render(request, 'reagentsapp/create_reagent.html', {'reagent_form': reagent_form})

@verified_required
def edit_reagent(request, id):
    reagent = Reagents.objects.get(id=id)
    reagent_form = ReagentForm(request.POST or None, instance=reagent)
    if request.method == 'POST' and reagent_form.is_valid():
        reagent_form.save()
        return redirect('reagentsapp:reagents_list')
    return render(request, 'reagentsapp/edit_reagent.html', {'reagent_form': reagent_form})

@verified_required
def delete_reagent(request, id):
    reagent = Reagents.objects.get(id=id)
    reagent.delete()
    return redirect('reagentsapp:reagents_list')


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

@verified_required
def generate_qr_code_url(request, reagent):
    reagent_url = request.build_absolute_uri(reverse('reagentsapp:reagent_details', args=[reagent.id, reagent.access_key]))
    img = qrcode.make(reagent_url)
    buffer = BytesIO()
    img.save(buffer)
    img_data = base64.b64encode(buffer.getvalue()).decode()
    return img_data

