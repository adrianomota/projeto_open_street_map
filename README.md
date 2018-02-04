# Estudo de Caso de Dados OpenStreetMap

**Name:** Adriano Mota

* Local: ,Barueri, São Paulo
 [OpenStreetMap URL] https://www.openstreetmap.org/export#map=13/-23.5121/-46.8357
 
Este mapa é da minha cidade, espero descobrir neste dataset informaçôes relevantes da minha cidade.

# 1. Dados auditados
Olhando para o arquivo XML, descobri que ele usa diferentes tipos de tags. Então, analisei o conjunto de dados da cidade de Barueri, São Paulo usando ElementTree e número de contagem das tags exclusivas.

 *{
 'bounds': 1,
 'member': 9899,
 'meta': 1,
 'nd': 408815,
 'node': 313187,
 'note': 1,
 'osm': 1,
 'relation': 710,
 'tag': 127641,
 'way': 41134 
 }
 
 # 2. Problemas encontrados
 O principal problema que encontramos no conjunto de dados é a inconsistência nas informações e o nomes em inglês.
 Algumas informações foram traduzidas para algo que faz mais sentido e de acordo com a minha região, já que temos variação dependendo da  região.
 
 * **Traduções para o português** 
    * `operator -> Concessionária`
    * `crossing_bell -> Cruzamento com sinal sonoro`
    * `public_transport -> Transporte público`
    * `toll_booth -> Pedágio`

* **Abreviações **
    * `pt: -> Ponte`
    * `addr:city -> Cidade`
    * `addr:country -> Country`
    * `addr:housenumber -> NUmero da casa`
    * `addr:state -> Estado`
    * `addr:street -> Bairro`

* ** Foram criadas funções para tratar essas traduções e entender melhor as informações no dataset, por exemplo:

```python 
def is_pt(value):
    return value.find("pt:") > -1
```
* ** Foram criadas funções para analisar os valores k e value das tags node e ways *  
   
 ```python
 def audit_node_tags_k(value):
    if is_residential(value):
        return "Residencial"
	.
	.
	# outras funções
  return
  
 def audit_node_tags_value(value):
     if is_pt(value):
        return "Ponte em "
	.
	.
	# outras funções
 return value
 
 # funções audit_node_tags_k e audit_node_tags_value
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

# funções audit_ways_tags_k e audit_ways_tags_value
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

```

* **File sizes: *

barueri_e_cidades_vizinhas.osm : 70.259 MB
nodes_csv: 26.935 KB
nodes_tags.csv: 238 KB
ways_csv: 2.554 KB
ways_nodes.csv: 9.138 KB
ways_tags.csv: 2.8 KB
openstreet_map.db: 35.840 KB
