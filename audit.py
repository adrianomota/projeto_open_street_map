import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSM_PATH = "dataset/barueri_e_cidades_vizinhas.osm"
regex = re.compile(r'\b\S+\.?', re.IGNORECASE)

expected = ["Avenida", "Alameda", "Parque", "Jardim", "Travessa", "Rua", "Estrada","Rodovia","Rotatória","Praca","Largo"]  #expected names in the dataset

mapping = {"Av.": "Avenida",
           "R.": "Rua",
           "Praca":"Praça",
           "Rotatoria":"Rotatória",
          }
 #Esta função faz uma iteração sobre cada node do arquivo osm
def get_element(osm_file, tags=('node', 'way', 'relation')):
    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()

# Procura a string pelo regex. Senão satisfazer a consição adiciona na lista.
def audit_street(street_types, street_name): 
    m = regex.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def is_street_name(elem): # Verifica se é um nome de rua
    return (elem.attrib['k'] == "addr:street")



def audit(osmfile): # retorna a lista com so noems auditadps
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for elem in get_element(OSM_PATH, tags=('node','way')):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street(street_types, tag.attrib['v'])

    return street_types

pprint.pprint(dict(audit(OSM_PATH))) # imprime os nomes

def string_case(s): # atualiza os nomes para a primeira letra em maiuscula
    if s.isupper():
        return s
    else:
        return s.title()

# retorna os nomes atualizados
def update_name(name, mapping):
    name = name.split(' ')
    for i in range(len(name)):
        if name[i] in mapping:
            name[i] = mapping[name[i]]
            name[i] = string_case(name[i])
        else:
            name[i] = string_case(name[i])
    
    name = ' '.join(name)
   

    return name

update_street = audit(OSM_PATH) 

# Imprime os nomes atualizados
for street_type, ways in update_street.items():
    for name in ways:
        better_name = update_name(name, mapping)
        print(name, "=>", better_name)  