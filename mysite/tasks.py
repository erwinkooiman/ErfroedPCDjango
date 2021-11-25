from opcua import Client,ua
from main.models import* 

uri = "opc.tcp://172.16.0.243:4840"     #adres van de opcua server
ns = 4                                  #namespace 
client = Client(uri)
subscribeNodes = []                     #list met nodes om te subscriben

def connectopcua():
    try:
        client.connect()                                            #start opcua connectie
        client.load_type_definitions()                              # scan server for custom structures and import them
        print('\x1b[6;30;42m' + 'opcua verbonden' + '\x1b[0m')      #print in kleur voor debug 
        global params                                               #stel parameters van subscriptie in
        params = ua.CreateSubscriptionParameters()
        params.RequestedPublishingInterval = 500
        params.RequestedLifetimeCount = 3000
        params.RequestedMaxKeepAliveCount = 10000
        params.MaxNotificationsPerPublish = 2147483647
        params.PublishingEnabled = True
        params.Priority = 0

    except Exception as e:
        client.disconnect()                                         #disconnect opcua als er een fout optreed
        print('\x1b[6;30;41m' + 'opcua NIET verbonden' + '\x1b[0m') #print in kleur voor debug 
        print(e)

def disconnectopcua():
    client.disconnect()                                     #disconnect opcua connectie
    print('\x1b[6;30;43m' + 'opcua gesloten' + '\x1b[0m')   #print in kleur voor debug 

def get_struct(nodeid):   
    obj = client.get_node(nodeid)       #haal object op van opcua server met node id
    client.load_type_definitions()      #load type structs van server
    after_array = obj.get_value()       #haal waardes op
    return after_array,obj              #return waardes


def maakpompgroep():
    global client
    connectopcua()                     #start opcua verbinding
    l = 9
    printProgressBar(0, l, prefix = 'Data ophalen:', suffix = 'Complete', length = 50)  #loading bar
    for i in range(10):                     
        bestaat = update_or_create_pompgroep(i) #check welke nodes aanwezig zijn
        
        if bestaat['isdoseerpomp']:     #als er een node gevonden is maak deze aan of update de waardes
            update_or_create_Doseerpomp(i)
        if bestaat['issysteempomp']:
            update_or_create_Systeempomp(i)
        if bestaat['isliterteller']:
            update_or_create_Literteller(i)
        if bestaat['isliterteller']:
            update_or_create_Waterfilter(i)
        if bestaat['iswaterfilter']:
            update_or_create_Doseerstraat(i)
        if bestaat['isdoseerstraat']:
            update_or_create_Meetstraat(i)
        if bestaat['ismeetstraat']:
            update_or_create_Meetstraat(i)
        printProgressBar(i, l, prefix = 'Data ophalen:', suffix = 'Complete', length = 50)  #update loading bar

    print('\x1b[6;30;42m' + 'Data opgehaald en geschreven naar database' + '\x1b[0m')


#update_or_create
def update_or_create_pompgroep(i):

    bestaat = { 
        'error' : 0,
        'isdoseerpomp' : 0,
        'issysteempomp' : 0,
        'isliterteller' : 0,
        'iswaterfilter' : 0,
        'isdoseerstraat' : 0,
        'ismeetstraat' : 0,
    }

    #als de node gevonden is word de dict geupdate en zal er een object aangemaakt worden om de waardes in te schrijven
    try:
        Doseerpomp = get_struct("ns={};s=pPG_{}_DoseerPomp".format(ns, i+1))
        bestaat['error'] +=1
        bestaat['isdoseerpomp'] = 1
    except:pass
    try:
        Systeempomp = get_struct("ns={};s=pPG_{}_SysteemPomp".format(ns, i+1))
        bestaat['error'] +=1
        bestaat['issysteempomp'] = 1
    except:pass
    try: 
        Literteller = get_struct("ns={};s=pPG_{}_LiterTeller".format(ns, i+1))
        bestaat['error'] +=1
        bestaat['isliterteller']  = 1
    except:pass
    try:
        Waterfilter = get_struct("ns={};s=pPG_{}_WaterFilter".format(ns, i+1))
        bestaat['error'] +=1
        bestaat['iswaterfilter'] = 1
    except:pass
    try:
        Doseerstraat = get_struct("ns={};s=pPG_{}_DoseerStraat".format(ns, i+1))
        bestaat['error'] +=1
        bestaat['isdoseerstraat'] = 1
    except:pass
    try:
        Meetstraat = get_struct("ns={};s=pPG_{}_MeetStraat".format(ns, i+1))
        bestaat['error'] +=1
        bestaat['ismeetstraat'] = 1
    except:pass

    # als er een of meer nodes gevonden zijn maak een pompgroep aan
    if bestaat['error'] > 0:
        pgname = "PG{}".format(i+1)
        pgdata = {'name':pgname }
        pg, created = PG.objects.update_or_create(name=pgname, defaults=pgdata)
        #print('\x1b[5;30;40m' + f'pompgroep aangemaakt = {created}' + '\x1b[0m')
    return bestaat

