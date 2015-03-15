# -*- coding: utf-8 -*-

import csv
try:
    import StringIO
except:
    from io import StringIO
import datetime as dt
import re

from django.conf import settings

from nptime import nptime
from pymongo import MongoClient
import arrow
import mongoengine

from . import choices, patterns


class Company(mongoengine.Document):

    """Modelo de compañias."""

    name = mongoengine.StringField(
        unique=True, max_length=255, verbose_name=u'nombre')
    idoidd = mongoengine.ListField(
        mongoengine.IntField(), verbose_name=u'idoidd')
    code = mongoengine.IntField(verbose_name=u'codigo')
    schedules = mongoengine.DictField(verbose_name=u'horarios')
    invoicing = mongoengine.StringField(
        choices=choices.INVOICING, verbose_name=u'facturación')
    id_compania = mongoengine.IntField()

    meta = {
        'ordering': ['name']
    }

    def __unicode__(self):
        return self.name


class Numeration(mongoengine.Document):

    """Modelo de las numeraciones."""

    numeration = mongoengine.StringField()
    company = mongoengine.ReferenceField(
        Company, reverse_delete_rule=mongoengine.CASCADE)

    meta = {
        'indexes': ['numeration']
    }

    def __unicode__(self):
        return self.numeration

    def get_range(self):
        return self._range

    @classmethod
    def upload(cls, filename):
        numbers = csv.DictReader(filename, delimiter=',')

        def reader_to_portability(reader):
            for r in reader:
                c = Company.objects.filter(
                    idoidd__in=[int(r['ido'])]).first()
                yield cls(
                    numeration='%s%s' % (r['zona'], r['rango']), company=c)

        cls.objects.delete()
        cls.objects.insert(reader_to_portability(numbers), load_bulk=False)


class Commune(mongoengine.Document):

    """Modelo que representa las comunas"""

    name = mongoengine.StringField(verbose_name='nombre')
    code = mongoengine.StringField(verbose_name='codigo')
    region = mongoengine.StringField(verbose_name='region')
    province = mongoengine.StringField(verbose_name='provincia')
    area = mongoengine.StringField(verbose_name='area')
    zone = mongoengine.StringField(verbose_name='zona')
    primary = mongoengine.StringField(verbose_name='primaria')

    def __unicode__(self):
        return self.name


class Line(mongoengine.Document):

    """Modelo de los clientes de convergia."""

    number = mongoengine.StringField(unique=True, verbose_name=u'numero')
    name = mongoengine.StringField(max_length=255, verbose_name=u'nombre')
    entity = mongoengine.StringField(
        choices=choices.ENTITIES, verbose_name=u'entidad')
    comments = mongoengine.StringField(verbose_name=u'comentarios')
    zone = mongoengine.IntField(verbose_name=u'area')
    city = mongoengine.IntField(verbose_name=u'comuna')
    company = mongoengine.IntField(default=333)
    rut = mongoengine.StringField(
        max_length=12, verbose_name=u'rut propietario')
    service = mongoengine.StringField(
        choices=choices.SERVICES, verbose_name=u'servicio', default='voip')
    mode = mongoengine.StringField(
        choices=choices.MODES, verbose_name=u'modalidad', default='postpago')
    due = mongoengine.FloatField(verbose_name=u'deuda vencida', default=0.0000)
    active = mongoengine.BooleanField(default=False, verbose_name=u'activo')
    document = mongoengine.IntField(verbose_name=u'documento')
    special_service = mongoengine.StringField(
        choices=choices.SPECIAL_SERVICES, verbose_name=u'servicio especial')
    commune = mongoengine.ReferenceField(Commune)

    meta = {
        'ordering': ['number'],
        'indexes': [('zone', 'city', 'entity', 'mode')]
    }

    def __unicode__(self):
        return str(self.number)

    @classmethod
    def get_services(cls, date):
        map_f = """
        function() {
            emit({commune: this.commune}, {count: 1, entity: this.entity});
        }"""
        reduce_f = """
        function(key, values) {
            var count = 0;
            values.forEach(function(v) {
                if (v.entity == 'empresa') {
                    count += v.count;
                }
            });
            return {count: count};
        }"""
        results = cls.objects.map_reduce(
            map_f, reduce_f, output='inline')

        def services_cb(obj):
            c = Commune.objects.get(pk=obj.key.get('commune'))
            return [
                314, date, c.primary, c.area, c.code, 1,
                'TB', 'RE', 'H', 'PP', 'D', '0', int(obj.value.get('count'))]

        r_filter = filter(lambda x: x.key.get('commune') is not None, results)

        return map(services_cb, r_filter)

    @classmethod
    def get_subscriptors(cls, date):
        count = cls.objects(
            entity='empresa', number__startswith='564469').count()

        return [[314, date, 'CO', count]] if count > 0 else [[]]


