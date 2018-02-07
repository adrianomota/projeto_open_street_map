import csv
import xml.etree.cElementTree as ET
from lxml import etree
import pprint
import re
import codecs
from io import StringIO
import string

OSM_PATH = "dataset/barueri_e_cidades_vizinhas.osm"
NODES_PATH = "dataset/csv/nodes.csv"
NODE_TAGS_PATH = "dataset/csv/nodes_tags.csv"
WAYS_PATH = "dataset/csv/ways.csv"
WAY_NODES_PATH = "dataset/csv/ways_nodes.csv"
WAY_TAGS_PATH = "dataset/csv/ways_tags.csv"

LOWER_COLON = re.compile(r'((\w|_)+):((\w|_)+:?.*)')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

field_nodes = { 'id':'',
                'lat':'',
                'lon':'',
                'user':'',
                'uid':'',
                'version':'',
                'changeset':'',
                'timestamp':''}


field_nodes_tags = { 'id':'',
                     'key':'',
                     'value':'',
                     'type':'' }

field_ways = { 'id':'',
               'user':'',
               'uid':'',
               'version':'',
               'changeset':'',
               'timestamp':'' }

field_ways_tags = { 'id':'',
                    'key':'',
                    'value':'',
                    'type':'', }

field_way_node = { 'id':'',
                   'node_id':'',
                   'position':'' }

def update_fields():
    for key, value in field.items():
        field[key] = ''

def audit_if_value_is_numeric(value):
    if not value.isnumeric():
        return value
    
def create_header_csv(csv, fields):
    fields_table = []
    for key, value in fields.items():
        fields_table.append(key)
    csv.writerow(fields_table)
  
def create_row_csv(csv, f):
    lines = []
    for key, value in f.items():
        lines.append(value)
    csv.writerow(lines)

def get_element(osm_file, tags=('node', 'way', 'relation')):
    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()