def update_or_create_Doseerpomp(i):                            

    pg = PG.objects.get(name="PG{}".format(i+1))
    try:
        nodeid = f"ns={ns};s=pPG_{i+1}_DoseerPomp"
        Doseerpomp,_ = get_struct(nodeid)                       #haal waardes op 
        for idx, dos in enumerate(Doseerpomp):
            DoseerpompName = "PG_{}_DoseerPomp{}".format(i+1,idx+1)

            HandlerName = f"pPG_{i+1}_DoseerPomp"
            subscribeNodes.append(client.get_node(nodeid))      #voeg node toe aan list om later te kunnen subscriben
            
                                
            Doseerpomp_Data ={                                  #schrijf waardes van server in dictionary
                'pg' :pg,
                'handlername': HandlerName,
                'nodeid':nodeid,
                'name': DoseerpompName,
                'Puls': dos.Puls,
                'Status':dos.Status
            }
            # update of create de database object met de dictionary
            rDoseerpomp, created = DoseerPomp.objects.update_or_create(name=DoseerpompName, defaults=Doseerpomp_Data)
            #print('\x1b[5;30;40m' + f'doseerpomp aangemaakt = {created}' + '\x1b[0m')
            

    except Exception as e:
        print(e)

def update_or_create_Systeempomp(i):

    pg = PG.objects.get(name="PG{}".format(i+1))
    try:
        nodeid = f"ns={ns};s=pPG_{i+1}_SysteemPomp"
        Systeempomp,obj = get_struct(nodeid)
        SysteempompName = f"PG_{i+1}_SysteemPomp"

        HandlerName = f"pPG_{i+1}_SysteemPomp"
        subscribeNodes.append(client.get_node(nodeid))

        Systeempomp_Data = {
            'pg': pg,
            'handlername': HandlerName,
            'nodeid': nodeid,
            'name': SysteempompName,
            'Keuze': Systeempomp.Keuze,
            'SlaveOf': Systeempomp.SlaveOf,
            'StoringThermostaat': Systeempomp.StoringThermostaat,
            'DrukSensorZuig': Systeempomp.DrukSensorZuig,
            'DrukSensorSysteem': Systeempomp.DrukSensorSysteem
        }
        rSysteempomp, created = SysteemPomp.objects.update_or_create(name=SysteempompName, defaults=Systeempomp_Data)
        #print('\x1b[5;30;40m' + f'Systeempomp aangemaakt = {created}' + '\x1b[0m')
    except Exception as e:
        print(e)           

    
    try:
        FDStatusName = "PG_{}_SysteemPomp.FDStatus".format(i+1)
        Systeempomp_FDStatus_Data = {
        'pg': pg,
        'handlername': HandlerName,
        'nodeid': "ns={};s=pPG_{}_SysteemPomp".format(ns, i+1),
        'name': FDStatusName,
        'DriveStatus':Systeempomp.FDStatus.DriveStatus,
        'DriveReady':Systeempomp.FDStatus.DriveReady,
        'DriveRun':Systeempomp.FDStatus.DriveRun,
        'DriveReversed':Systeempomp.FDStatus.DriveReversed,
        'DriveFault': Systeempomp.FDStatus.DriveFault,
        'DriveAlarm': Systeempomp.FDStatus.DriveAlarm,
        'DriveAtReference':Systeempomp.FDStatus.DriveAtReference,
        'OutputFrequency':Systeempomp.FDStatus.OutputFrequency,
        'ActiveFaultCode':Systeempomp.FDStatus.ActiveFaultCode,
        'PIDFeedback':Systeempomp.FDStatus.PIDFeedback,
        }
        rFDstatus, created = FDStatus.objects.update_or_create(name=FDStatusName, defaults=Systeempomp_FDStatus_Data)
        #print('\x1b[0;30;47m' + f'FDStatus aangemaakt = {created}' + '\x1b[0m')
    except Exception as e:
        print(e)

    try:
        FDControlName = "PG_{}_SysteemPomp.FDControl".format(i+1)
        Systeempomp_FDControl_data = {
        'pg': pg,
        'handlername': HandlerName,
        'nodeid': "ns={};s=pPG_{}_SysteemPomp".format(ns, i+1),
        'name': FDControlName,
        'Start':Systeempomp.FDControl.Start,
        'Direction':Systeempomp.FDControl.Direction,
        'ResetFault':Systeempomp.FDControl.ResetFault,
        'PID_Reference':Systeempomp.FDControl.PID_Reference
        }
        rFDcontrol, created = FDControl.objects.update_or_create(name=FDControlName, defaults=Systeempomp_FDControl_data)
        #print('\x1b[5;30;40m' + f'FDControl aangemaakt = {created}' + '\x1b[0m')
    except Exception as e:
        print(e)

