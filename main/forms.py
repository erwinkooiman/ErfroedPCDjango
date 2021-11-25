from django import forms
from .models import DoseerPomp, DoseerStraat, ECSensorNa, ECSensorVoor, FDControl, FDStatus, LiterTeller, PHSensorNa, PHSensorVoor, SysteemPomp, WaterFilter,SV,MeetStraat

class CreateNewList(forms.Form):
    name = forms.CharField(label= "name", max_length=200)
    check = forms.BooleanField(required=False)

class SysteempompForm(forms.ModelForm):
    class Meta:
        model = SysteemPomp
        exclude = ('pg','name','nodeid','handlername')

class FDStatusForm(forms.ModelForm):
    class Meta:
        model = FDStatus
        exclude = ('pg','name','nodeid','handlername')

class FDControlForm(forms.ModelForm):
    class Meta:
        model = FDControl
        exclude = ('pg','name','nodeid','handlername')

class DoseerpompForm(forms.ModelForm):
    class Meta:
        model = DoseerPomp
        exclude = ('pg','name','nodeid','handlername')
        
class LitertellerForm(forms.ModelForm):
    class Meta:
        model = LiterTeller
        exclude = ('pg','name','nodeid','handlername')

class WaterfilterForm(forms.ModelForm):
    class Meta:
        model = WaterFilter
        exclude = ('pg','name','nodeid','handlername')

class DoseerstraatForm(forms.ModelForm):
    class Meta:
        model = DoseerStraat
        exclude = ('pg','name','nodeid','handlername')

class SVForm(forms.ModelForm):
    class Meta:
        model = SV
        exclude = ('doseerstraat','name','nodeid','handlername')

class MeetstraatForm(forms.ModelForm):
    class Meta:
        model = MeetStraat
        exclude = ('pg','name','nodeid','handlername')

class PHSensorVoorForm(forms.ModelForm):
    class Meta:
        model = PHSensorVoor
        exclude = ('pg','name','nodeid','handlername')

class PHSensorNaForm(forms.ModelForm):
    class Meta:
        model = PHSensorNa
        exclude = ('pg','name','nodeid','handlername')

class ECSensorVoorForm(forms.ModelForm):
    class Meta:
        model = ECSensorVoor
        exclude = ('pg','name','nodeid','handlername')

class ECSensorNaForm(forms.ModelForm):
    class Meta:
        model = ECSensorNa
        exclude = ('pg','name','nodeid','handlername')