class Cdr(mongoengine.Document):

    """Modelo de los cdr."""

    year = mongoengine.StringField(
        max_length=4, choices=choices.YEARS, verbose_name='año', required=True)
    month = mongoengine.StringField(
        max_length=2, choices=choices.MONTHS, verbose_name='mes',
        required=True)
    incoming_ctc = mongoengine.FileField(verbose_name='CTC', required=True)
    incoming_entel = mongoengine.FileField(verbose_name='ENTEL', required=True)
    outgoing = mongoengine.FileField(verbose_name='STI', required=True)
    processed = mongoengine.BooleanField(default=False)

    def __unicode__(self):
        return u'{0}-{1}'.format(self.year, self.month)

    def get_date(self):
        """Retorna la fecha para traficos."""
        return self.year + self.month

    def get_valid(self, ani, final_number, dialed_number, ingress_duration):
        """Funcion que determina si un registro debe o no ser facturado"""
        p1 = re.search(patterns.national, ani)
        p2 = re.search(patterns.national, final_number)
        p3 = re.search(patterns.special2, final_number)
        p4 = re.search(patterns.pattern_112, dialed_number)
        p5 = len(ani) == 11 and re.search(patterns.valid_ani, ani)
        p6 = ingress_duration > 0

        return True if p1 and p2 and not p3 and not p4 and p5 and p6 else False

    def get_type_incoming(self, ani, final_number):
        """Funcion que determina el tipo de llamada"""
        if re.search(patterns.pattern_564469, final_number):
            if re.search(patterns.movil, ani):
                return 'voip-movil'

            elif not re.search(patterns.national, ani):
                return 'voip-ldi'

            else:
                return 'voip-local'

        else:
            if re.search(patterns.movil, ani):
                return 'movil'

            elif not re.search(patterns.national, ani):
                return 'internacional'

            elif re.search(patterns.santiago, ani):
                return 'local'

            elif re.search(patterns.special, ani):
                return 'especial'

            else:
                return 'nacional'

    def get_day(self, connect_time, festives):
        if connect_time.date() in festives:
            return 'festive'

        else:
            if connect_time.weekday() in range(5):
                return 'bussines'

            elif connect_time.weekday() == 5:
                return 'saturday'

            else:
                return 'festive'

    def schedule_compay(self, fecha_llamada, hora_llamada, compania):
        def get_schedule(name):
            tipo = dia.get(name)

            if tipo:
                start = dt.datetime.strptime(tipo['start'], '%H:%M:%S').time()
                end = dt.datetime.strptime(tipo['end'], '%H:%M:%S').time()

                if start < end:
                    if start <= hora_llamada <= end:
                        return name

                else:
                    if start <= hora_llamada <= dt.time(23, 59, 59):
                        return name

                    elif dt.time(0, 0) <= hora_llamada <= end:
                        return name

            else:
                return None

        dia = compania.schedules.get(self.get_day(fecha_llamada))

        if dia:
            for n in ['normal', 'reducido', 'nocturno']:
                tipo = get_schedule(n)

                if tipo is not None:
                    return tipo

        else:
            return None

    def split_schedule(self, connect_time, duracion, compania):
        def split1(start, end):
            start = nptime().from_time(
                dt.datetime.strptime(start, '%H:%M:%S').time())
            end = nptime().from_time(
                dt.datetime.strptime(end, '%H:%M:%S').time())

            if hora_inicio < start < hora_fin:
                duracion1 = int((start - hora_inicio).total_seconds())
                duracion2 = int((hora_fin - start).total_seconds())

                return (
                    {
                        'fecha_llamada': fecha_llamada,
                        'hora_inicio': hora_inicio,
                        'duracion': duracion1
                    },
                    {
                        'fecha_llamada': fecha_llamada,
                        'hora_inicio': start,
                        'duracion': duracion2})

            elif hora_inicio < end < hora_fin:
                duracion1 = int((end - hora_inicio).total_seconds())
                duracion2 = int((hora_fin - end).total_seconds())

                return (
                    {
                        'fecha_llamada': fecha_llamada,
                        'hora_inicio': hora_inicio,
                        'duracion': duracion1
                    },
                    {
                        'fecha_llamada': fecha_llamada,
                        'hora_inicio': end + dt.timedelta(seconds=1),
                        'duracion': duracion2})

            else:
                return None

        def split2(start, end):
            start = nptime().from_time(
                dt.datetime.strptime(start, '%H:%M:%S').time())
            end = nptime().from_time(
                dt.datetime.strptime(end, '%H:%M:%S').time())

            if hora_inicio < start < dt.time(23, 59, 59):
                duracion1 = int((start - hora_inicio).total_seconds())
                duracion2 = int((nptime(23, 59, 59) - start).total_seconds())
                duracion3 = int((hora_fin - nptime(0, 0)).total_seconds()) + 1

                return (
                    {
                        'fecha_llamada': fecha_llamada,
                        'hora_inicio': hora_inicio,
                        'duracion': duracion1
                    },
                    {
                        'fecha_llamada': fecha_llamada,
                        'hora_inicio': start,
                        'duracion': duracion2
                    },
                    {
                        'fecha_llamada': fecha_llamada + dt.timedelta(
                            days=1),
                        'hora_inicio': nptime(0, 0),
                        'duracion': duracion3})

            elif hora_inicio < end < dt.time(23, 59, 59):
                duracion1 = int((end - hora_inicio).total_seconds())
                duracion2 = int((nptime(23, 59, 59) - end).total_seconds())
                duracion3 = int((hora_fin - nptime(0, 0)).total_seconds()) + 1

                return (
                    {
                        'fecha_llamada': fecha_llamada,
                        'hora_inicio': hora_inicio,
                        'duracion': duracion1
                    },
                    {
                        'fecha_llamada': fecha_llamada,
                        'hora_inicio': end + dt.timedelta(seconds=1),
                        'duracion': duracion2
                    },
                    {
                        'fecha_llamada': fecha_llamada + dt.timedelta(
                            days=1),
                        'hora_inicio': nptime(0, 0),
                        'duracion': duracion3
                    }
                )

            elif dt.time(0, 0) < start < hora_fin:
                d1 = int((nptime(23, 59, 59) - hora_inicio).total_seconds())
                d2 = int((start - nptime(0, 0)).total_seconds()) + 1
                d3 = int((hora_fin - start).total_seconds())

                return (
                    {
                        'fecha_llamada': fecha_llamada,
                        'hora_inicio': hora_inicio,
                        'duracion': d1
                    },
                    {
                        'fecha_llamada': fecha_llamada + dt.timedelta(
                            days=1),
                        'hora_inicio': nptime(0, 0),
                        'duracion': d2
                    },
                    {
                        'fecha_llamada': fecha_llamada + dt.timedelta(
                            days=1),
                        'hora_inicio': start,
                        'duracion': d3})

            elif dt.time(0, 0) <= end <= hora_fin:
                d1 = int((nptime(23, 59, 59) - hora_inicio).total_seconds())
                d2 = int((end - nptime(0, 0)).total_seconds()) + 1
                d3 = int((hora_fin - end).total_seconds())

                return (
                    {
                        'fecha_llamada': fecha_llamada,
                        'hora_inicio': hora_inicio,
                        'duracion': d1
                    },
                    {
                        'fecha_llamada': fecha_llamada + dt.timedelta(
                            days=1),
                        'hora_inicio': nptime(0, 0),
                        'duracion': d2
                    },
                    {
                        'fecha_llamada': fecha_llamada + dt.timedelta(
                            days=1),
                        'hora_inicio': end + dt.timedelta(seconds=1),
                        'duracion': d3
                    },
                )

            else:
                return None

        fecha_llamada = connect_time.date()
        hora_inicio = nptime().from_time(connect_time.time())
        hora_fin = hora_inicio + dt.timedelta(seconds=float(duracion))

        if hora_inicio <= hora_fin:
            dia = compania.schedules.get(self.get_day(fecha_llamada))

            if dia:
                for n in ['normal', 'reducido', 'nocturno']:
                    tipo = dia.get(n)

                    if tipo:
                        output = split1(tipo['start'], tipo['end'])

                        if output is not None:
                            return output

            return ({
                'fecha_llamada': fecha_llamada,
                'hora_inicio': hora_inicio,
                'duracion': duracion},)

        else:
            dia = compania.schedules.get(self.get_day(fecha_llamada))

            if dia:
                for n in ['normal', 'reducido', 'nocturno']:
                    tipo = dia.get(n)

                    if tipo:
                        output = split2(tipo['start'], tipo['end'])

                        if output is not None:
                            return output

            return ({
                'fecha_llamada': fecha_llamada,
                'hora_inicio': hora_inicio,
                'duracion': duracion},)

    def get_entity(self, final_number):
        l = Line.objects(number=final_number).first()

        return None if l is None else l.entity

    def insert_incoming(self, name):
        if name == 'ENTEL':
            incoming = self.incoming_entel.read()

        else:
            incoming = self.incoming_ctc.read()

        incoming_file = StringIO.StringIO(incoming)
        incoming_dict = csv.DictReader(incoming_file, delimiter=',')
        date = '%s-%s' % (self.year, self.month)
        start = arrow.get('%s-01' % date, 'YYYY-MM-DD')
        end = start.replace(months=1)
        festives = Holiday.objects(
            date__gte=start, date__lt=end).values_list('date')
        festives = [f.date() for f in festives]

        def reader_to_incomming(reader):
            for r in reader:
                connect_time = arrow.get(
                    r['CONNECT_TIME'], 'YYYY-MM-DD HH:mm:ss')
                disconnect_time = arrow.get(
                    r['DISCONNECT_TIME'], 'YYYY-MM-DD HH:mm:ss')
                _type = self.get_type_incoming(r['ANI'], r['DIALED_NUMBER'])

                if re.search(patterns.pattern_num_6, r['ANI']):
                    numeration = r['ANI'][2:][:6]

                else:
                    numeration = r['ANI'][2:][:5]

                day = self.get_day(connect_time, festives)
                ingress_duration = int(r['INGRESS_DURATION'])
                valid = self.get_valid(
                    r['ANI'], r['FINAL_NUMBER'], r['DIALED_NUMBER'],
                    ingress_duration)
                weekday = connect_time.weekday()

                if not valid:
                    observation = 'No cumple con los filtros'

                else:
                    observation = None

                yield Incoming(
                    connect_time=connect_time,
                    disconnect_time=disconnect_time,
                    ani=r['ANI'],
                    ani_number=r['ANI_NUMBER'],
                    ingress_duration=ingress_duration,
                    dialed_number=r['DIALED_NUMBER'],
                    final_number=r['FINAL_NUMBER'],
                    cdr=self,
                    valid=valid,
                    numeration=numeration,
                    _type=_type,
                    weekday=weekday,
                    observation=observation,
                    day=day)

        Incoming.objects.insert(
            reader_to_incomming(incoming_dict), load_bulk=False)

        for c in Portability.objects.distinct('company'):
            numbers = Portability.objects.filter(company=c).values_list(
                'number')
            Incoming.objects.filter(
                cdr=self, valid=True, ani__in=numbers,
                company=None).update(set__company=c)

        for c in Numeration.objects.distinct('company'):
            numerations = Numeration.objects.filter(company=c).values_list(
                'numeration')
            Incoming.objects.filter(
                cdr=self, valid=True, numeration__in=numerations,
                company=None).update(set__company=c)

        Incoming.objects.filter(
            cdr=self, valid=True, company=None).update(
                set__valid=False, set__observation='Sin empresa')
        date = '%s-%s' % (self.year, self.month)
        start = arrow.get('%s-01' % date, 'YYYY-MM-DD')
        end = start.replace(months=1)
        festives = Holiday.objects(
            date__gte=start, date__lt=end).values_list('date')
        festives = [f.date() for f in festives]

        for i in Incoming.objects.filter(cdr=self, valid=True):
            for d in c.schedules.keys():
                day = c.schedules.get(t)
                types = day.keys()

                for i, t in enumerate(types):
                    day_type = day.get(t)
                    time_start = arrow.get(
                        day_type.get('start'), 'H:mm:ss')
                    time_end = arrow.get(
                        day_type.get('end'), 'H:mm:ss')

                    if d == 'festive':
                        for f in festives:
                            start = arrow.get(f)

                            if time_start < time_end:
                                start = start.replace(
                                    hour=time_start.hour,
                                    minute=time_start.minute,
                                    second=time_start.second)
                                end = start.replace(
                                    hour=time_end.hour,
                                    minute=time_end.minute,
                                    second=time_end.second)
                                Incoming.objects.filter(
                                    cdr=self, valid=True, company=c,
                                    connect_time__gte=start,
                                    connect_time__lte=end).update(
                                        set__schedule=t)

                            else:
                                start = start.replace(
                                    hour=time_start.hour,
                                    minute=time_start.minute,
                                    second=time_start.second)
                                end = start.replace(
                                    hour=23,
                                    minute=59,
                                    second=59)
                                Incoming.objects.filter(
                                    cdr=self, valid=True, company=c,
                                    connect_time__gte=start,
                                    connect_time__lte=end).update(
                                        set__schedule=t)
                                start = start.replace(
                                    hour=0,
                                    minute=0,
                                    second=0)
                                end = start.replace(
                                    hour=time_end.hour,
                                    minute=time_end.minute,
                                    second=time_end.second)
                                Incoming.objects.filter(
                                    cdr=self, valid=True, company=c,
                                    connect_time__gte=start,
                                    connect_time__lte=end).update(
                                        set__schedule=t)

                    elif d == 'bussines':
                        for i in Incoming.objects.filter(
                                cdr=self, valid=True, company=c,
                                weekday__gte=0,
                                weekday__lte=4,
                                schedule=None):
                            start = arrow.get(i.connect_time)

                            if time_start < time_end:
                                s = start.replace(
                                    hour=time_start.hour,
                                    minute=time_start.minute,
                                    second=time_start.second)
                                e = start.replace(
                                    hour=time_end.hour,
                                    minute=time_end.minute,
                                    second=time_end.second)

                                if s <= arrow.get(i.connect_time) <= e:
                                    i.schedule = t
                                    i.save()

                            else:
                                s = start.replace(
                                    hour=time_start.hour,
                                    minute=time_start.minute,
                                    second=time_start.second)
                                e = start.replace(
                                    hour=23,
                                    minute=59,
                                    second=59)

                                if s <= arrow.get(i.connect_time) <= e:
                                    i.schedule = t
                                    i.save()

                                s = start.replace(
                                    hour=0,
                                    minute=0,
                                    second=0)
                                e = start.replace(
                                    hour=time_end.hour,
                                    minute=time_end.minute,
                                    second=time_end.second)

                                if s <= arrow.get(i.connect_time) <= e:
                                    i.schedule = t
                                    i.save()

                    else:
                        for i in Incoming.objects.filter(
                                cdr=self, valid=True, company=c,
                                weekday=5,
                                schedule=None):
                            start = arrow.get(i.connect_time)

                            if time_start < time_end:
                                s = start.replace(
                                    hour=time_start.hour,
                                    minute=time_start.minute,
                                    second=time_start.second)
                                e = start.replace(
                                    hour=time_end.hour,
                                    minute=time_end.minute,
                                    second=time_end.second)

                                if s <= arrow.get(i.connect_time) <= e:
                                    i.schedule = t
                                    i.save()

                            else:
                                s = start.replace(
                                    hour=time_start.hour,
                                    minute=time_start.minute,
                                    second=time_start.second)
                                e = start.replace(
                                    hour=23,
                                    minute=59,
                                    second=59)

                                if s <= arrow.get(i.connect_time) <= e:
                                    i.schedule = t
                                    i.save()

                                s = start.replace(
                                    hour=0,
                                    minute=0,
                                    second=0)
                                e = start.replace(
                                    hour=time_end.hour,
                                    minute=time_end.minute,
                                    second=time_end.second)

                                if s <= arrow.get(i.connect_time) <= e:
                                    i.schedule = t
                                    i.save()

        Incoming.objects.filter(
            cdr=self, valid=True, schedule=None).update(
                set__valid=False, set__observation='Sin horario')

    def get_zone_range(self, ani):
        if re.search(patterns.pattern_num_6, ani):
            numeration = ani[2:][:6]

        else:
            numeration = ani[2:][:5]

        return numeration

    def get_company(self, ani):
        p = Portability.objects(number=ani).first()

        if p is not None:
            return p.company

        else:
            kwargs = self.get_zone_range(ani)
            n = Numeration.objects(**kwargs).first()

            if n is not None:
                return n.company

            else:
                return None

    def get_type_outgoing(self, ani, final_number):
        type_call = None

        if re.search(patterns.pattern_56446, ani):
            if re.search(patterns.movil, final_number):
                type_call = 'voip-movil'

            elif re.search(patterns.national, final_number):
                type_call = 'voip-local'

        elif re.search(patterns.national, ani):
            if re.search(patterns.movil, final_number):
                type_call = 'movil'

            elif (re.search(patterns.national, final_number)
                    and not re.search(patterns.pattern_56446, final_number)):
                type_call = 'local'

            elif not re.search(patterns.national, final_number):
                type_call = 'internacional'

        return type_call

    def get_horario(self, connect_time):
        """
        Metodo que determina el tipo de horario de una llamada
        :param connect_time: Fecha y hora de la llamada.
        :type connect_time: datetime.datetime
        """

        if 0 < connect_time.date().isoweekday() < 6:
            if dt.time(8, 0) <= connect_time.time() <= dt.time(19, 59, 59):
                return 'normal'

            elif dt.time(20, 0) <= connect_time.time() <= dt.time(23, 59, 59):
                return 'reducido'

            elif dt.time(0, 0) <= connect_time.time() <= dt.time(7, 59, 59):
                return 'nocturno'

        elif connect_time.date().isoweekday() == 6:
            if dt.time(8, 0) <= connect_time.time() <= dt.time(13, 59, 59):
                return 'normal'

            elif dt.time(14, 0) <= connect_time.time() <= dt.time(23, 59, 59):
                return 'reducido'

            elif dt.time(0, 0) <= connect_time.time() <= dt.time(7, 59, 59):
                return 'nocturno'

        else:
            if dt.time(8, 0) <= connect_time.time() <= dt.time(23, 59, 59):
                return 'reducido'

            elif dt.time(0, 0) <= connect_time.time() <= dt.time(23, 59, 59):
                return 'nocturno'

            else:
                return None

    def insert_outgoing(self):
        outgoing = self.outgoing.read()
        outgoing_file = StringIO.StringIO(outgoing)
        outgoing_dict = csv.DictReader(outgoing_file, delimiter=',')

        def reader_to_outgoing(reader):
            for r in reader:
                _type = self.get_type_outgoing(r['ANI'], r['FINAL_NUMBER'])
                company = self.get_company(r['FINAL_NUMBER'])
                connect_time = dt.datetime.strptime(
                    r['CONNECT_TIME'], '%Y-%m-%d %H:%M:%S')
                ingress_duration = int(r['INGRESS_DURATION'])
                line = Line.objects(number=r['ANI_NUMBER']).first()
                schedule = self.get_horario(connect_time)
                entity = self.get_entity(r['FINAL_NUMBER'])

                if company and _type and ingress_duration > 0:
                    valid = True

                else:
                    valid = False

                yield Outgoing(
                    connect_time=connect_time,
                    ani=r['ANI'],
                    ani_number=r['ANI_NUMBER'],
                    final_number=r['FINAL_NUMBER'],
                    dialed_number=r['DIALED_NUMBER'],
                    ingress_duration=ingress_duration,
                    cdr=self,
                    valid=valid,
                    company=company,
                    _type=_type,
                    line=line,
                    schedule=schedule,
                    entity=entity)

        Outgoing.objects.insert(
            reader_to_outgoing(outgoing_dict), load_bulk=False)

    def get_ingress_duration_by_type(cdr, company, _type, schedule):
        return Incoming.objects(
            cdr=cdr, company=company, _type=_type, schedule=schedule,
            entity='Empresa').sum('ingress_duration')

    def get_count_by_type(cdr, company, _type, schedule):
        return Incoming.objects(
            cdr=cdr, company=company, _type=_type, schedule=schedule,
            entity='Empresa').count()

    def get_outgoing_ingress_duration(cdr, company, _type, schedule):
        return Outgoing.objects(
            cdr=cdr, company=company, _type=_type, schedule=schedule,
            entity='Empresa').sum('ingress_duration')

    def get_outgoing_count(cdr, company, _type, schedule):
        return Outgoing.objects(
            cdr=cdr, company=company, _type=_type, schedule=schedule,
            entity='Empresa').count()

    def get_traffic(self, _type):
        items = []
        date = self.get_date()

        for c in Company.objects(invoicing='monthly'):
            for s in map(lambda x: x[0], choices.TIPO_CHOICES):
                ingress_duration = self.get_ingress_duration_by_type(
                    self, c, _type, s)
                count = self.get_count_by_type(self, c, _type, s)

                if ingress_duration > 0 and count > 0:
                    if _type == 'local':
                        items.append(
                            314, date, 'E', '06', '2', c.code, 'TB', 'CO',
                            'NOR', '0%s' % s, count, round(ingress_duration))

                    elif _type == 'voip-local':
                        items.append(
                            314, date, 'E', c.code, 'CO', 'NOR',
                            '0%s' % s, count, round(ingress_duration),
                            round(ingress_duration) * 20)

                    elif _type == 'movil':
                        items.append(
                            314, date, 'E', c.code, '06', '2', 'TB', 'CO',
                            'NOR', '0%s' % s, count, round(ingress_duration))

                    elif _type == 'voip-movil':
                        items.append(
                            314, date, 'E', c.code, 'CO', 'NOR',
                            '0%s' % s, count, round(ingress_duration),
                            round(ingress_duration) * 20)

                ingress_duration = self.get_outgoing_ingress_duration(
                    self, c, _type, s)
                count = self.get_outgoing_count(self, c, _type, s)

                if ingress_duration > 0 and count > 0:
                    if _type == 'local':
                        items.append(
                            314, date, 'S', '06', '2', c.code, 'TB', 'CO',
                            'NOR', '0%s' % s, count, round(ingress_duration))

                    elif _type == 'voip-local':
                        items.append(
                            314, date, 'S', c.code, 'CO', 'NOR',
                            '0%s' % s, count, round(ingress_duration),
                            round(ingress_duration) * 20)

                    elif _type == 'movil':
                        items.append(
                            314, date, 'S', c.code, '06', '2', 'TB', 'CO',
                            'NOR', '0%s' % s, count, round(ingress_duration))

                    elif _type == 'voip-movil':
                        items.append(
                            314, date, 'S', c.code, 'CO', 'NOR',
                            '0%s' % s, count, round(ingress_duration),
                            round(ingress_duration) * 20)

                    elif _type == 'internacional':
                        items.append(
                            314, date, 'LDI', 'S', 112, '06', 2, 'TB', 'CO',
                            'NOR', '0%s' % s, count, round(ingress_duration))

        return items