def update_or_create_Literteller(i):                    #deze functie maakt of update de waardes in de database

    pg = PG.objects.get(name="PG{}".format(i+1))        # pompgroep object waar de literteller aan gelinkt word
    try:
        nodeid = f"ns={ns};s=pPG_{i+1}_LiterTeller"
        Literteller,obj = get_struct(nodeid)            #haal struct op van opcua server,return-> list met literteller structs

        HandlerName = f"pPG_{i+1}_LiterTeller"          #HandlerName wordt niet meer gebruikt
        subscribeNodes.append(client.get_node(nodeid))  # voeg de node toe aan de subscribeNodes list om later op te subscriben

        for idx, liter in enumerate(Literteller):                       #voor elke literteller in de list
            LitertellerName = "PG_{}_Literteller{}".format(i+1,idx+1)   
            Literteller_Data = {                                        #scrijft alle opgehaalde data in een dictionary 
            'pg': pg,                                                   #pg linkt de literteller aan een pompgroep
            'handlername': HandlerName,                                 
            'nodeid': nodeid,
            'name': LitertellerName,
            'ResetLitersWatergift':liter.ResetLitersWatergift,
            'AantalLitersPuls':liter.AantalLitersPuls,
            'FlowActive':liter.FlowActive,
            'TotaalAantalLitersWatergift':liter.TotaalAantalLitersWatergift,
            'TotaalAantalM3': liter.TotaalAantalM3,
            'TotaalAantalLiters': liter.TotaalAantalLiters,
            'ActueleFlow':liter.ActueleFlow,
            }
            # update or create een database object met de Literteller_Data dictionary
            rLitterteller, created = LiterTeller.objects.update_or_create(name=LitertellerName, defaults=Literteller_Data)
            #print('Litterteller aangemaakt = ',created)

    except Exception as e:
        print(e)        #als er een fout optreed print de error in de terminal

def update_or_create_Waterfilter(i):

    pg = PG.objects.get(name="PG{}".format(i+1))
    try:
        nodeid = f"ns={ns};s=pPG_{i+1}_WaterFilter"
        Waterfilter,obj = get_struct(nodeid)

        HandlerName = f"pPG_{i+1}_WaterFilter"
        subscribeNodes.append(client.get_node(nodeid))

        for idx, filter in enumerate(Waterfilter):
            WaterfilterName = "PG_{}WaterFilter{}".format(i+1,idx+1)
            Waterfilter_Data = {
            'pg': pg,
            'handlername': HandlerName,
            'nodeid': nodeid,
            'name': WaterfilterName,
            'Hand':filter.Hand,
            'Bedrijf':filter.Bedrijf,
            'Wachttijd':filter.Wachttijd,
            'Spoeltijd':filter.Spoeltijd,
            'AantalSpoelbeurten': filter.AantalSpoelbeurten,
            'DrukSensorVoor': filter.DrukSensorVoor,
            }
            rWaterfilter, created = WaterFilter.objects.update_or_create(name=WaterfilterName, defaults=Waterfilter_Data)
            #print('waterfilter aangemaakt = ',created)

    except Exception as e:
        print(e)
                        
def update_or_create_Doseerstraat(i):

    pg = PG.objects.get(name="PG{}".format(i+1))
    try:
        nodeid = f"ns={ns};s=pPG_{i+1}_DoseerStraat"
        Doseerstraat,obj = get_struct(nodeid)

        HandlerName = f"pPG_{i+1}_DoseerStraat"
        subscribeNodes.append(client.get_node(nodeid))

        for idx, straat in enumerate(Doseerstraat):
            DoseerstraatName = "PG_{}_Doseerstraat{}".format(i+1,idx+1)
            data = {
            'pg': pg,
            'handlername': HandlerName,
            'nodeid': nodeid,
            'name': DoseerstraatName,
            'MVPulstijd':straat.MVPulstijd,
            'MVPauzetijd':straat.MVPauzetijd,
            'MVKeuze':straat.MVKeuze,
            'MVStatus':straat.MVStatus,
            'MVActStand': straat.MVActStand,
            }
            rDoseerstraat, created = DoseerStraat.objects.update_or_create(name=DoseerstraatName, defaults=data)
            #print('Doseerstraat aangemaakt = ',created)

            for idx2, sv in enumerate(Doseerstraat[idx].SV):
                SVName = "PG_{}_Doseerstraat{}.SV{}".format(i+1, idx+1,idx2+1)
                data = {
                    'doseerstraat': rDoseerstraat,
                    'handlername': HandlerName,
                    'nodeid': "ns={};s=pPG_{}_DoseerStraat".format(ns, i+1),
                    'name': SVName,
                    'Keuze': sv.Keuze,
                    'ActStand': sv.ActStand
                }
                rSV, created = SV.objects.update_or_create(name=SVName, defaults=data)
                # print('SV aangemaakt = ', created)

    except Exception as e:
        print(e)

