from django.shortcuts import render, redirect
from .models import Protocols
from .AI import remove_empty_lines, create_protocol_prompt, extract_info_from_response, generate_openai_response
from .forms import ProtocolsForm
import openai
import os
from calendarapp.decorators import verified_required  

@verified_required
def upload_and_process_protocol(request):
    if request.method == 'POST':
        protocol_form = ProtocolsForm(request.POST, request.FILES)
        if protocol_form.is_valid():
            openai.api_key = os.getenv('OPENAI_API_KEY')

            # Zapisz tylko plik w celu uzyskania dostępu do ścieżki pliku
            file_field = protocol_form.cleaned_data.get('file')
            temp_protocol = Protocols(file=file_field)
            temp_protocol.save()

            # Przetworzenie pliku
            doc_path = temp_protocol.file.path
            cleaned_text = remove_empty_lines(doc_path)
            prompt = create_protocol_prompt(cleaned_text)

            response = generate_openai_response(prompt)
            print(response)
            title, description, method = extract_info_from_response(response)

            # Aktualizacja reszty pól i zapis
            temp_protocol.title = title
            temp_protocol.description = description
            temp_protocol.method = method
            temp_protocol.save()

    return redirect('protocolsapp:protocols_list')

from django.shortcuts import redirect

@verified_required
def delete_protocol(request, id):
    protocol_to_delete = Protocols.objects.get(id=id)
    protocol_to_delete.delete()
    return redirect('protocolsapp:protocols_list')

@verified_required
def protocols(request):
    protocol_form = ProtocolsForm()
    protocols = Protocols.objects.all()

    return render(request, 'protocolsapp/protocols.html', {'protocols': protocols, 'protocol_form': protocol_form})

@verified_required
def detail(request, id):
    protocol = Protocols.objects.get(id=id)
    return render(request, 'protocolsapp/protocol_detail.html', {'protocol': protocol})