class Incoming(mongoengine.Document):

    """Modelo de las llamdas entrantes."""

    connect_time = mongoengine.DateTimeField()
    disconnect_time = mongoengine.DateTimeField()
    ani = mongoengine.StringField()
    final_number = mongoengine.StringField()
    ani_number = mongoengine.StringField()
    ingress_duration = mongoengine.IntField()
    dialed_number = mongoengine.StringField()
    cdr = mongoengine.ReferenceField(
        Cdr, reverse_delete_rule=mongoengine.CASCADE)
    valid = mongoengine.BooleanField()
    invoiced = mongoengine.BooleanField(default=False)
    observation = mongoengine.StringField()
    company = mongoengine.ReferenceField(Company)
    _type = mongoengine.StringField()
    schedule = mongoengine.StringField()
    entity = mongoengine.StringField()
    numeration = mongoengine.StringField()
    weekday = mongoengine.IntField()

    def __unicode__(self):
        return str(self.connect_time)


class Outgoing(mongoengine.Document):

    """Modelo de las llamdas salientes."""

    connect_time = mongoengine.DateTimeField()
    ani = mongoengine.StringField()
    final_number = mongoengine.StringField()
    ani_number = mongoengine.StringField()
    ingress_duration = mongoengine.IntField()
    dialed_number = mongoengine.StringField()
    cdr = mongoengine.ReferenceField(
        Cdr, reverse_delete_rule=mongoengine.CASCADE)
    valid = mongoengine.BooleanField()
    company = mongoengine.ReferenceField(Company)
    line = mongoengine.ReferenceField(Line)
    _type = mongoengine.StringField()
    schedule = mongoengine.StringField()
    entity = mongoengine.StringField()

    def __unicode__(self):
        return str(self.connect_time)