def update_or_create_Meetstraat(i):  

    pg = PG.objects.get(name="PG{}".format(i+1))
    try:
        nodeid = f"ns={ns};s=pPG_{i+1}_MeetStraat"
        Meetstraat,obj = get_struct(nodeid)

        HandlerName = f"pPG_{i+1}_MeetStraat"
        subscribeNodes.append(client.get_node(nodeid))


        for idx, meet in enumerate(Meetstraat):
            MeetstraatName = "PG_{}Meetstraat{}".format(i+1,idx+1)
            data = {
            'pg': pg,
            'handlername': HandlerName,
            'nodeid': nodeid,
            'name': MeetstraatName,
            'PHMaximaal':meet.PHMaximaal,
            'PHMaxAfwijking':meet.PHMaxAfwijking,
            'PHMaxTijdAfwijking':meet.PHMaxTijdAfwijking,
            'PHAlarmSensor':meet.PHAlarmSensor,
            'PHAlarmRegeling': meet.PHAlarmRegeling,
            'ECMaximaal': meet.ECMaximaal,
            'ECMaxAfwijking':meet.ECMaxAfwijking,
            'ECMaxTijdAfwijking':meet.ECMaxTijdAfwijking,
            'ECAlarmSensor':meet.ECAlarmSensor,
            'ECAlarmRegeling':meet.ECAlarmRegeling,
            'DrukSensor':meet.DrukSensor,
            'OMSensorNa':meet.OMSensorNa,
            }
            rMeetstraat, created = MeetStraat.objects.update_or_create(name=MeetstraatName, defaults=data)
            #print('Meetstraat aangemaakt = ',created)

            for idx2, PHSv in enumerate(Meetstraat[idx].PHSensorVoor):
                PHSensorVoorName = "PG_{}Meetstraat{}.PHSensorVoor{}".format(i+1,idx+1,idx2+1)
                data = {
                'meetstraat': rMeetstraat,
                'handlername': HandlerName,
                'nodeid': "ns={};s=pPG_{}Meetstraat".format(ns, i+1),
                'name': PHSensorVoorName,
                'value':PHSv
                }
                rPHSensorVoor, created = PHSensorVoor.objects.update_or_create(name=PHSensorVoorName, defaults=data)
                #print('PHSensorVoor aangemaakt = ',created)

            for idx2, PHSn in enumerate(Meetstraat[idx].PHSensorNa):
                PHSensorNaName = "PG_{}Meetstraat{}.PHSensorNa{}".format(i+1,idx+1,idx2+1)
                data = {
                'meetstraat': rMeetstraat,
                'handlername': HandlerName,
                'nodeid': "ns={};s=pPG_{}Meetstraat".format(ns, i+1),
                'name': PHSensorNaName,
                'value':PHSn
                }
                rPHSensorNa, created = PHSensorNa.objects.update_or_create(name=PHSensorNaName, defaults=data)
               # print('PHSensorNa aangemaakt = ',created)

            for idx2, ECv in enumerate(Meetstraat[idx].ECSensorVoor):
                ECSensorVoorName = "PG_{}Meetstraat{}.ECSensorVoor{}".format(i+1,idx+1,idx2+1)
                data = {
                'meetstraat': rMeetstraat,
                'handlername': HandlerName,
                'nodeid': "ns={};s=pPG_{}Meetstraat".format(ns, i+1),
                'name': ECSensorVoorName,
                'Value':ECv.Value,
                'ReadCompensatie':ECv.ReadCompensatie,
                'WriteCompensatie':ECv.WriteCompensatie,
                'CMDCompensatie':ECv.CMDCompensatie,
                'CMDCompensatieOK':ECv.CMDCompensatieOK,
                'CMDCompensatieERR':ECv.CMDCompensatieERR,
                }

                rECSensorVoor, created = ECSensorVoor.objects.update_or_create(name=ECSensorVoorName, defaults=data)
                #print('ECSensorVoor aangemaakt = ',created)

            for idx2, ECn in enumerate(Meetstraat[idx].ECSensorNa):
                ECSensorNaName = "PG_{}Meetstraat{}.ECSensorNa{}".format(i+1,idx+1,idx2+1)
                data = {
                'meetstraat': rMeetstraat,
                'handlername': HandlerName,
                'nodeid': "ns={};s=pPG_{}Meetstraat".format(ns, i+1),
                'name': ECSensorNaName,
                'Value':ECn.Value,
                'ReadCompensatie':ECn.ReadCompensatie,
                'WriteCompensatie':ECn.WriteCompensatie,
                'CMDCompensatie':ECn.CMDCompensatie,
                'CMDCompensatieOK':ECn.CMDCompensatieOK,
                'CMDCompensatieERR':ECn.CMDCompensatieERR,
                }
                rECSensorNa, created = ECSensorNa.objects.update_or_create(name=ECSensorNaName, defaults=data)
                #print('ECSensorNa aangemaakt = ',created)

    except Exception as e:
        print(e)


#write values
def write_value_Doseerpomp(obj):
    try:
        struct,_ = get_struct(obj.nodeid)   #get struct van opcua server
        send = client.get_node(obj.nodeid)  #get node van opcua server
        for dos in struct:                  # voor het aantal doseerpompen in struct
            dos.Puls = int(obj.Puls)        #schrijf waardes van object naar struct
            dos.status = bool(obj.Status)   

        dv = ua.DataValue(ua.Variant(struct))   
        dv.ServerTimestamp = None           #timestamp is nodig om naar opcua server te kunnen sturen
        dv.SourceTimestamp = None
        send.set_value(dv)                  #send value
    except Exception as e:
        print('\x1b[6;30;41m' + 'fout opgetreden bij schrijven naar doseerpomp' + '\x1b[0m')

