from django.shortcuts import render, redirect
from django.urls import reverse
from . forms import SamplesForm, SampleUsageForm
from .models import SamplesModel
from .filters import OrderSampleFilter
from reagentsapp.utils import generate_pie_chart
import base64
from io import BytesIO
import qrcode

# Create your views here.
def samples(request):
    samples = SamplesModel.objects.all()
    sample_filter = OrderSampleFilter(request.GET, queryset=samples)
    samples = sample_filter.qs
    return render(request, 'samplesapp/samples.html', {"samples" : samples, "sample_filter" : sample_filter})

def create_sample(request):
    if request.method == 'POST':
        samples_form = SamplesForm(request.POST)
        if samples_form.is_valid():
            new_sample = samples_form.save()
            return redirect('samplesapp:samples_list')
    samples_form = SamplesForm()
    return render(request, 'samplesapp/create_sample.html', {'samples_form': samples_form})

def edit_sample(request, id):
    samples = SamplesModel.objects.get(id=id)
    samples_form = SamplesForm(request.POST or None, instance=samples)
    if request.method == 'POST' and samples_form.is_valid():
        samples_form.save()
        return redirect('samplesapp:samples_list')
    return render(request, 'samplesapp/edit_sample.html', {'samples_form': samples_form})

def delete_sample(request, id):
    sample = SamplesModel.objects.get(id=id)
    sample.delete()
    return redirect('samplesapp:samples_list')

def sample_details(request, id, access_key=None):
    sample = SamplesModel.objects.get(id=id)

    error_message = None
    usage_form = SampleUsageForm()

    if request.method == "POST":
        usage_form = SampleUsageForm(request.POST)

        if usage_form.is_valid():
            used_amount = usage_form.cleaned_data.get('used_amount')

            if sample.remained - used_amount >= 0:
                sample.remained -= used_amount
                sample.save()
            else:
                error_message = "Próba zużycia większej ilości próbki niż dostępna!"
        else:
            error_message = "Nieprawidłowe dane w formularzu!"

    # pie_chart_data = generate_pie_chart(sample.remained, sample.quantity)
    # qr_code_data = generate_qr_code_url(request, sample)

    return render(request, 'samplesapp/sample_detail.html', {
        'sample': sample,
        'usage_form': usage_form,
        'error_message': error_message,
        # 'qr_data': qr_code_data,
        # 'pie_chart_data': pie_chart_data
    })


# def generate_qr_code_url(request, sample):
#     sample_url = request.build_absolute_uri(reverse('samplesapp:sample_details', args=[sample.id, sample.access_key]))
#     img = qrcode.make(sample_url)
#     buffer = BytesIO()
#     img.save(buffer)
#     img_data = base64.b64encode(buffer.getvalue()).decode()
#     return img_data