class Portability(mongoengine.Document):

    """Modelo de los numeros portados."""

    number = mongoengine.StringField()
    company = mongoengine.ReferenceField(Company)
    _type = mongoengine.IntField()
    date = mongoengine.DateTimeField()
    ido = mongoengine.IntField()

    def __unicode__(self):
        return str(self.number)

    @classmethod
    def upload(cls, filename):
        numbers = csv.DictReader(filename, delimiter=',')

        def reader_to_portability(reader):
            for r in reader:
                yield {
                    'date': dt.datetime.strptime(
                        r['fecha'], '%Y%m%d'),
                    'number': r['numero'],
                    'ido': int(r['ido']),
                    '_type': int(r['tipo'])}

        db = MongoClient(settings.MONGODB_URI).gesvoip
        db.portability.remove()
        db.portability.insert(reader_to_portability(numbers))

        for c in Company.objects.all():
            cls.objects.filter(ido__in=c.idoidd).update(set__company=c)


class Holiday(mongoengine.Document):

    """Modelo de los feriados."""

    date = mongoengine.DateTimeField(unique=True, verbose_name=u'fecha')
    reason = mongoengine.StringField(max_length=255, choices=choices.HOLIDAYS)

    meta = {
        'ordering': ['-date']
    }

    def __unicode__(self):
        return str(self.date)