def write_value_Systeempomp(obj):
    try:
        struct,_ = get_struct(obj.nodeid)
        send = client.get_node(obj.nodeid)

        struct.Keuze                = int(obj.Keuze)
        struct.SlaveOf              = int(obj.SlaveOf)
        struct.StoringThermostaat   = bool(obj.StoringThermostaat)
        struct.DrukSensorZuig       = int(obj.DrukSensorZuig)
        struct.DrukSensorSysteem    = int(obj.DrukSensorSysteem)

        """FDStatus"""
        pgname = obj.name
        name = str(pgname +".FDStatus")
        obj = FDStatus.objects.get(name = name)
        struct.FDStatus.DriveStatus      = int(obj.DriveStatus)
        struct.FDStatus.DriveReady       = bool(obj.DriveReady)
        struct.FDStatus.DriveReversed    = bool(obj.DriveReversed)
        struct.FDStatus.DriveFault       = bool(obj.DriveFault)
        struct.FDStatus.DriveAlarm       = bool(obj.DriveAlarm)
        struct.FDStatus.DriveAtReference = bool(obj.DriveAtReference)
        struct.FDStatus.OutputFrequency  = int(obj.OutputFrequency)
        struct.FDStatus.ActiveFaultCode  = int(obj.ActiveFaultCode)
        struct.FDStatus.PIDFeedback      = int(obj.PIDFeedback)

        """FDControl"""
        name = str(pgname +".FDControl")
        obj = FDControl.objects.get(name = name)
        struct.FDControl.Start          = bool(obj.Start)
        struct.FDControl.Direction      = bool(obj.Direction)
        struct.FDControl.ResetFault     = bool(obj.ResetFault)
        struct.FDControl.PID_Reference  = int(obj.PID_Reference)

        dv = ua.DataValue(ua.Variant(struct))
        dv.ServerTimestamp = None
        dv.SourceTimestamp = None
        send.set_value(dv)
    except Exception as e:
        print(e)
        print('\x1b[6;30;41m' + 'fout opgetreden bij schrijven naar Systeempomp' + '\x1b[0m')

def write_value_Literteller(obj):                   #deze functie schrijft de waardes van de database naar de opcua server

    try:
        struct,_ = get_struct(obj.nodeid)           #haal struct op
        send = client.get_node(obj.nodeid)          #haal node op
        for liter in struct:                        #voor litterteller in list of littertellers
            liter.ResetLitersWatergift          = bool(obj.ResetLitersWatergift)    #schijf waardes van database naar struct (class)
            liter.AantalLitersPuls              = int(obj.AantalLitersPuls)
            liter.FlowActive                    = bool(obj.FlowActive)
            liter.TotaalAantalLitersWatergift   = int(obj.TotaalAantalLitersWatergift)
            liter.TotaalAantalM3                = int(obj.TotaalAantalM3)
            liter.TotaalAantalLiters            = int(obj.TotaalAantalLiters)
            liter.ActueleFlow                   = int(obj.ActueleFlow)

        dv = ua.DataValue(ua.Variant(struct))      #dit zet de struct in de juiste voor om verstruurd te worden 
        dv.ServerTimestamp = None                  #timestamps zijn nodig anders foutmelding
        dv.SourceTimestamp = None
        send.set_value(dv)                          #verstuur naar opcua server                   
    except Exception as e:
        print('\x1b[6;30;41m' + 'fout opgetreden bij schrijven naar Literteller' + '\x1b[0m') #print in kleur voor debug 
        print(e)    #print foutcode

def write_value_Waterfilter(obj):

    try:
        struct,_ = get_struct(obj.nodeid)
        send = client.get_node(obj.nodeid)
        for filter in struct:
            filter.Wachttijd            = int(obj.Wachttijd)
            filter.Hand                 = bool(obj.Hand)
            filter.Bedrijf              = bool(obj.Bedrijf)
            filter.Spoeltijd            = int(obj.Spoeltijd)
            filter.AantalSpoelbeurten   = int(obj.AantalSpoelbeurten)
            filter.DrukSensorVoor       = int(obj.DrukSensorVoor)


        dv = ua.DataValue(ua.Variant(struct))
        dv.ServerTimestamp = None
        dv.SourceTimestamp = None
        send.set_value(dv)
    except Exception as e:
        print('\x1b[6;30;41m' + 'fout opgetreden bij schrijven naar Waterfilter' + '\x1b[0m')
        print(e)

def write_value_Doseerstraat(obj):

    try:
        struct,_ = get_struct(obj.nodeid)
        send = client.get_node(obj.nodeid)
        for idx, straat in enumerate(struct):
            straat.MVPulstijd   = bool(obj.MVPulstijd)
            straat.MVPauzetijd  = bool(obj.MVPauzetijd)
            straat.MVKeuze      = int(obj.MVKeuze)
            straat.MVStatus     = int(obj.MVStatus)
            straat.MVActStand   = int(obj.MVActStand)
            for idx2, sv in enumerate(straat.SV):
                pgname = obj.name
                name = str(pgname +f".SV{idx2+1}")
                svobj = SV.objects.get(name=name)
                sv.ActStand = bool(svobj.ActStand)
                sv.Keuze    = int(svobj.Keuze)

        dv = ua.DataValue(ua.Variant(struct))
        dv.ServerTimestamp = None
        dv.SourceTimestamp = None
        send.set_value(dv)
    except Exception as e:
        print('\x1b[6;30;41m' + 'fout opgetreden bij schrijven naar DoseerStraat' + '\x1b[0m')
        print(e)

