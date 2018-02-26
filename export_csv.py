import csv
import xml.etree.cElementTree as ET
from lxml import etree
import pprint
import re
import codecs
from io import StringIO
import string
import udacity.helper.translate as helper
import udacity.helper.clean_data as clean

'''caminho do arquivo .osm'''
OSM_PATH = "dataset/barueri_e_cidades_vizinhas.osm"

'''#caminho do arquivo nodes,csv'''
NODES_PATH = "dataset/csv/nodes.csv"

'''caminho do arquivo nodes_tags,csv'''
NODE_TAGS_PATH = "dataset/csv/nodes_tags.csv"

'''caminho do arquivo ways,csv'''
WAYS_PATH = "dataset/csv/ways.csv"

'''caminho do arquivo ways_nodes,csv'''
WAY_NODES_PATH = "dataset/csv/ways_nodes.csv"

'''caminho do arquivo ways_tags,csv'''
WAY_TAGS_PATH = "dataset/csv/ways_tags.csv"


'''tupla contendo so campos do arquivo nodes.csv'''
field_nodes = { 'id':'',
                'lat':'',
                'lon':'',
                'user':'',
                'uid':'',
                'version':'',
                'changeset':'',
                'timestamp':''}


'''tupla contendo so campos do arquivo nodes_tags.csv'''
field_nodes_tags = { 'id':'',
                     'key':'',
                     'value':'',
                     'type':'' }

'''tupla contendo so campos do arquivo ways.csv'''
field_ways = { 'id':'',
               'user':'',
               'uid':'',
               'version':'',
               'changeset':'',
               'timestamp':'' }

'''tupla contendo so campos do arquivo ways_tags.csv'''
field_ways_tags = { 'id':'',
                    'key':'',
                    'value':'',
                    'type':'', }

'''tupla contendo so campos do arquivo ways_nodes.csv'''
field_way_node = { 'id':'',
                   'node_id':'',
                   'position':'' }

'''
    Descrição:
      Esta função faz a verificação se o valor é um número

    Utilização:
      audit_if_value_helper.is_numeric(10)

    Parâmetros:
      value
        Um valor numérico
'''
def audit_if_value_is_numeric(value):
    if not value.isnumeric():
        return value

'''
    Descrição:
      Esta função escreve o cabeçalho de arquivo do tipo CSV

    Utilização:
      create_header_csv(csv,campos)

    Parâmetros:
      csv
        um arquivo csv já criado em dhelper.isco
      campos
        Uma tupla contendo os campos do cabeçalho do arquivo csv
''' 
def create_header_csv(csv, fields):
    fields_table = []
    for key, value in fields.items():
        fields_table.append(key)
    csv.writerow(fields_table)
  

'''
    Descrição:
      Esta função escreve o as lianhas do arquivo do tipo CSV

    Utilização:
      create_row_csv(csv,campos)

    Parâmetros:
      csv
        Arquivo csv
      campos
        Uma tupla contendo os campos do cabeçalho do arquivo csv
''' 
def create_row_csv(csv, f):
    lines = []
    for key, value in f.items():
        lines.append(value)
    csv.writerow(lines)

'''
    Descrição:
      Esta função faz uma iteração sobre cada node do arquivo osm

    Utilização:
      get_element(OSM_PATH, tags=('node'))

    Parâmetros:
      osm_file
        Caminho do Arquivo osm
      tags
        tags a serem lidas do arquivo osm
''' 
def get_element(osm_file, tags=('node', 'way', 'relation')):
    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()

'''
    Descrição:
      Esta função faz cria o arquivo node.csv

    Utilização:
      create_csv_node_table(NODES_PATH)

    Parâmetros:
      file
        Caminho do arquivo node.csv
''' 
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
     

