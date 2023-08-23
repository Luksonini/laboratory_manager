from django.shortcuts import render, redirect
from .models import Protocols, ChatResponse
from .AI import remove_empty_lines, create_protocol_prompt, extract_info_from_response, generate_openai_response
from .forms import ProtocolsForm
import openai

def protocols(request):
    if request.method == 'POST':
        protocol_form = ProtocolsForm(request.POST, request.FILES)
        if protocol_form.is_valid():
            new_protocol = protocol_form.save()
                    
    protocol_form = ProtocolsForm()
    protocols = Protocols.objects.all()
    return render(request, 'protocolsapp/protocols.html', {'protocols': protocols, 'protocol_form': protocol_form})

# def detail(request, id):
#     protocol = Protocols.objects.get(id=id)
#     saved_response = ChatResponse.objects.get(id=id)
#     doc_path = protocol.file.path

#     if saved_response.title is None:
            
#         cleaned_text = remove_empty_lines(doc_path)
#         if cleaned_text:
#             prompt = create_protocol_prompt(cleaned_text)
#         resp = openai.ChatCompletion.create(
#             model="gpt-4",
#             max_tokens=1024,
#             n=1,
#             stop=None,
#             messages=[{'role': 'user', "content": prompt}],
#             temperature=0.5,
#         )
#         resp = resp['choices'][0]["message"]["content"]
#         title, description, method  = extract_info_from_response(resp)
#         saved_response.title = title
#         saved_response.description = description
#         saved_response.method = method
#         saved_response.save()
#     return render(request, 'protocolsapp/protocol_detail.html', {'protocol': protocol, "saved_response" : saved_response})
import re
def detail(request, id):
    protocol = Protocols.objects.get(id=id)

    try:
        saved_response = ChatResponse.objects.get(protocol=protocol)
    except ChatResponse.DoesNotExist:
        saved_response = ChatResponse(protocol=protocol)
        saved_response.save()

    doc_path = protocol.file.path
    # if not saved_response.description:
    cleaned_text = remove_empty_lines(doc_path)
    
    prompt = create_protocol_prompt(cleaned_text)
    print(prompt)
        
    resp = openai.ChatCompletion.create(
        model="gpt-4",
        max_tokens=1024,
        n=1,
        stop=None,
        messages=[{'role': 'system', "content": prompt}],
        temperature=0.5,
    )
    resp = resp['choices'][0]["message"]["content"]
    title, description, method  = extract_info_from_response(resp)
    saved_response.title = title
    saved_response.description = description
    saved_response.method = method
    saved_response.save()
    print(title)

    return render(request, 'protocolsapp/protocol_detail.html', {'protocol': protocol, "resp" : resp, "saved_response" : saved_response})

def extract_info_from_response(response_text):
    title_match = re.search(r"Title: (.*?)\s*Protocol Description:", response_text)
    title = title_match.group(1) if title_match else None
    description_match = re.search(r"Protocol Description: (.*?)\s*Methods:", response_text)
    description = description_match.group(1) if description_match else None
    methods_match = re.search(r"Methods: (.*)", response_text, re.DOTALL)
    methods = methods_match.group(1) if methods_match else None
    return title, description, methods