def write_value_Meetstraat(obj):

    try:
        struct,_ = get_struct(obj.nodeid)
        send = client.get_node(obj.nodeid)
        for idx, meet in enumerate(struct):
            meet.PHMaximaal          = int(obj.PHMaximaal)
            meet.PHMaxAfwijking      = int(obj.PHMaxAfwijking)
            meet.PHMaxTijdAfwijking  = int(obj.PHMaxTijdAfwijking)
            meet.PHAlarmSensor       = bool(obj.PHAlarmSensor)
            meet.PHAlarmRegeling     = bool(obj.PHAlarmRegeling)
            meet.ECMaximaal          = int(obj.ECMaximaal)
            meet.ECMaxAfwijking      = int(obj.ECMaxAfwijking)
            meet.ECMaxTijdAfwijking  = int(obj.ECMaxTijdAfwijking)
            meet.ECAlarmSensor       = bool(obj.ECAlarmSensor)
            meet.ECAlarmRegeling     = bool(obj.ECAlarmRegeling)
            meet.DrukSensor          = int(obj.DrukSensor)
            meet.OMSensorNa          = int(obj.OMSensorNa)
                    
            for idx2, phv in enumerate(meet.PHSensorVoor):
                pgname = obj.name
                name = str(pgname +f".PHSensorVoor{idx2+1}")
                PHsvobj = PHSensorVoor.objects.get(name=name)

                phv = int(PHsvobj.s1)

         
            for idx2, phn in enumerate(meet.PHSensorNa):
                pgname = obj.name
                name = str(pgname +f".PHSensorNa{idx2+1}")
                PHsnobj = PHSensorNa.objects.get(name=name)

                phn = int(PHsnobj.s1)
            
            for idx2, ecv in enumerate(meet.ECSensorVoor):
                pgname = obj.name
                name = str(pgname +f".ECSensorVoor{idx2+1}")
                ecvobj = ECSensorVoor.objects.get(name=name)

                ecv.Value               = int(ecvobj.Value)
                ecv.ReadCompensatie     = int(ecvobj.ReadCompensatie)
                ecv.WriteCompensatie    = int(ecvobj.WriteCompensatie)
                ecv.CMDCompensatie      = int(ecvobj.CMDCompensatie)
                ecv.CMDCompensatieOK    = int(ecvobj.CMDCompensatieOK)
                ecv.CMDCompensatieERR   = int(ecvobj.CMDCompensatieERR)

            for idx2, ecn in enumerate(meet.ECSensorNa):
                pgname = obj.name
                name = str(pgname +f".ECSensorNa{idx2+1}")
                ecnobj = ECSensorNa.objects.get(name=name)

                ecn.Value               = int(ecnobj.Value)
                ecn.ReadCompensatie     = int(ecnobj.ReadCompensatie)
                ecn.WriteCompensatie    = int(ecnobj.WriteCompensatie)
                ecn.CMDCompensatie      = int(ecnobj.CMDCompensatie)
                ecn.CMDCompensatieOK    = int(ecnobj.CMDCompensatieOK)
                ecn.CMDCompensatieERR   = int(ecnobj.CMDCompensatieERR)

        dv = ua.DataValue(ua.Variant(struct))
        dv.ServerTimestamp = None
        dv.SourceTimestamp = None
        send.set_value(dv)
    except Exception as e:
        print('\x1b[6;30;41m' + 'fout opgetreden bij schrijven naar Meetstraat' + '\x1b[0m')
        print(e)


#update values  
#deze functies worden aangeroepen door datachange
def update_value_Doseerpomp(nodeid, data):                         
    rDoseerpomp = DoseerPomp.objects.filter(handlername = nodeid)   #haal database object op
    for idx, dos in enumerate(rDoseerpomp):                         #voor alle doseerpompen in node
        obj = DoseerPomp.objects.get(name = dos.name)               #haal een doseerpomp op 
        Doseerpomp_Data = {                                         #schrijf ontvange data van opcua server in een dictionary
         'Puls': data[idx].Puls,
        'Status':data[idx].Status
        }
        for attr, value in  Doseerpomp_Data.items(): 
                setattr(obj, attr, value)                           #maak database object gelijk aan dictionary
        obj.save()                                                  #save to database

def update_value_Systeempomp(nodeid, data):
    Systeempomp_Data = {
            'Keuze': data.Keuze,
            'SlaveOf': data.SlaveOf,
            'StoringThermostaat': data.StoringThermostaat,
            'DrukSensorZuig': data.DrukSensorZuig,
            'DrukSensorSysteem': data.DrukSensorSysteem
        }
    rSysteempomp, created = SysteemPomp.objects.get_or_create(handlername = nodeid, defaults=Systeempomp_Data)

    for attr, value in  Systeempomp_Data.items(): 
        setattr(rSysteempomp, attr, value)
    rSysteempomp.save()

    Systeempomp_FDStatus_Data = {
        'DriveStatus':data.FDStatus.DriveStatus,
        'DriveReady':data.FDStatus.DriveReady,
        'DriveRun':data.FDStatus.DriveRun,
        'DriveReversed':data.FDStatus.DriveReversed,
        'DriveFault': data.FDStatus.DriveFault,
        'DriveAlarm': data.FDStatus.DriveAlarm,
        'DriveAtReference':data.FDStatus.DriveAtReference,
        'OutputFrequency':data.FDStatus.OutputFrequency,
        'ActiveFaultCode':data.FDStatus.ActiveFaultCode,
        'PIDFeedback':data.FDStatus.PIDFeedback,
        }
    rFDStatus, created = FDStatus.objects.get_or_create(handlername = nodeid ,defaults=Systeempomp_FDStatus_Data)

    for attr, value in  Systeempomp_FDStatus_Data.items(): 
        setattr(rFDStatus, attr, value)
    rFDStatus.save()

    Systeempomp_FDControl_data = {
        'Start':data.FDControl.Start,
        'Direction':data.FDControl.Direction,
        'ResetFault':data.FDControl.ResetFault,
        'PID_Reference':data.FDControl.PID_Reference
        }
    rFDControl, created = FDControl.objects.get_or_create(handlername = nodeid, defaults=Systeempomp_FDControl_data)

    for attr, value in  Systeempomp_FDControl_data.items(): 
        setattr(rFDControl, attr, value)
    rFDControl.save()

