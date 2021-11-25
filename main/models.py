from django.db import models
# Create your models here.

class ToDoList(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Item(models.Model):
    todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    complete = models.BooleanField()

    def __str__(self):
        return self.text


class PG(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


""" PG.DoseerPomp """


class DoseerPomp(models.Model):
    pg = models.ForeignKey(PG, on_delete=models.CASCADE)
    handlername = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    nodeid = models.CharField(max_length=200, default='SOME STRING')

    Puls = models.BooleanField()
    Status = models.CharField(max_length=200)

    def __str__(self):
        return self.name


""" PG.SysteemPomp """


class SysteemPomp(models.Model):
    pg = models.ForeignKey(PG, on_delete=models.CASCADE)
    handlername = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    nodeid = models.CharField(max_length=200, default='SOME STRING')

    Keuze = models.CharField(max_length=200)
    SlaveOf = models.CharField(max_length=200)
    StoringThermostaat = models.BooleanField(default = False)
    DrukSensorZuig = models.CharField(max_length=200)
    DrukSensorSysteem = models.CharField(max_length=200)

    def __str__(self):
        return self.name
        


""" PG.SysteemPomp.FDStatus """


class FDStatus(models.Model):
    pg = models.ForeignKey(PG, on_delete=models.CASCADE)
    handlername = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    nodeid = models.CharField(max_length=200, default='SOME STRING')

    DriveStatus = models.CharField(max_length=200)
    DriveReady = models.BooleanField(max_length=200)
    DriveRun = models.BooleanField(max_length=200)
    DriveReversed = models.BooleanField(max_length=200)
    DriveFault = models.BooleanField(max_length=200)
    DriveAlarm = models.BooleanField(max_length=200)
    DriveAtReference = models.BooleanField(max_length=200)
    OutputFrequency = models.CharField(max_length=200)
    ActiveFaultCode = models.CharField(max_length=200)
    PIDFeedback = models.CharField(max_length=200)

    def __str__(self):
        return self.name


""" PG.SysteemPomp.FDControl """


class FDControl(models.Model):
    pg = models.ForeignKey(PG, on_delete=models.CASCADE)
    handlername = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    nodeid = models.CharField(max_length=200, default='SOME STRING')

    Start = models.BooleanField(max_length=200)
    Direction = models.BooleanField(max_length=200)
    ResetFault = models.BooleanField(max_length=200)
    PID_Reference = models.CharField(max_length=200)

    def __str__(self):
        return self.name


""" PG.LiterTeller """


class LiterTeller(models.Model):
    pg = models.ForeignKey(PG, on_delete=models.CASCADE)
    handlername = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    nodeid = models.CharField(max_length=200, default='SOME STRING')

    ResetLitersWatergift = models.BooleanField(max_length=200)
    AantalLitersPuls = models.CharField(max_length=200)
    FlowActive = models.BooleanField(max_length=200)
    TotaalAantalLitersWatergift = models.CharField(max_length=200)
    TotaalAantalM3 = models.CharField(max_length=200)
    TotaalAantalLiters = models.CharField(max_length=200)
    ActueleFlow = models.CharField(max_length=200)

    def __str__(self):
        return self.name


""" PG.WaterFilter """


class WaterFilter(models.Model):
    pg = models.ForeignKey(PG, on_delete=models.CASCADE)
    handlername = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    nodeid = models.CharField(max_length=200, default='SOME STRING')

    Hand = models.BooleanField(max_length=200)
    Bedrijf = models.BooleanField(max_length=200)
    Wachttijd = models.CharField(max_length=200)
    Spoeltijd = models.CharField(max_length=200)
    AantalSpoelbeurten = models.CharField(max_length=200)
    DrukSensorVoor = models.CharField(max_length=200)

    def __str__(self):
        return self.name


""" PG.DoseerStraat """


class DoseerStraat(models.Model):
    pg = models.ForeignKey(PG, on_delete=models.CASCADE)
    handlername = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    nodeid = models.CharField(max_length=200, default='SOME STRING')

    MVPulstijd = models.CharField(max_length=200)
    MVPauzetijd = models.CharField(max_length=200)
    MVKeuze = models.CharField(max_length=200)
    MVStatus = models.CharField(max_length=200)
    MVActStand = models.CharField(max_length=200)

    def __str__(self):
        return self.name


""" PG.DoseerStraat.SV """


class SV(models.Model):
    doseerstraat = models.ForeignKey(DoseerStraat, on_delete=models.CASCADE)
    handlername = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    nodeid = models.CharField(max_length=200, default='SOME STRING')

    Keuze = models.CharField(max_length=200)
    ActStand = models.BooleanField(max_length=200)

    def __str__(self):
        return self.name


""" PG.MeetStraat """


class MeetStraat(models.Model):
    pg = models.ForeignKey(PG, on_delete=models.CASCADE)
    handlername = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    nodeid = models.CharField(max_length=200, default='SOME STRING')

    PHMaximaal = models.CharField(max_length=200)
    PHMaxAfwijking = models.CharField(max_length=200)
    PHMaxTijdAfwijking = models.CharField(max_length=200)
    PHAlarmSensor = models.BooleanField(max_length=200)
    PHAlarmRegeling = models.BooleanField(max_length=200)
    ECMaximaal = models.CharField(max_length=200)
    ECMaxAfwijking = models.CharField(max_length=200)
    ECMaxTijdAfwijking = models.CharField(max_length=200)
    ECAlarmSensor = models.BooleanField(max_length=200)
    ECAlarmRegeling = models.BooleanField(max_length=200)
    DrukSensor = models.CharField(max_length=200)
    OMSensorNa = models.CharField(max_length=200)

    def __str__(self):
        return self.name
        


""" PG.MeetStraat.PHSensorVoor """


class PHSensorVoor(models.Model):
    meetstraat = models.ForeignKey(MeetStraat, on_delete=models.CASCADE)
    handlername = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    nodeid = models.CharField(max_length=200, default='SOME STRING')
    s1 = models.CharField(max_length=200)
    s2 = models.CharField(max_length=200)
    s3 = models.CharField(max_length=200)


    def __str__(self):
        return self.name


""" PG.MeetStraat.PHSensorNa """


class PHSensorNa(models.Model):
    meetstraat = models.ForeignKey(MeetStraat, on_delete=models.CASCADE)
    handlername = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    nodeid = models.CharField(max_length=200, default='SOME STRING')
    value = models.CharField(max_length=200)
    s1 = models.CharField(max_length=200)
    s2 = models.CharField(max_length=200)
    s3 = models.CharField(max_length=200)

    def __str__(self):
        return self.name


""" PG.MeetStraat.ECSensorVoor """


class ECSensorVoor(models.Model):
    meetstraat = models.ForeignKey(MeetStraat, on_delete=models.CASCADE)
    handlername = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    nodeid = models.CharField(max_length=200, default='SOME STRING')

    Value = models.CharField(max_length=200)
    ReadCompensatie = models.CharField(max_length=200)
    WriteCompensatie = models.CharField(max_length=200)
    CMDCompensatie = models.CharField(max_length=200)
    CMDCompensatieOK = models.BooleanField(max_length=200)
    CMDCompensatieERR = models.BooleanField(max_length=200)

    def __str__(self):
        return self.name


""" PG.MeetStraat.ECSensorNa """


class ECSensorNa(models.Model):
    meetstraat = models.ForeignKey(MeetStraat, on_delete=models.CASCADE)
    handlername = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    nodeid = models.CharField(max_length=200, default='SOME STRING')

    Value = models.CharField(max_length=200)
    ReadCompensatie = models.CharField(max_length=200)
    WriteCompensatie = models.CharField(max_length=200)
    CMDCompensatie = models.CharField(max_length=200)
    CMDCompensatieOK = models.BooleanField(max_length=200)
    CMDCompensatieERR = models.BooleanField(max_length=200)

    def __str__(self):
        return self.name