'''
    Descrição:
      Esta função faz cria o arquivo node_tags.csv

    Utilização:
      create_csv_node_tags_table(NODES_TAGS_PATH)

    Parâmetros:
      file
       Caminho do arquivo node_tags.csv
''' 
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

                            
'''
    Descrição:
      Esta função faz cria o arquivo ways.csv

    Utilização:
      create_csv_ways_table(WAYS_PATH)

    Parâmetros:
      file
        Caminho do arquivo ways.csv
''' 
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



'''
    Descrição:
      Esta função faz cria o arquivo ways_tags.csv

    Utilização:
      create_csv_ways_tags_table(WAYS_TAGS_PATH)

    Parâmetros:
      file
        Caminho do arquivo ways_tags.csv
''' 
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



'''
    Descrição:
      Esta função faz cria o arquivo ways_nodes.csv

    Utilização:
      create_csv_ways_tags_table(WAYS_NODES_PATH)

    Parâmetros:
      file
        Caminho do arquivo ways_nodes.csv
''' 
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



'''
    Descrição:
      Esta função faz a auditoria dos valores do atributo k da tag node_tag '

    Utilização:
      audit_node_tags_k(tag.attrib['k'])

    Parâmetros:
      value
        Valor do tipo texto

    Retorno
      string
'''
def audit_node_tags_k(value):
    
    if helper.is_residential(value):
        return "Residencial"
    if helper.is_highway(value):
        return "Auto estrada"
    if helper.is_stop(value):
        return "Parada"
    if helper.is_train(value):
        return "Trem"
    if helper.is_public_transport(value):
        return "Transporte Público"
    if helper.is_cuisine(value):
        return "Cozinha"
    if helper.is_distance_word(value):
        return "Distância"
    if helper.is_barrier(value):
        return "Barreira"
    if helper.is_operator(value):
        return "Concessionária"
    if helper.is_place(value):
        return "Lugar"
    if helper.is_description(value):
        return "Descrição"
    if helper.is_name(value):
        return "Nome"
    if helper.is_highway(value):
        return "Rodovia"
    if helper.is_wheelchair(value):
        return "Cadeira de rodas"
    if helper.is_yes(value):
        return "Sim"
    if helper.is_toilets_wheelchair(value):
        return "Sanitário para cadeirantes"
    if helper.is_crossing_barrier(value):
        return "Cruzamento com barreiras"
    if helper.is_crossing_bell(value):
        return "Cruzamento com sinal sonoro"
    if helper.is_crossing_chicane(value):
        return "Cruzamento com chicane"
    if helper.is_crossing_light(value):
        return "Cruzamento iluminado"
    if helper.is_crossing_saltire(value):
        return "Cruzamento em diagonal"
    if helper.is_crossing_supervision(value):
        return "Cruzamento Supervisionado"
    if helper.is_noexit(value):
        return "Sem saída"
    if helper.is_turning_circle(value):
        return "Rotatória"
    if helper.is_population(value):
        return "População"
    if helper.is_charge(value):
        return "Carregar"
    if helper.is_bicycle(value):
        return "Bicicleta"
    if helper.is_railway(value):
        return "Estrada de ferro"
    if helper.is_power(value):
        return "Energia"
    if helper.is_bus(value):
        return "Ônibus"
    if helper.is_waterway(value):
        return "Via fluvial"
    if helper.is_crossing(value):
        return "Cruzamento"
    if helper.is_traffic_signals(value):
        return "Sinal de Trânsito"
    if helper.is_rank(value):
        return "Classificação"
    if helper.is_source(value):
        return "Fonte"
    if helper.is_brand(value):
        return "Marca"
    if helper.is_shop(value):
        return "Fazer compras"
    if helper.is_bump(value):
        return "Colisão"
    if helper.is_note(value):
        return "Observação"
    if helper.is_pt(value):
        return "Ponte "
    if helper.is_addr_city(value):
        return "Cidade"
    if helper.is_addr_country(value):
        return "País"
    if helper.is_addr_housenumber(value):
        return "Número"
    if helper.is_addr_postcode(value):
        return "CEP"
    if helper.is_addr_state(value):
        return "UF"
    if helper.is_addr_street(value):
        return "Rua"
    if helper.is_addr_suburb(value):
        return "Bairro"
    if helper.is_bank(value):
        return "Banco"
    if helper.is_atm(value):
        return "Caixa eletrônico"
    if helper.is_phone(value):
        return "Telefone"
    if helper.is_station(value):
        return 'Estação'
    return value