def update_value_Literteller(nodeid, data):                         #deze functies worden geroepen door de Datachange subhandler
    rLiterteller = LiterTeller.objects.filter(handlername = nodeid) #haal alle litertellers in database object op
    for idx, literteller in enumerate(rLiterteller):                #loop door alle litertellers in database
        obj = LiterTeller.objects.get(name = literteller.name)      #haal één literteller op 
        Literteller_Data = {                                        #schrijf ontvangen data van opcua server in dictionary 
                'ResetLitersWatergift':data[idx].ResetLitersWatergift,
                'AantalLitersPuls':data[idx].AantalLitersPuls,
                'FlowActive':data[idx].FlowActive,
                'TotaalAantalLitersWatergift':data[idx].TotaalAantalLitersWatergift,
                'TotaalAantalM3': data[idx].TotaalAantalM3,
                'TotaalAantalLiters': data[idx].TotaalAantalLiters,
                'ActueleFlow':data[idx].ActueleFlow,
                }
        for attr, value in  Literteller_Data.items():                #maak database object gelijk aan dictionary
                setattr(obj, attr, value)
        obj.save()                                                   #save to database
        # print('Literteller updated')

def update_value_Waterfilter(nodeid, data):
    rWaterfilter = WaterFilter.objects.filter(handlername = nodeid)
    for idx, waterfilter in enumerate(rWaterfilter):
        obj = WaterFilter.objects.get(name = waterfilter.name)
        Waterfilter_Data = {
            'Hand':data[idx].Hand,
            'Bedrijf':data[idx].Bedrijf,
            'Wachttijd':data[idx].Wachttijd,
            'Spoeltijd':data[idx].Spoeltijd,
            'AantalSpoelbeurten': data[idx].AantalSpoelbeurten,
            'DrukSensorVoor': data[idx].DrukSensorVoor,
            }

        for attr, value in  Waterfilter_Data.items(): 
                setattr(obj, attr, value)
        obj.save()
        # print('Waterfilter updated')

def update_value_Doseerstraat(nodeid, data):
    rDoseerstraat = DoseerStraat.objects.filter(handlername = nodeid)
    for idx, straat in enumerate(rDoseerstraat):
        obj = DoseerStraat.objects.get(name = straat.name)
        Doseerstraatdata = {
            'MVPulstijd':data[idx].MVPulstijd,
            'MVPauzetijd':data[idx].MVPauzetijd,
            'MVKeuze':data[idx].MVKeuze,
            'MVStatus':data[idx].MVStatus,
            'MVActStand': data[idx].MVActStand,
            }
        for attr, value in  Doseerstraatdata.items(): 
                setattr(obj, attr, value)
        obj.save()
        #print('Doseerstraat updated')
        rSV = SV.objects.filter(handlername = nodeid)
        for idx2, sv in zip(range(len(data[idx].SV)), rSV):
            obj = SV.objects.get(name = sv.name) 
            SVdata = {
                'Keuze': data[idx].SV[idx2].Keuze,
                'ActStand': data[idx].SV[idx2].ActStand,
            }
            for attr, value in  SVdata.items(): 
                setattr(obj, attr, value)
            obj.save()
                #print('SV updated')

