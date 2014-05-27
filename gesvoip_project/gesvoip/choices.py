# -*- coding: utf-8 -*-

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
YEARS = [
    ('{0}'.format(i), '{0}'.format(i))
    for i in range(dt.date.today().year, 2000, -1)
]

CITIES = (
    (13101, 'Santiago'),
    (13102, 'Cerrillos'),
    (13103, 'Cerro Navia'),
    (13104, 'Conchali'),
    (13105, 'El Bosque'),
    (13106, 'Estacion Central'),
    (13107, 'Huechuraba'),
    (13108, 'Independencia'),
    (13109, 'La Cisterna'),
    (13110, 'La Florida'),
    (13111, 'La Granja'),
    (13112, 'La Pintana'),
    (13113, 'La Reina'),
    (13114, 'Las Condes'),
    (13115, 'Lo Barnechea'),
    (13116, 'Lo Espejo'),
    (13117, 'Lo Prado'),
    (13118, 'Macul'),
    (13119, 'Maipu'),
    (13120, 'Ñuñoa'),
    (13121, 'Pedro Aguirre Cerda'),
    (13122, 'Peñalolen'),
    (13123, 'Providencia'),
    (13124, 'Pudahuel'),
    (13125, 'Quilicura'),
    (13126, 'Quinta Normal'),
    (13127, 'Recoleta'),
    (13128, 'Renca'),
    (13129, 'San Joaquin'),
    (13130, 'San Miguel'),
    (13131, 'San Ramon'),
    (13132, 'Vitacura'),
    (13201, 'Puente Alto'),
    (13202, 'Pirque'),
    (13203, 'San Jose de Maipo'),
    (13301, 'Colina'),
    (13302, 'Lampa'),
    (13303, 'Til Til'),
    (13401, 'San Bernardo'),
    (13402, 'Buin'),
    (13403, 'Calera de Tango'),
    (13404, 'Paine'),
    (13501, 'Melipilla'),
    (13502, 'Alhue'),
    (13503, 'Curacavi'),
    (13504, 'Maria Pinto'),
    (13505, 'San Pedro'),
    (13601, 'Talagante'),
    (13602, 'El Monte'),
    (13603, 'Isla de Maipo'),
    (13604, 'Padre Hurtado'),
    (13605, 'Peñaflor'),
    (1101, 'Iquique'),
    (1102, 'Camiña'),
    (1103, 'Colchane'),
    (1104, 'Huara'),
    (1105, 'Pica'),
    (1106, 'Pozo Almonte'),
    (1107, 'Alto Hospicio'),
    (1201, 'Arica'),
    (1202, 'Camarones'),
    (1301, 'Putre'),
    (1302, 'General Lagos'),
    (1401, 'Pozo Almonte'),
    (1402, 'Camiña'),
    (1403, 'Colchane'),
    (1404, 'Huara'),
    (1405, 'Pica'),
    (2101, 'Antofagasta'),
    (2102, 'Mejillones'),
    (2103, 'Sierra Gorda'),
    (2104, 'Taltal'),
    (2201, 'Calama'),
    (2202, 'Ollagüe'),
    (2203, 'San Pedro de Ata</optio'),
    (2301, 'Tocopilla'),
    (2302, 'Maria Elena'),
    (3101, 'Copiapo'),
    (3102, 'Caldera'),
    (3103, 'Tierra Amarilla'),
    (3201, 'Chañaral'),
    (3202, 'Diego de Almagro'),
    (3301, 'Vallenar'),
    (3302, 'Alto Del Carmen'),
    (3303, 'Freirina'),
    (3304, 'Huasco'),
    (4101, 'La Serena'),
    (4102, 'Coquimbo'),
    (4103, 'Andacollo'),
    (4104, 'La Higuera'),
    (4105, 'Paihuano'),
    (4106, 'Vicuña'),
    (4201, 'Illapel'),
    (4202, 'Canela'),
    (4203, 'Los Vilos'),
    (4204, 'Salamanca'),
    (4301, 'Ovalle'),
    (4302, 'Combarbala'),
    (4303, 'Monte Patria'),
    (4304, 'Punitaqui'),
    (4305, 'Rio Hurtado'),
    (5101, 'Valparaiso'),
    (5102, 'Casablanca'),
    (5103, 'oncon'),
    (5104, 'Juan Fernandez'),
    (5105, 'uchuncavi'),
    (5106, 'Quilpue'),
    (5107, 'Quintero'),
    (5108, 'Villa Alemana'),
    (5109, 'iña del Mar'),
    (5201, 'Isla de Pascua'),
    (5301, 'Los Andes'),
    (5302, 'Calle Larga'),
    (5303, 'inconada'),
    (5304, 'San Esteban'),
    (5401, 'La Ligua'),
    (5402, 'abildo'),
    (5403, 'Papudo'),
    (5404, 'Petorca'),
    (5405, 'apallar'),
    (5501, 'Quillota'),
    (5502, 'Calera'),
    (5503, 'Hijuelas'),
    (5504, 'La Cruz'),
    (5505, 'imache'),
    (5506, 'Nogales'),
    (5507, 'Olmue'),
    (5601, 'San Antonio'),
    (5602, 'Algarrobo'),
    (5603, 'Cartagena'),
    (5604, 'El Quisco'),
    (5605, 'El Tabo'),
    (5606, 'Santo Domingo'),
    (5701, 'San Felipe'),
    (5702, 'Catemu'),
    (5703, 'Llaillay'),
    (5704, 'Panquehue'),
    (5705, 'Putaendo'),
    (5706, 'anta Maria'),
    (5801, 'Quilpue'),
    (5802, 'Limache'),
    (5803, 'Olmue'),
    (5804, 'Villa Alemana'),
    (6101, 'Rancagua'),
    (6102, 'Codegua'),
    (6103, 'Coinco'),
    (6104, 'Coltauco'),
    (6105, 'Doñihue'),
    (6106, 'Graneros'),
    (6107, 'Las Cabras'),
    (6108, 'Machali'),
    (6109, 'alloa'),
    (6110, 'Mostazal'),
    (6111, 'Olivar'),
    (6112, 'Peumo'),
    (6113, 'Pichidegua'),
    (6114, 'Quinta de Tilcoco'),
    (6115, 'Rengo'),
    (6116, 'Requinoa'),
    (6117, 'San Vicente'),
    (6201, 'Pichilemu'),
    (6202, 'La Estrella'),
    (6203, 'Litueche'),
    (6204, 'Marchihue'),
    (6205, 'Navidad'),
    (6206, 'Paredones'),
    (6301, 'San Fernando'),
    (6302, 'Chepica'),
    (6303, 'Chimbarongo'),
    (6304, 'Lolol'),
    (6305, 'Nancagua'),
    (6306, 'Palmilla'),
    (6307, 'Peralillo'),
    (6308, 'Placilla'),
    (6309, 'Pumanque'),
    (6310, 'Santa Cruz'),
    (7101, 'Talca'),
    (7102, 'Constitucion'),
    (7103, 'Curepto'),
    (7104, 'Empedrado'),
    (7105, 'Maule'),
    (7106, 'Pelarco'),
    (7107, 'Pencahue'),
    (7108, 'Rio Claro'),
    (7109, 'San Clemente'),
    (7110, 'San Rafael'),
    (7201, 'Cauquenes'),
    (7202, 'Chanco'),
    (7203, 'Pelluhue'),
    (7301, 'Curico'),
    (7302, 'Hualañe'),
    (7303, 'Licanten'),
    (7304, 'Molina'),
    (7305, 'Rauco'),
    (7306, 'Romeral'),
    (7307, 'Sagrada Familia'),
    (7308, 'Teno'),
    (7309, 'Vichuquen'),
    (7401, 'Linares'),
    (7402, 'Colbun'),
    (7403, 'Longavi'),
    (7404, 'Parral'),
    (7405, 'Retiro'),
    (7406, 'San Javier'),
    (7407, 'Villa Alegre'),
    (7408, 'Yerbas Buenas'),
    (8101, 'Concepcion'),
    (8102, 'Coronel'),
    (8103, 'Chiguayante'),
    (8104, 'Florida'),
    (8105, 'Hualqui'),
    (8106, 'Lota'),
    (8107, 'Penco'),
    (8108, 'San Pedro de la Paz'),
    (8109, 'Juana'),
    (8110, 'Talcahuano'),
    (8111, 'Tome'),
    (8112, 'Hualpen'),
    (8201, 'Lebu'),
    (8202, 'Arauco'),
    (8203, 'Cañete'),
    (8204, 'Contulmo'),
    (8205, 'Curanilahue'),
    (8206, 'Los Alamos'),
    (8207, 'Tirua'),
    (8301, 'Los Angeles'),
    (8302, 'Antuco'),
    (8303, 'Cabrero'),
    (8304, 'Laja'),
    (8305, 'Mulchen'),
    (8306, 'Nacimiento'),
    (8307, 'Negrete'),
    (8308, 'Quilaco'),
    (8309, 'Quilleco'),
    (8310, 'San Rosendo'),
    (8311, 'Santa Barbara'),
    (8312, 'Tucapel'),
    (8313, 'Yumbel'),
    (8314, 'Alto Biobio'),
    (8401, 'Chillan'),
    (8402, 'Bulnes'),
    (8403, 'Cobquecura'),
    (8404, 'Coelemu'),
    (8405, 'Coihueco'),
    (8406, 'Chillan Viejo'),
    (8407, 'El Carmen'),
    (8408, 'Ninhue'),
    (8409, 'Ñiquen'),
    (8410, 'Pemuco'),
    (8411, 'Pinto'),
    (8412, 'Portezuelo'),
    (8413, 'Quillon'),
    (8414, 'Quirihue'),
    (8415, 'Ranquil'),
    (8416, 'San Carlos'),
    (8417, 'San Fabian'),
    (8418, 'San Ignacio'),
    (8419, 'San Nicolas'),
    (8420, 'Treguaco'),
    (8421, 'Yungay'),
    (9101, 'Temuco'),
    (9102, 'Carahue'),
    (9103, 'Cunco'),
    (9104, 'Curarrehue'),
    (9105, 'Freire'),
    (9106, 'Galvarino'),
    (9107, 'Gorbea'),
    (9108, 'Lautaro'),
    (9109, 'Loncoche'),
    (9110, 'Melipeuco'),
    (9111, 'Nueva Imperial'),
    (9112, 'Padre Las Casas'),
    (9113, 'Perquenco'),
    (9114, 'Pitrufquen'),
    (9115, 'Pucon'),
    (9116, 'Saavedra'),
    (9117, 'Teodoro Schmidt'),
    (9118, 'Tolten'),
    (9119, 'Vilcun'),
    (9120, 'Villarrica'),
    (9121, 'Cholchol'),
    (9201, 'Angol'),
    (9202, 'Collipulli'),
    (9203, 'Curacautin'),
    (9204, 'Ercilla'),
    (9205, 'Lonquimay'),
    (9206, 'Los Sauces'),
    (9207, 'Lumaco'),
    (9208, 'Puren'),
    (9209, 'Renaico'),
    (9210, 'Traiguen'),
    (9211, 'Victoria'),
    (10101, 'Puerto Montt'),
    (10102, 'Calbuco'),
    (10103, 'Cochamo'),
    (10104, 'Fresia'),
    (10105, 'Frutillar'),
    (10106, 'Los Muermos'),
    (10107, 'Llanquihue'),
    (10108, 'Maullin'),
    (10109, 'Puerto Varas'),
    (10201, 'Castro'),
    (10202, 'Ancud'),
    (10203, 'Chonchi'),
    (10204, 'Curaco de Velez'),
    (10205, 'Dalcahue'),
    (10206, 'Puqueldon'),
    (10207, 'Queilen'),
    (10208, 'Quellon'),
    (10209, 'Quemchi'),
    (10210, 'Quinchao'),
    (10301, 'Osorno'),
    (10302, 'Puerto Octay'),
    (10303, 'Purranque'),
    (10304, 'Puyehue'),
    (10305, 'Rio Negro'),
    (10306, 'San Juan de la Costa'),
    (10307, 'San Pablo'),
    (10401, 'Chaiten'),
    (10402, 'Futaleufu'),
    (10403, 'Hualaihue'),
    (10404, 'Palena'),
    (10501, 'Valdivia'),
    (10502, 'Corral'),
    (10503, 'Futrono'),
    (10504, 'La Union'),
    (10505, 'Lago Ranco'),
    (10506, 'Lanco'),
    (10507, 'Los Lagos'),
    (10508, 'Mafil'),
    (10509, 'San Jose de la Mariquina'),
    (10510, 'Paillaco'),
    (10511, 'Panguipulli'),
    (10512, 'Rio Bueno'),
    (11101, 'Coyhaique'),
    (11102, 'Lago Verde'),
    (11201, 'Aisen'),
    (11202, 'Puerto Cisnes'),
    (11203, 'Guaitecas'),
    (11301, 'Cochrane'),
    (11302, 'O\'Higgins'),
    (11303, 'Tortel'),
    (11401, 'Chile Chico'),
    (11402, 'Rio Ibañez'),
    (12101, 'Punta Arenas'),
    (12102, 'Laguna Blanca'),
    (12103, 'Rio Verde'),
    (12104, 'San Gregorio'),
    (12201, 'CABO DE HORNOS'),
    (12202, 'Antartica'),
    (12301, 'Porvenir'),
    (12302, 'Primavera'),
    (12303, 'Timaukel'),
    (12401, 'Natales'),
    (12402, 'Torres del Paine'),
    (14101, 'Valdivia'),
    (14102, 'Corral'),
    (14103, 'Lanco'),
    (14104, 'Los Lagos'),
    (14105, 'Mafil'),
    (14106, 'San Jose de la Mariquina'),
    (14107, 'Paillaco'),
    (14108, 'Panguipulli'),
    (14201, 'La Union'),
    (14202, 'Futrono'),
    (14203, 'Lago Ranco'),
    (14204, 'Rio Bueno'),
    (15101, 'Arica'),
    (15102, 'Camarones'),
    (15201, 'Putre'),
    (15202, 'General Lagos'),
)