'''
    Descrição:
      Esta função faz a auditoria dos valores do atributo value da tag node_tag'

    Utilização:
      audit_node_tags_value(tag.attrib['value'])

    Parâmetros:
      value
        Valor do tipo texto.
'''
def audit_node_tags_value(value):
    
    if helper.is_residential(value):
        return "Residencial"
    if helper.is_pt(value):
      return "Ponte em "
    if helper.is_motorway_junction(value):
        return "Junção de auto-estrada"
    if helper.is_milestone(value):
        return "Marco Histórico"
    if helper.is_traffic_signals(value):
        return "Sinal de Trânsito"
    if helper.is_switch(value):
        return "Interrupção de linha férrea"
    if helper.is_fast_food(value):
        return "Restaurante de Fast Food"
    if helper.is_toll_booth(value):
        return "Pedágio"
    if helper.is_city(value):
        return "Cidade"
    if helper.is_stop(value):
        return "Parada"
    if helper.is_yes(value):
        return "Sim"
    if helper.is_mini_roundabout(value):
        return "Mini rotatória"
    if helper.is_signal(value):
        return "Sinal"
    if helper.is_crossing(value):
        return "Cruzamento"
    if helper.is_stop_position(value):
        return "Embarque"
    if helper.is_shelter(value):
        return "Abrigo"
    if helper.is_parking(value):
        return "Estacionamento"
    if helper.is_sports_centre(value):
        return "Centro Desportivo"
    if helper.is_bus_stop(value):
        return "Ponto de Ônibus"
    if helper.is_restaurant(value):
        return "Restaurante"
    if helper.is_fuel(value):
        return "Posto de gasolina"
    if helper.is_supermarket(value):
        return "Supermercado"
    if helper.is_tourism(value):
        return "Turhelper.ismo"
    if helper.is_helipad(value):
        return "Heliponto"
    if helper.is_tower(value):
        return "Torre"
    if helper.is_bakery(value):
        return "Padaria"
    if helper.is_bump(value):
        return "Colisão"
    if helper.is_turning_circle(value):
        return "Rotatória"
    if helper.is_communication(value):
        return "Comunicação"
    if helper.is_lock_gate(value):
        return "Portão de bloqueio"
    if helper.is_source(value):
        return "Origem"
    if helper.is_exit(value):
        return "Saída"
    if helper.is_shelter(value):
        return "Abrigo"
    if helper.is_bank(value):
        return "Banco"
    if helper.is_pharmacy(value):
        return "Farmácia"
    if helper.is_school(value):
        return "Escola"
    if helper.is_place_of_worship(value):
        return "Religião"
    if helper.is_atm(value):
        return "Caixa eletrônico"
    if helper.is_christian(value):
        return "Cristianismo"
    if helper.is_pizza(value):
        return "Pizza"
    if helper.is_regional(value):
        return "Comidas Regionais"
    if helper.is_steak_house(value):
        return "Rede de grelhados"
    if helper.is_burger(value):
        return "Amburgueria"
    if helper.is_italian_pizza(value):
        return "Pizza Italiana tradicional"
    if helper.is_addr_suburb(value):
        return "Bairro"
    if helper.is_avenida_abbreviation(value):
        return value.replace('Av.','Avenida')
    if helper.is_jardim_abbreviation(value):
        return value.replace('Jd.','Jardim')
    if helper.is_parque_abbreviation(value):
        return value.replace("Pq.","Parque")
    if helper.is_rua_abbreviation(value):
        return value.replace('R.','Rua')
    if helper.is_doutor_abbreviation(value):
        return value.replace('Dr.','Doutor')
    if helper.is_alameda_abbreviation(value):
        return value.replace('Al.','Alameda')
    if helper.is_station(value):
        return 'Estação'
    if helper.is_phone_value(value):
        return clean.update_phone(value)
    if helper.is_postcode_value(value):
        return clean.update_postcode(value)
    return value