def update_value_Meetstraat(nodeid, data):
    rMeetstraat = MeetStraat.objects.filter(handlername = nodeid)
    for idx, meet in enumerate(rMeetstraat):
        obj = MeetStraat.objects.get(name = meet.name)
        Meetstraatdata = {
            'PHMaximaal':data[idx].PHMaximaal,
            'PHMaxAfwijking':data[idx].PHMaxAfwijking,
            'PHMaxTijdAfwijking':data[idx].PHMaxTijdAfwijking,
            'PHAlarmSensor':data[idx].PHAlarmSensor,
            'PHAlarmRegeling': data[idx].PHAlarmRegeling,
            'ECMaximaal': data[idx].ECMaximaal,
            'ECMaxAfwijking':data[idx].ECMaxAfwijking,
            'ECMaxTijdAfwijking':data[idx].ECMaxTijdAfwijking,
            'ECAlarmSensor':data[idx].ECAlarmSensor,
            'ECAlarmRegeling':data[idx].ECAlarmRegeling,
            'DrukSensor':data[idx].DrukSensor,
            'OMSensorNa':data[idx].OMSensorNa,
            }
        for attr, value in  Meetstraatdata.items(): 
                setattr(obj, attr, value)
        obj.save()
        #print('Meetstraat updated')

        rPHSv = PHSensorVoor.objects.filter(handlername = nodeid)
        for idx2, PHSv in enumerate(rPHSv):
            obj = PHSensorVoor.objects.get(name = PHSv)
            PHSvdata = {
                's1':data[idx].PHSensorVoor[0],
                's2':data[idx].PHSensorVoor[1],
                's2':data[idx].PHSensorVoor[2],
            }
            for attr, value in  PHSvdata.items(): 
                setattr(obj, attr, value)
            obj.save()
            #print('PH Sensor Voor updated')

        rPHSn = PHSensorNa.objects.filter(handlername = nodeid)
        for idx2, PHSn in enumerate(rPHSn):
            obj = PHSensorNa.objects.get(name = PHSn)
            PHSvdata = {
                's1':data[idx].PHSensorNa[0],
                's2':data[idx].PHSensorNa[1],
                's2':data[idx].PHSensorNa[2],
            }
            for attr, value in  PHSvdata.items(): 
                setattr(obj, attr, value)
            obj.save()
            #print('PH Sensor Na updated')


        try:
            rECSv = ECSensorVoor.objects.filter(handlername = nodeid)
            for idx2, ECSv in enumerate(rECSv):
                obj = ECSensorVoor.objects.get(name = ECSv)
                ECSvdata = {
                    'Value':data[idx].ECSensorVoor[idx2].Value,
                    'ReadCompensatie':data[idx].ECSensorVoor[idx2].ReadCompensatie,
                    'WriteCompensatie':data[idx].ECSensorVoor[idx2].WriteCompensatie,
                    'CMDCompensatie':data[idx].ECSensorVoor[idx2].CMDCompensatie,
                    'CMDCompensatieOK':data[idx].ECSensorVoor[idx2].CMDCompensatieOK,
                    'CMDCompensatieERR':data[idx].ECSensorVoor[idx2].CMDCompensatieERR,
                    }
                for attr, value in  ECSvdata.items(): 
                    setattr(obj, attr, value)
                obj.save()
                #print('EC Sensor voor updated')
        except Exception as e:
            print(e)
            print("idx2= ",idx2)



        rECSn = ECSensorNa.objects.filter(handlername = nodeid)
        for idx2, ECSn in enumerate(rECSn):
            obj = ECSensorNa.objects.get(name = ECSn)
            ECSndata = {
                'Value':data[idx].ECSensorNa[idx2].Value,
                'ReadCompensatie':data[idx].ECSensorNa[idx2].ReadCompensatie,
                'WriteCompensatie':data[idx].ECSensorNa[idx2].WriteCompensatie,
                'CMDCompensatie':data[idx].ECSensorNa[idx2].CMDCompensatie,
                'CMDCompensatieOK':data[idx].ECSensorNa[idx2].CMDCompensatieOK,
                'CMDCompensatieERR':data[idx].ECSensorNa[idx2].CMDCompensatieERR,
                }
            for attr, value in  ECSndata.items(): 
                setattr(obj, attr, value)
            obj.save()
            #print('EC Sensor Na updated', ECSndata)


class SubHandler(object):                                       #deze class wordt geroepen als een variable waarop gesubscribed is in de plc veranderd
    def datachange_notification(node, val, data,attr):          
        print("Python: New data change event", node, val)
        update_models(val.nodeid.Identifier,data)               #stuur de naam en de data door

class Sub:
    def subscribe(self):
        handler = SubHandler()      
        self.opcua_subscription = client.create_subscription(100, handler)   #maak subscripties
        print("subscribe")
        self.opcua_handle = self.opcua_subscription.subscribe_data_change(subscribeNodes) #subscribe to datachanges met de subscribeNodes list 

    def unsubscribe(self):
        print("unsubscribe")
        self.opcua_subscription.unsubscribe(self.opcua_handle)            #unsubsctibe to datachanges met behulp van de handle


def update_models(name,data):                                   #deze functie zoekt uit welke waarde veranderd is aan de hand van de naam
    for i in range(10):
        if name == f'pPG_{i}_DoseerPomp':
            update_value_Doseerpomp(name,data)                  #update de database objects
        elif name == f'pPG_{i}_SysteemPomp':
            update_value_Systeempomp(name,data)
        elif name == f'pPG_{i}_LiterTeller':
             update_value_Literteller(name,data)
        elif name == f'pPG_{i}_WaterFilter':
            update_value_Waterfilter(name,data)      
        elif name == f'pPG_{i}_DoseerStraat':
            update_value_Doseerstraat(name,data)     
        elif name == f'pPG_{i}_MeetStraat':
            update_value_Meetstraat(name,data) 


#progressbar
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()



maakpompgroep()             #maak pompgroep objects aan en haal waarde van de server op
s = Sub()
s.subscribe()               #subscribe op data change

 
def stop():                 #kan gebruikt worden om opcua goed af te sluiten
    s.unsubscribe()                                           #unsubsctibe to datachanges met behulp van de handle
    disconnectopcua()                                       #disconnect opcua

def Start():                #kan gebruikt worden om te verbinden met opcua en subscripties aan te maken                
    connectopcua()
    s.subscribe()


#dit is een test voor github