class Invoice(mongoengine.Document):

    """Modelo de facturas."""

    company = mongoengine.ReferenceField(Company)
    cdr = mongoengine.ReferenceField(
        Cdr, reverse_delete_rule=mongoengine.CASCADE)
    call_number = mongoengine.IntField()
    call_duration = mongoengine.IntField()
    total = mongoengine.FloatField()
    invoiced = mongoengine.BooleanField(default=False)
    code = mongoengine.SequenceField()

    def __unicode__(self):
        return self.get_date()

    def get_date(self):
        return u'{0}-{1}'.format(self.cdr.year, self.cdr.month)

    def get_total(self):
        return int(round(self.total)) if self.total else 0

    def get_periods(self):
        return Period.objects(invoice=self)


class Period(mongoengine.Document):

    """Modelo que representa los periodos de las facturas"""

    invoice = mongoengine.ReferenceField(Invoice)
    start = mongoengine.DateTimeField()
    end = mongoengine.DateTimeField()
    call_number = mongoengine.IntField()
    call_duration = mongoengine.IntField()
    total = mongoengine.FloatField()

    def __unicode__(self):
        return self.get_range()

    def get_start(self):
        return self.start.strftime('%Y-%m-%d')

    def get_end(self):
        return self.end.strftime('%Y-%m-%d')

    def get_range(self):
        return u'{0} - {1}'.format(self.get_start(), self.get_end())

    def get_rates(self):
        return Rate.objects(period=self)

    def get_total(self):
        return int(round(self.total)) if self.total else 0


