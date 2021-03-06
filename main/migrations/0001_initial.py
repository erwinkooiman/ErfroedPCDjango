# Generated by Django 3.2.9 on 2021-11-16 10:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DoseerStraat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('nodeid', models.CharField(default='SOME STRING', max_length=200)),
                ('MVPulstijd', models.CharField(max_length=200)),
                ('MVPauzetijd', models.CharField(max_length=200)),
                ('MVKeuze', models.CharField(max_length=200)),
                ('MVStatus', models.CharField(max_length=200)),
                ('MVActStand', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='MeetStraat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('nodeid', models.CharField(default='SOME STRING', max_length=200)),
                ('PHMaximaal', models.CharField(max_length=200)),
                ('PHMaxAfwijking', models.CharField(max_length=200)),
                ('PHMaxTijdAfwijking', models.CharField(max_length=200)),
                ('PHAlarmSensor', models.BooleanField(max_length=200)),
                ('PHAlarmRegeling', models.BooleanField(max_length=200)),
                ('ECMaximaal', models.CharField(max_length=200)),
                ('ECMaxAfwijking', models.CharField(max_length=200)),
                ('ECMaxTijdAfwijking', models.CharField(max_length=200)),
                ('ECAlarmSensor', models.BooleanField(max_length=200)),
                ('ECAlarmRegeling', models.BooleanField(max_length=200)),
                ('DrukSensor', models.CharField(max_length=200)),
                ('OMSensorNa', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='PG',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ToDoList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='WaterFilter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('nodeid', models.CharField(default='SOME STRING', max_length=200)),
                ('Hand', models.BooleanField(max_length=200)),
                ('Bedrijf', models.BooleanField(max_length=200)),
                ('Wachttijd', models.CharField(max_length=200)),
                ('Spoeltijd', models.CharField(max_length=200)),
                ('AantalSpoelbeurten', models.CharField(max_length=200)),
                ('DrukSensorVoor', models.CharField(max_length=200)),
                ('pg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.pg')),
            ],
        ),
        migrations.CreateModel(
            name='SysteemPomp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('nodeid', models.CharField(default='SOME STRING', max_length=200)),
                ('Keuze', models.CharField(max_length=200)),
                ('SlaveOf', models.CharField(max_length=200)),
                ('StoringThermostaat', models.BooleanField(default=False)),
                ('DrukSensorZuig', models.CharField(max_length=200)),
                ('DrukSensorSysteem', models.CharField(max_length=200)),
                ('pg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.pg')),
            ],
        ),
        migrations.CreateModel(
            name='SV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('nodeid', models.CharField(default='SOME STRING', max_length=200)),
                ('Keuze', models.CharField(max_length=200)),
                ('ActStand', models.BooleanField(max_length=200)),
                ('doseerstraat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.doseerstraat')),
            ],
        ),
        migrations.CreateModel(
            name='PHSensorVoor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('nodeid', models.CharField(default='SOME STRING', max_length=200)),
                ('value', models.CharField(max_length=200)),
                ('meetstraat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.meetstraat')),
            ],
        ),
        migrations.CreateModel(
            name='PHSensorNa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('nodeid', models.CharField(default='SOME STRING', max_length=200)),
                ('value', models.CharField(max_length=200)),
                ('meetstraat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.meetstraat')),
            ],
        ),
        migrations.AddField(
            model_name='meetstraat',
            name='pg',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.pg'),
        ),
        migrations.CreateModel(
            name='LiterTeller',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('nodeid', models.CharField(default='SOME STRING', max_length=200)),
                ('ResetLitersWatergift', models.BooleanField(max_length=200)),
                ('AantalLitersPuls', models.CharField(max_length=200)),
                ('FlowActive', models.BooleanField(max_length=200)),
                ('TotaalAantalLitersWatergift', models.CharField(max_length=200)),
                ('TotaalAantalM3', models.CharField(max_length=200)),
                ('TotaalAantalLiters', models.CharField(max_length=200)),
                ('ActueleFlow', models.CharField(max_length=200)),
                ('pg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.pg')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=300)),
                ('complete', models.BooleanField()),
                ('todolist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.todolist')),
            ],
        ),
        migrations.CreateModel(
            name='FDStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('nodeid', models.CharField(default='SOME STRING', max_length=200)),
                ('DriveStatus', models.CharField(max_length=200)),
                ('DriveReady', models.BooleanField(max_length=200)),
                ('DriveRun', models.BooleanField(max_length=200)),
                ('DriveReversed', models.BooleanField(max_length=200)),
                ('DriveFault', models.BooleanField(max_length=200)),
                ('DriveAlarm', models.BooleanField(max_length=200)),
                ('DriveAtReference', models.BooleanField(max_length=200)),
                ('OutputFrequency', models.CharField(max_length=200)),
                ('ActiveFaultCode', models.CharField(max_length=200)),
                ('PIDFeedback', models.CharField(max_length=200)),
                ('pg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.pg')),
            ],
        ),
        migrations.CreateModel(
            name='FDControl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('nodeid', models.CharField(default='SOME STRING', max_length=200)),
                ('Start', models.BooleanField(max_length=200)),
                ('Direction', models.BooleanField(max_length=200)),
                ('ResetFault', models.BooleanField(max_length=200)),
                ('PID_Reference', models.CharField(max_length=200)),
                ('pg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.pg')),
            ],
        ),
        migrations.CreateModel(
            name='ECSensorVoor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('nodeid', models.CharField(default='SOME STRING', max_length=200)),
                ('Value', models.CharField(max_length=200)),
                ('ReadCompensatie', models.CharField(max_length=200)),
                ('WriteCompensatie', models.CharField(max_length=200)),
                ('CMDCompensatie', models.CharField(max_length=200)),
                ('CMDCompensatieOK', models.BooleanField(max_length=200)),
                ('CMDCompensatieERR', models.BooleanField(max_length=200)),
                ('meetstraat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.meetstraat')),
            ],
        ),
        migrations.CreateModel(
            name='ECSensorNa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('nodeid', models.CharField(default='SOME STRING', max_length=200)),
                ('Value', models.CharField(max_length=200)),
                ('ReadCompensatie', models.CharField(max_length=200)),
                ('WriteCompensatie', models.CharField(max_length=200)),
                ('CMDCompensatie', models.CharField(max_length=200)),
                ('CMDCompensatieOK', models.BooleanField(max_length=200)),
                ('CMDCompensatieERR', models.BooleanField(max_length=200)),
                ('meetstraat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.meetstraat')),
            ],
        ),
        migrations.AddField(
            model_name='doseerstraat',
            name='pg',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.pg'),
        ),
        migrations.CreateModel(
            name='DoseerPomp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('nodeid', models.CharField(default='SOME STRING', max_length=200)),
                ('Puls', models.BooleanField()),
                ('Status', models.CharField(max_length=200)),
                ('pg', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.pg')),
            ],
        ),
    ]
