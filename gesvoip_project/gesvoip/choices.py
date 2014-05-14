import datetime as dt


COMPANIAS = (
    ('ENTEL', 'ENTEL'),
    ('CTC', 'CTC'),
)

MONTHS = (
    ('01', 'Enero'),
    ('02', 'Febrero'),
    ('03', 'Marzo'),
    ('04', 'Abril'),
    ('05', 'Mayo'),
    ('06', 'Junio'),
    ('07', 'Julio'),
    ('08', 'Agosto'),
    ('09', 'Septiembre'),
    ('10', 'Octubre'),
    ('11', 'Noviembre'),
    ('12', 'Diciembre'),
)

YEARS = tuple(
    ('{0}'.format(i), '{0}'.format(i))
    for i in range(dt.date.today().year, 2000, -1)
)

HORARIOS = (
    ('normal', 'normal'),
    ('reducido', 'reducido'),
    ('nocturno', 'nocturno'),
)

DIAS = (
    ('habil', 'habil'),
    ('sabado', 'sabado'),
    ('festivo', 'festivo'),
)

ESTADOS = (
    ('desactivado', 'desactivado'),
    ('activado', 'activado'),
    ('facturado', 'facturado'),
)

ROLES = (
    ('Operador', 'Operador'),
    ('Administrador', 'Administrador'),
)