class Rate(mongoengine.Document):

    """Modelo que representa las tarifas de las compañias"""

    period = mongoengine.ReferenceField(Period)
    _type = mongoengine.StringField()
    price = mongoengine.FloatField()
    call_number = mongoengine.IntField()
    call_duration = mongoengine.IntField()
    total = mongoengine.FloatField()

    def __unicode__(self):
        return self._type

    def get_type(self):
        return self._type

    def get_total(self):
        return int(round(self.total)) if self.total else 0


class LocalCenter(mongoengine.Document):

    """Modelo que representa los centros locales"""

    company = mongoengine.ReferenceField(Company)
    code = mongoengine.IntField(unique=True, verbose_name=u'codigo local')
    name = mongoengine.StringField(
        max_length=255, verbose_name=u'descripción local')

    def __unicode__(self):
        return self.name


class Ccaa(mongoengine.Document):

    """Modelo que representa los cargos de acceso"""

    month = mongoengine.StringField(
        max_length=2, choices=choices.MONTHS, verbose_name=u'mes')
    year = mongoengine.StringField(
        max_length=4, choices=choices.YEARS, verbose_name=u'año')
    company = mongoengine.ReferenceField(
        Company, verbose_name=u'concecionaria interconectada')
    invoice = mongoengine.IntField(verbose_name=u'número factura')
    start = mongoengine.DateTimeField(verbose_name=u'fecha inicio')
    end = mongoengine.DateTimeField(verbose_name=u'fecha fin')
    invoice_date = mongoengine.DateTimeField(
        verbose_name=u'fecha emision factura')
    schedule = mongoengine.StringField(verbose_name=u'tipo horario')
    call_duration = mongoengine.IntField(verbose_name=u'trafico')
    total = mongoengine.IntField(verbose_name=u'monto')

    def __unicode__(self):
        return u'{0} {1}'.format(self.get_date(), self.company)

    def get_date(self):
        return u'{0}-{1}'.format(self.year, self.month)

    def get_schedule(self):
        if self.schedule == 'normal':
            return 'N'

        elif self.schedule == 'reducido':
            return 'R'

        else:
            return 'O'

    @classmethod
    def get_report(cls, year, month):
        date = year + month

        def report_cb(obj):
            return [
                314,
                date,
                obj.company.code,
                obj.invoice,
                obj.start.strftime('%Y%m%d'),
                obj.end.strftime('%Y%m%d'),
                'PCA',
                obj.invoice_date.strftime('%Y%m%d'),
                obj.get_schedule(),
                '',
                obj.call_duration,
                obj.total]

        return map(report_cb, cls.objects(year=year, month=month))
