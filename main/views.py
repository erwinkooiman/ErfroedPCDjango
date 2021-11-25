
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from .models import SysteemPomp, ToDoList
from .forms import*
from mysite.tasks import*

def index(response,id):
    ls = ToDoList.objects.get(id=id)

    if response.method == "POST":
        print(response.POST)
        if response.POST.get("save"):
            for item in ls.item_set.all():
                if response.POST.get("c"+ str(item.id)) == "clicked":
                    item.complete = True
                else:
                    item.complete = False
                item.save()

        elif response.POST.get("newItem"):
            txt = response.POST.get("new")

            if len(txt) > 2 :
                ls.item_set.create(text=txt, complete=False)
            else:
                print("invalid")

    return render(response, "main/list.html",{"ls":ls})

def home(response):
    return render(response, "main/home.html",{})

def create(response):
    if response.method == "POST":
        form = CreateNewList(response.POST)
        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name= n)
            t.save()
        return HttpResponseRedirect("/%i" %t.id)
    else:
        form = CreateNewList()
    return render(response, "main/create.html",{"form":form})


def systeempomp_view(request, id = None):
    obj = SysteemPomp.objects.get(id=id)
    if request.method == 'POST':
        if request.POST.get('WriteValues'):
            form = SysteempompForm(request.POST, instance=obj)
            if form.is_valid():
                form.save()
                write_value_Systeempomp(obj)
            return render(request,"main/Systeempomp_template.html",get_systeempomp_data(id))

        if request.POST.get('GetValues'):
            return render(request,'main/Systeempomp_template.html',get_systeempomp_data(id))
    else:
        return render(request,'main/Systeempomp_template.html',get_systeempomp_data(id))

def get_systeempomp_data(id):
    obj = SysteemPomp.objects.get(id=id)
    form = SysteempompForm(instance=obj)
    FDSname = obj.name+'.FDStatus'
    FDSobj = FDStatus.objects.get(name=FDSname)
    fdstatusform = FDStatusForm(instance=FDSobj)
    FDCname = obj.name+'.FDControl'
    FDCobj = FDControl.objects.get(name=FDCname)
    fdcontrolform = FDControlForm(instance=FDCobj)

    return {'form':form,'form2':fdstatusform,'form3':fdcontrolform,'obj':obj,'FDCobj':FDCobj,'FDSobj':FDSobj}

def doseerpomp_view(request, id = None):
    obj = DoseerPomp.objects.get(id=id)
    if request.method == 'POST':
        if request.POST.get('WriteValues'):
            form = DoseerpompForm(request.POST, instance=obj)
            if form.is_valid():
                form.save()
                write_value_Doseerpomp(obj)
                
            return render(request,"main/DoseerPomp_template.html",get_doseerpomp_data(id))
        if request.POST.get('GetValues'):
            return render(request,'main/DoseerPomp_template.html',get_doseerpomp_data(id))
    else:
        return render(request,'main/DoseerPomp_template.html',get_doseerpomp_data(id))

def get_doseerpomp_data(id):
    obj = DoseerPomp.objects.get(id=id)
    form = DoseerpompForm(instance=obj)

    return {'form':form,'obj':obj}

def literteller_view(request, id = None):
    obj = LiterTeller.objects.get(id=id)
    if request.method == 'POST':
        if request.POST.get('WriteValues'):
            form = LitertellerForm(request.POST, instance=obj)
            if form.is_valid():
                form.save()
                obj = LiterTeller.objects.get(id=id)
                write_value_Literteller(obj)
                
            return render(request,"main/Literteller_template.html",get_Literteller_data(id))
        if request.POST.get('GetValues'):

            return render(request,'main/Literteller_template.html',get_Literteller_data(id))
    else:
        return render(request,'main/Literteller_template.html',get_Literteller_data(id))

def get_Literteller_data(id):
    obj = LiterTeller.objects.get(id=id)
    form = LitertellerForm(instance=obj)
    return {'form':form,'obj':obj}

def waterfilter_view(request, id = None):
    pass
    obj = WaterFilter.objects.get(id=id)
    if request.method == 'POST':
        if request.POST.get('WriteValues'):
            form = WaterfilterForm(request.POST, instance=obj)
            if form.is_valid():
                form.save()
                write_value_Waterfilter(obj)
                
            return render(request,"main/Waterfilter_template.html",get_waterfilter_data(id))
        if request.POST.get('GetValues'):

            return render(request,'main/Waterfilter_template.html',get_waterfilter_data(id))
    else:
        return render(request,'main/Waterfilter_template.html',get_waterfilter_data(id))

def get_waterfilter_data(id):
    obj = WaterFilter.objects.get(id=id)
    form = WaterfilterForm(instance=obj)

    return {'form':form,'obj':obj}

def doseerstraat_view(request, id = None):
    pass
    obj = DoseerStraat.objects.get(id=id)
    if request.method == 'POST':
        if request.POST.get('WriteValues'):
            form = DoseerstraatForm(request.POST, instance=obj)
            if form.is_valid():
                form.save()
                write_value_Doseerstraat(obj)
                
            return render(request,"main/Doseerstraat_template.html",get_doseerstraat_data(id))
        if request.POST.get('GetValues'):

            return render(request,'main/Doseerstraat_template.html',get_doseerstraat_data(id))
    else:
        return render(request,'main/Doseerstraat_template.html',get_doseerstraat_data(id))

def get_doseerstraat_data(id):
    obj = DoseerStraat.objects.get(id=id)
    form = DoseerstraatForm(instance=obj)
    i = int(obj.pg.name[2:])
    temp = SV.objects.filter(name__startswith=f"PG_{i}Doseerstraat1")
    svform = []
    svobj = []
    for sv in temp:
        svobj.append(sv)
        svform.append(SVForm(instance=sv))

    return {'form':form,'obj':obj,'form2':svform,'obj2':svform}


def meetstraat_view(request, id = None):
    obj = MeetStraat.objects.get(id=id)
    if request.method == 'POST':
        if request.POST.get('WriteValues'):
            form = MeetstraatForm(request.POST, instance=obj)
            if form.is_valid():
                form.save()
                write_value_Meetstraat(obj)
            return render(request,"main/Meetstraat_template.html",get_meetstraat_data(id))

        if request.POST.get('GetValues'):
            return render(request,'main/Meetstraat_template.html',get_meetstraat_data(id))
    else:
        return render(request,'main/Meetstraat_template.html',get_meetstraat_data(id))


def get_meetstraat_data(id):
    obj = MeetStraat.objects.get(id=id)
    form = MeetstraatForm(instance=obj)

    i = int(obj.pg.name[2:])
    temp = PHSensorNa.objects.filter(name__startswith=f"PG_{i}Meetstraat1")
    PHsnform = PHSensorNaForm(instance=temp[0])
    PHsnobj = temp[0]
    # for phsn in temp:
    #     PHsnobj.append(phsn)
    #     PHsnform.append(PHSensorNaForm(instance=phsn))


    return {'form':form,'obj':obj,'from2':PHsnform,'obj2':PHsnobj}

 

def stop_view(request):
    stop()
    return render(request, "main/home.html",{})

def startopcua_view(request):
    Start()
    return render(request, "main/home.html",{})



