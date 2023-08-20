from django.shortcuts import render
from . models import Protocols

def protocols(request):
    protocols = Protocols.objects.all()
    return render(request, 'protocolsapp/protocols.html', {'protocols': protocols})

def detail(request, id):
    protocol = Protocols.objects.get(id=id)
    return render(request, 'protocolsapp/protocol_detail.html', {'protocol': protocol})