def create_csv_node_table(file):
    with open (file,'w', newline='',encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        create_header_csv(csv_writer,field_nodes)
     
        for elm in get_element(OSM_PATH, tags=('node')):
            if elm.tag == 'node':
                for node in elm.iter('node'):
                    field_nodes['id'] =node.attrib['id']
                    field_nodes['lat'] = node.attrib['lat']  
                    field_nodes['lon'] = node.attrib['lon']  
                    field_nodes['user'] = audit_if_value_is_numeric(node.attrib['user'].capitalize())  
                    field_nodes['uid'] = node.attrib['uid']
                    field_nodes['version'] = node.attrib['version']  
                    field_nodes['changeset'] = node.attrib['changeset']
                    field_nodes['timestamp'] = node.attrib['timestamp']
                    create_row_csv(csv_writer,field_nodes)
     

def create_csv_node_tags_table(file):
    with open (file,'w', newline='',encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        for elm in get_element(OSM_PATH, tags=('node')):
                if elm.tag == 'node':
                    for node in elm.iter('node'):
                        for tag in elm.iter('tag'):
                            field_nodes_tags['id'] = node.attrib['id']
                            field_nodes_tags['key'] = audit_node_tags_k(tag.attrib['k'])
                            field_nodes_tags['value'] = audit_node_tags_value(tag.attrib['v'])
                            field_nodes_tags['type'] = ''
                            create_row_csv(csv_writer,field_nodes_tags)

def create_csv_ways_table(file):
    with open (file,'w', newline='',encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        create_header_csv(csv_writer,field_ways)
        for elm in get_element(OSM_PATH, tags=('way')):
            if elm.tag == 'way':
                for way in elm.iter('way'):
                    field_ways['id'] = way.attrib['id']
                    field_ways['user'] = way.attrib['user'].capitalize()
                    field_ways['uid'] = way.attrib['uid']
                    field_ways['version'] = way.attrib['version']
                    field_ways['changeset'] = way.attrib['changeset']
                    field_ways['timestamp'] = way.attrib['timestamp']
                    create_row_csv(csv_writer,field_ways)

def create_csv_ways_tags_table(file):
    with open (file,'w', newline='',encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        create_header_csv(csv_writer,field_ways_tags)
        for elm in get_element(OSM_PATH, tags=('way')):
            if elm.tag == 'way':
                for way in elm.iter('way'):
                    for tag in elm.iter('tag'):
                        field_ways_tags['id'] = way.attrib['id']
                        field_ways_tags['key'] = audit_ways_tags_k(tag.attrib['k'])
                        field_ways_tags['value'] = audit_ways_tags_value(tag.attrib['v'])
                        field_ways_tags['type'] = ''
                        create_row_csv(csv_writer,field_ways_tags)

def create_csv_ways_node_table(file):
    with open (file,'w', newline='',encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        create_header_csv(csv_writer,field_way_node)
        for elm in get_element(OSM_PATH, tags=('way')):
            if elm.tag == 'way':
                for way in elm.iter('way'):
                     for nd in elm.iter('nd'):
                        field_way_node['id'] = way.attrib['id']
                        field_way_node['node_id'] = nd.attrib['ref']
                        field_way_node['position'] = ''
                        create_row_csv(csv_writer,field_way_node)

#helper functions
def is_motorway_junction(value):
  return value.find("motorway_junction") > -1
        
def is_pt(value):
    return value.find("pt:") > -1

def is_milestone(value):
    return value.find("milestone") > -1

def is_traffic_signals(value):
    return value.find("traffic_signals") > -1

def is_highway(value):
    return value.find("highway") > -1

def is_railway(value):
    return value.find("railway") > -1

def is_stop(value):
    return value.find("stop") > -1

def is_switch(value):
    return value.find("switch") > -1

def is_train(value):
    return value.find("train") > -1

def is_fast_food(value):
    return value.find("fast_food") > -1

def is_public_transport(value):
    return value.find("public_transport") > -1

def is_cuisine(value):
    return value.find("cuisine") > -1

def is_distance_word(value):
    return value.find("distance") > -1

def is_barrier(value):
    return value.find("barrier") > -1

def is_toll_booth(value):
    return value.find("toll_booth") > -1

def is_operator(value):
    return value.find("operator") > -1

def is_population(value):
    return value.find("population") > -1

def is_place(value):
    return value.find("place") > -1

def is_city(value):
    return value.find("city") > -1

def is_description(value):
    return value.find("description") > -1

def is_name(value):
    return value.find("name") > -1

def is_wheelchair(value):
    return value.find("wheelchair") > -1

def is_yes(value):
    return value.find("yes") > -1    

def is_toilets_wheelchair(value):
    return value.find("toilets:wheelchair") > -1

def is_crossing_barrier(value):
    return value.find("crossing:barrier") > -1

def is_crossing_bell(value):
    return value.find("crossing:bell") > -1

def is_crossing_chicane(value):
    return value.find("crossing:chicane") > -1

def is_crossing_light(value):
    return value.find("crossing:light") > -1

def is_crossing_saltire(value):
    return value.find("crossing:saltire") > -1

def is_crossing_supervision(value):
    return value.find("crossing:supervision") > -1    

def is_noexit(value):
    return value.find("noexit") > -1

def is_turning_circle(value):
    return value.find("turning_circle") > -1

def is_mini_roundabout(value):
    return value.find("mini_roundabout") > -1

def is_signal(value):
    return value.find("signal") > -1

def is_crossing(value):
    return value.find("crossing") > -1

def is_stop_position(value):
    return value.find("stop_position") > -1

def is_shelter(value):
    return value.find("shelter") > -1

def is_parking(value):
    return value.find("parking") > -1

def is_sports_centre(value):
    return value.find("sports_centre") > -1

def is_bus_stop(value):
    return value.find("bus_stop") > -1

def is_charge(value):
    return value.find("charge") > -1

def is_restaurant(value):
    return value.find("restaurant") > -1

def is_fuel(value):
    return value.find("fuel") > -1

def is_supermarket(value):
    return value.find("supermarket") > -1

def is_tourism(value):
    return value.find("tourism") > -1

def is_bicycle(value):
    return value.find("bicycle") > -1    

def is_helipad(value):
    return value.find("helipad") > -1

def is_power(value):
    return value.find("power") > -1

def is_tower(value):
    return value.find("tower") > -1

def is_bus(value):
    return value.find("bus") > -1

def is_bakery(value):
    return value.find("bakery") > -1

def is_traffic_calming(value):
    return value.find("traffic_calming") > -1

def is_bump(value):
    return value.find("bump") > -1    

def is_communication(value):
    return value.find("communication") > -1    

def is_waterway(value):
    return value.find("waterway") > -1

def is_lock_gate(value):
    return value.find("lock_gate") > -1

def is_residential(value):
    return value.find("residential") > -1

def is_lane(value):
    return value.find("lanes") > -1

def is_maxspeed(value):
    return value.find("maxspeed") > -1

def is_oneway(value):
    return value.find("oneway") > -1

def is_surface(value):
    return value.find("surface") > -1

def is_paved(value):
    return value.find("paved") > -1    

def is_asphalt(value):
    return value.find("asphalt") > -1

def is_toll(value):
    return value.find("toll") > -1

def is_layer(value):
    return value.find("layer") > -1

def is_sidewalk(value):
    return value.find("sidewalk") > -1

def is_destination(value):
    return value.find("destination") > -1

def is_service(value):
    return value.find("service") > -1

def is_parking_aisle(value):
    return value.find("parking_aisle")

def is_trunk_link(value):
    return value.find("trunk_link") > -1

def is_tertiary(value):
    return value.find("tertiary") > -1

def is_trunk(value):
    return value.find("trunk") > -1

def is_leisure(value):
    return value.find("leisure") > -1

def  is_park(value):
    return value.find("park") > -1

def is_secondary(value):
    return value.find("secondary") > -1

def is_designated(value):
    return value.find("designated") > -1

def is_cycleway_left(value):
    return value.find("cycleway:left") > -1

def is_cycleway_right(value):
    return value.find("cycleway:right") > -1

def is_bridge(value):
    return value.find("bridge") > -1

def is_viaduct(value):
    return value.find("viaduct") > -1

def is_no(value):
    return value.find("no") > -1

def is_abandoned(value):
    return value.find("abandoned") > -1

def is_unclassified(value):
    return value.find("unclassified") > -1

def is_horse(value):
    return value.find("horse") > -1

def is_landuse(value):
    return value.find("landuse") > -1

def is_cemetery(value):
    return value.find("cemetery") > -1

def is_motorway(value):
    return value.find("motorway") > -1

def is_foot(value):
    return value.find("foot") > -1

def is_rank(value):
    return value.find("rank") > -1

def is_source(value):
    return value.find("source") > -1

def is_brand(value):
    return value.find("brand") > -1

def is_exit(value):
    return value.find("exit") > -1

def is_shop(value):
    return value.find("shop") > -1

def is_note(value):
    return value.find("note") > -1

def is_addr_city(value):
    return value.find("addr:city") > -1

def is_addr_country(value):
    return value.find("addr:country") > -1

def is_addr_housenumber(value):
    return value.find("addr:housenumber") > -1

def is_addr_postcode(value):
    return value.find("addr:postcode") > -1

def is_addr_state(value):
    return value.find("addr:state") > -1

def is_addr_street(value):
    return value.find("addr:street") > -1

def is_bank(value):
    return value.find("bank") > -1

def is_atm(value):
    return value.find("atm") > -1

def is_pharmacy(value):
    return value.find("pharmacy") > -1

def is_place_of_worship(value):
    return value.find("place_of_worship") > -1

def is_school(value):
    return value.find("school") > -1

def is_pub(value):
    return value.find("Pub") > -1    

def is_christian(value):
    return value.find("christian") > -1

def is_pizza(value):
    return value.find("pizza") > -1

def is_regional(value):
    return value.find("regional") > -1

def is_steak_house(value):
    return value.find("steak_house") > -1

def is_burger(value):
    return value.find("burger") > -1

def is_varios1(value):
    return value.find("burger;oriental;international;grill;sausage;pasta;noodles;pancake;pizza;chicken;italian_pizza") > -1

def is_varios2(value):
    return value.find("grill;sausage;portuguese;local;steak_house;pasta;chicken;kebab;barbecue") > -1

def is_varios_3(value):
    return value.find("oriental;noodles;pasta;international;pizza;arab;sausage") > -1

def is_varios_4(value):
    return value.find("pizza;diner;cake") > -1

def is_italian_pizza(value):
    return value.find("italian_pizza") > -1


def audit_node_tags_k(value):
    
    if is_residential(value):
        return "Residencial"
    if is_highway(value):
        return "Auto estrada"
    if is_stop(value):
        return "Parada"
    if is_train(value):
        return "Trem"
    if is_public_transport(value):
        return "Transporte Público"
    if is_cuisine(value):
        return "Cozinha"
    if is_distance_word(value):
        return "Distância"
    if is_barrier(value):
        return "Barreira"
    if is_operator(value):
        return "Concessionária"
    if is_place(value):
        return "Lugar"
    if is_description(value):
        return "Descrição"
    if is_name(value):
        return "Nome"
    if is_highway(value):
        return "Rodovia"
    if is_wheelchair(value):
        return "Cadeira de rodas"
    if is_yes(value):
        return "Sim"
    if is_toilets_wheelchair(value):
        return "Sanitário para cadeirantes"
    if is_crossing_barrier(value):
        return "Cruzamento com barreiras"
    if is_crossing_bell(value):
        return "Cruzamento com sinal sonoro"
    if is_crossing_chicane(value):
        return "Cruzamento com chicane"
    if is_crossing_light(value):
        return "Cruzamento iluminado"
    if is_crossing_saltire(value):
        return "Cruzamento em diagonal"
    if is_crossing_supervision(value):
        return "Cruzamento supervisionado"
    if is_noexit(value):
        return "Sem saída"
    if is_turning_circle(value):
        return "Rotatória"
    if is_population(value):
        return "População"
    if is_charge(value):
        return "Carregar"
    if is_bicycle(value):
        return "Bicicleta"
    if is_railway(value):
        return "Estrada de ferro"
    if is_power(value):
        return "Energia"
    if is_bus(value):
        return "Ônibus"
    if is_waterway(value):
        return "Via fluvial"
    if is_crossing(value):
        return "Cruzamento"
    if is_traffic_signals(value):
        return "Sinal de Trânsito"
    if is_rank(value):
        return "Classificação"
    if is_source(value):
        return "Fonte"
    if is_brand(value):
        return "Marca"
    if is_shop(value):
        return "Fazer compras"
    if is_bump(value):
        return "Colisão"
    if is_note(value):
        return "Observação"
    if is_pt(value):
        return "Ponte "
    if is_addr_city(value):
        return "Cidade"
    if is_addr_country(value):
        return "País"
    if is_addr_housenumber(value):
        return "Número"
    if is_addr_postcode(value):
        return "CEP"
    if is_addr_state(value):
        return "UF"
    if is_addr_street(value):
        return "Bairro"
    if is_bank(value):
        return "Banco"
    if is_atm(value):
        return "Caixa eletrônico"
    return value

def audit_node_tags_value(value):
    
    if is_residential(value):
        return "Residencial"
    if is_pt(value):
      return "Ponte em "
    if is_motorway_junction(value):
        return "Junção de auto-estrada"
    if is_milestone(value):
        return "Marco Histórico"
    if is_traffic_signals(value):
        return "Sinal de Trânsito"
    if is_switch(value):
        return "Interrupção de linha férrea"
    if is_fast_food(value):
        return "Restaurante de Fast Food"
    if is_toll_booth(value):
        return "Pedágio"
    if is_city(value):
        return "Cidade"
    if is_stop(value):
        return "Parada"
    if is_yes(value):
        return "Sim"
    if is_mini_roundabout(value):
        return "Mini rotatória"
    if is_signal(value):
        return "Sinal"
    if is_crossing(value):
        return "Cruzamento"
    if is_stop_position(value):
        return "Embarque"
    if is_shelter(value):
        return "Abrigo"
    if is_parking(value):
        return "Estacionamento"
    if is_sports_centre(value):
        return "Centro Desportivo"
    if is_bus_stop(value):
        return "Ponto de Ônibus"
    if is_restaurant(value):
        return "Restaurante"
    if is_fuel(value):
        return "Posto de gasolina"
    if is_supermarket(value):
        return "Supermercado"
    if is_tourism(value):
        return "Turismo"
    if is_helipad(value):
        return "Heliponto"
    if is_tower(value):
        return "Torre"
    if is_bakery(value):
        return "Padaria"
    if is_bump(value):
        return "Colisão"
    if is_turning_circle(value):
        return "Rotatória"
    if is_communication(value):
        return "Comunicação"
    if is_lock_gate(value):
        return "Portão de bloqueio"
    if is_source(value):
        return "Origem"
    if is_exit(value):
        return "Saída"
    if is_shelter(value):
        return "Abrigo"
    if is_bank(value):
        return "Banco"
    if is_pharmacy(value):
        return "Farmácia"
    if is_school(value):
        return "Escola"
    if is_place_of_worship(value):
        return "Religião"
    if is_atm(value):
        return "Caixa eletrônico"
    if is_christian(value):
        return "Cristianismo"
    if is_pizza(value):
        return "Pizza"
    if is_regional(value):
        return "Comidas regionais"
    if is_steak_house(value):
        return "Rede de grelhados"
    if is_burger(value):
        return "Amburgueria"
    if is_varios1(value):
        return "Amburguer, Comida Internacional, Panquecas, Macarrão, Massas, Linguiças, Comida Japonesa, Pizza, Frango e Grelhados em geral."
    if is_varios2(value):
        return "Comida Japonesa, Linguiça, Comida Árabe, Pizza, Grelhados em geral, Frango e churrasco"
    if is_varios_3(value):
        return "Pizza italiana"
    if is_varios_4(value):
        return "Comida japonesa, Comida Árabe e Grelhados em geral"
    if is_italian_pizza(value):
        return "Pizza Italiana tradicional"
    return value

def audit_ways_tags_k(value):
    
    if is_name(value):
       return "Nome"
    if is_highway(value):
       return "Rodovia"
    if is_lane(value):
       return "Pistas"
    if is_maxspeed(value):
       return "Velocidade Máxima"
    if is_oneway(value):
       return "Sentido único"
    if is_surface(value):
       return "Superfície"
    if is_paved(value):
       return "Pavimentado"
    if is_toll(value):
       return "Pedágio"        
    if is_layer(value):
       return "Camadas"
    if is_sidewalk(value):
       return "Calçada" 
    if is_destination(value):
       return "Destino"
    if is_leisure(value):
        return "Lazer"
    if is_bicycle(value):
        return "Bicicleta"
    if is_cycleway_left(value):
        return "Ciclo a esuqerda"
    if is_cycleway_right(value):
        return "Ciclo a direitis_cycleway_direitaa"
    if is_foot(value):
        return "Possui passagem de pedestres"
    if is_bridge(value):
        return "Ponte"
    if is_railway(value):
        return "Estrada de ferro"
    if is_horse(value):
        return "Cavalo"
    if is_landuse(value):
        return "Uso da terra"
    if is_motorway(value):
        return "Autoestrada"
    return value

def audit_ways_tags_value(value):
    
    if is_name(value):
       return "Nome"
    if is_trunk_link(value):
       return "Tronco de ligação"
    if is_asphalt(value):
       return "Asfalto"
    if is_tertiary(value):
       return "Terciário"
    if is_yes(value):
        return "Sim"
    if is_no(value):
        return "Não"
    if is_trunk(value):
        return "Tronco"
    if is_park(value):
        return "Parque"
    if is_secondary(value):
        return "Secondário"
    if is_designated(value):
        return "Área designada a bicicletas"
    if is_residential(value):
        return "Residencial"
    if is_lane(value):
        return "Faixa"       
    if is_paved(value):
        return "Pavimentado"
    if is_abandoned(value):
        return "Abandonado"
    if is_unclassified(value):
        return "Não classificado"
    if is_cemetery(value):
        return "Cemitério"
    if is_motorway(value):
        return "Autoestrada"
    return value


def process_map():
    create_csv_node_table(NODES_PATH)
    create_csv_node_tags_table(NODE_TAGS_PATH)
    create_csv_ways_table(WAYS_PATH)
    create_csv_ways_tags_table(WAY_TAGS_PATH)
    create_csv_ways_node_table(WAY_NODES_PATH)


if __name__ == '__main__':
    process_map()
    print("Finish the task...")