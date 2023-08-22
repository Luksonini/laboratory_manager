from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from .models import Protocols
from .AI import remove_empty_lines, create_protocol_prompt, extract_info_from_response
import openai

def protocols(request):
    protocols = Protocols.objects.all()
    return render(request, 'protocolsapp/protocols.html', {'protocols': protocols})

def detail(request, id):
    protocol = Protocols.objects.get(id=id)
    return render(request, 'protocolsapp/protocol_detail.html', {'protocol': protocol})

def update_protocol(request, protocol_id):
    protocol = get_object_or_404(Protocols, id=protocol_id)
    doc_path = protocol.file.path

    # Usuń puste linie i utwórz prompt
    cleaned_text = remove_empty_lines(doc_path)
    prompt = create_protocol_prompt(cleaned_text)

    # Utwórz odpowiedź z OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-4",
        max_tokens=1024,
        n=1,
        stop=None,
        messages=[{'role':'user', "content": prompt}],
        temperature=0.7,
    )

    result = response['choices'][0]["message"]["content"]

    # Wyciągnięcie informacji
    title, description, methods = extract_info_from_response(result)

    # Aktualizacja modelu
    protocol.title = title
    protocol.description = description
    protocol.method = methods
    protocol.save()

    return redirect('some_view')  