'''
    Descrição:
      Esta função faz a auditoria dos valores do atributo k da tag way_tag'
is_tower
    Utilização:
      audit_ways_tags_k(tag.attrib['k'])

    Parâmetros:
      value
        Valor do tipo texto.
'''
def audit_ways_tags_k(value):
    
    if helper.is_name(value):
       return "Nome"
    if helper.is_highway(value):
       return "Rodovia"
    if helper.is_lane(value):
       return "Phelper.istas"
    if helper.is_maxspeed(value):
       return "Velocidade Máxima"
    if helper.is_oneway(value):
       return "Sentido único"
    if helper.is_surface(value):
       return "Superfície"
    if helper.is_paved(value):
       return "Pavimentado"
    if helper.is_toll(value):
       return "Pedágio"        
    if helper.is_layer(value):
       return "Camadas"
    if helper.is_sidewalk(value):
       return "Calçada" 
    if helper.is_destination(value):
       return "Destino"
    if helper.is_leisure(value):
        return "Lazer"
    if helper.is_bicycle(value):
        return "Bicicleta"
    if helper.is_cycleway_left(value):
        return "Ciclo a esquerda"
    if helper.is_cycleway_right(value):
        return "Ciclo a direita"
    if helper.is_foot(value):
        return "Possui passagem de pedestres"
    if helper.is_bridge(value):
        return "Ponte"
    if helper.is_railway(value):
        return "Estrada de ferro"
    if helper.is_horse(value):
        return "Cavalo"
    if helper.is_landuse(value):
        return "Uso da terra"
    if helper.is_motorway(value):
        return "Autoestrada"
    if helper.is_addr_postcode(value):
        return "CEP"
    return value



'''
    Descrição:
      Esta função faz a auditoria dos valores do atributo value da tag way_tag'

    Utilização:
      audit_ways_tags_k(tag.attrib['value'])

    Parâmetros:
      value
        Valor do tipo texto.
'''
def audit_ways_tags_value(value):
    
    if helper.is_name(value):
       return "Nome"
    if helper.is_trunk_link(value):
       return "Tronco de ligação"
    if helper.is_asphalt(value):
       return "Asfalto"
    if helper.is_tertiary(value):
       return "Terciário"
    if helper.is_yes(value):
        return "Sim"
    if helper.is_no(value):
        return "Não"
    if helper.is_trunk(value):
        return "Tronco"
    if helper.is_park(value):
        return "Parque"
    if helper.is_secondary(value):
        return "Secondário"
    if helper.is_designated(value):
        return "Área designada a bicicletas"
    if helper.is_residential(value):
        return "Residencial"
    if helper.is_lane(value):
        return "Faixa"       
    if helper.is_paved(value):
        return "Pavimentado"
    if helper.is_abandoned(value):
        return "Abandonado"
    if helper.is_unclassified(value):
        return "Não classificado"
    if helper.is_cemetery(value):
        return "Cemitério"
    if helper.is_motorway(value):
        return "Autoestrada"
    if helper.is_postcode_value(value):
        return clean.update_postcode(value)
    return value



# ================================================== #
#               Main Function                        #
# ================================================== #

'''
    Descrição:
      Esta função processa a criação de todos os arquivos csv.'
 
    Utilização:
      process_map()
'''
def process_map():
    create_csv_node_table(NODES_PATH)
    create_csv_node_tags_table(NODE_TAGS_PATH)
    create_csv_ways_table(WAYS_PATH)
    create_csv_ways_tags_table(WAY_TAGS_PATH)
    create_csv_ways_node_table(WAY_NODES_PATH)


if __name__ == '__main__':
    process_map()
    print("Finished the task...")