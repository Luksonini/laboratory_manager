from django.shortcuts import render, redirect
from . models import Reagents
from . forms import ReagentForm

def reagents(request):
    reagents = Reagents.objects.all()
    return render(request, 'reagentsapp/reagents.html', {'reagents' : reagents})

def create_reagent(request):    
    if request.method == 'POST':
        reagent_form = ReagentForm(request.POST)
        if reagent_form.is_valid():
            new_reagent = reagent_form.save()
            return redirect('reagentsapp:reagents_list')

    reagent_form = ReagentForm()
    return render(request, 'reagentsapp/create_reagent.html', {'reagent_form' : reagent_form})

def edit_reagent(request, id):
    reagent = Reagents.objects.get(id=id)
    reagent_form = ReagentForm(request.POST or None, instance=reagent)
    if request.method == 'POST' and reagent_form.is_valid():
        reagent_form.save()
        return redirect('reagentsapp:reagents_list') 
    return render(request, 'reagentsapp/edit_reagent.html', {'reagent_form' : reagent_form})