ZONES = (
    (2, 'Santiago'),
    (58, 'Arica'),
    (57, 'Iquique'),
    (55, 'Antofagasta'),
    (52, 'Copiapo'),
    (51, 'La Serena'),
    (53, 'Ovalle'),
    (33, 'Quillota'),
    (32, 'Valparaiso'),
    (34, 'Los Andes'),
    (35, 'San Antonio'),
    (72, 'Rancagua'),
    (75, 'Curico'),
    (71, 'Talca'),
    (73, 'Linares'),
    (42, 'Chillan'),
    (41, 'Concepcion'),
    (43, 'Los angeles'),
    (45, 'Temuco'),
    (63, 'Valdivia'),
    (64, 'Osorno'),
    (65, 'Puerto Montt'),
    (67, 'Coyhaique'),
    (61, 'Punta Arenas'),
)

NATURAL = 'natural'
COMPANY = 'empresa'
ENTITIES = (
    (NATURAL, 'Natural'),
    (COMPANY, 'Empresa'),
)

TIPOS = (
    ('voip-movil', 'voip-movil'),
    ('voip-ldi', 'voip-ldi'),
    ('voip-local', 'voip-local'),
    ('movil', 'movil'),
    ('internacional', 'internacional'),
    ('local', 'local'),
    ('especial', 'especial'),
    ('nacional', 'nacional'),
)

NORMAL = 'normal'
REDUCIDO = 'reducido'
NOCTURNO = 'nocturno'
TIPO_CHOICES = (
    (NORMAL, 'Normal'),
    (REDUCIDO, 'Reducido'),
    (NOCTURNO, 'Nocturno')
)

INVOICING = (
    ('monthly', 'Mensual'),
    ('biannual', 'Semestral'),
    ('quarterly', 'Trimestral'),
    ('annual', 'Anual'),
)

SERVICES = (
    ('movil', 'Movil'),
    ('fijo', 'Fijo'),
    ('voip', 'Voip'),
    ('rural', 'Rural'),
    ('mppc', 'MPPC'),
)

MODES = (
    ('prepago', 'Prepago'),
    ('postpago', 'Postpago'),
)

SPECIAL_SERVICES = (
    ('isdn', 'ISDN'),
    ('pabx', 'PABX'),
)
