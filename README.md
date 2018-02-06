# Estudo de Caso de Dados OpenStreetMap

* Local: ,Barueri, São Paulo
* [OpenStreetMap URL] https://www.openstreetmap.org/export#map=13/-23.5121/-46.8357
 
Este mapa é da minha cidade, espero descobrir neste dataset informaçôes relevantes da minha cidade.

# 1. Dados auditados
Olhando para o arquivo XML, descobri que ele usa diferentes tipos de tags. Então, analisei o conjunto de dados da cidade de Barueri, São Paulo usando ElementTree e número de contagem das tags exclusivas.

 
 * `'bounds': 1,`
 * `'member': 9899,`
 * `'meta': 1,`
 * `'nd': 408815,`
 * `'node': 313187,`
 * `'note': 1,`
 * `'osm': 1,`
 * `'relation': 710,`
 * `'tag': 127641,`
 * `'way': 41134 `
 
 
 # 2. Problemas encontrados
 O principal problema que encontramos no conjunto de dados é a inconsistência nas informações e o nomes em inglês.
 Algumas informações foram traduzidas para algo que faz mais sentido e de acordo com a minha região, já que temos variação dependendo da  região.
 
 * **Traduções para o português** 
    * `pt -> Ponte`	
    * `operator -> Concessionária`
    * `crossing_bell -> Cruzamento com sinal sonoro`
    * `public_transport -> Transporte público`
    * `toll_booth -> Pedágio`

* **Abreviações**
    * `pt: -> Ponte`
    * `addr:city -> Cidade`
    * `addr:country -> Country`
    * `addr:housenumber -> NUmero da casa`
    * `addr:state -> Estado`
    * `addr:street -> Bairro`

* **Foram criadas funções para tratar essas traduções e entender melhor as informações no dataset, por exemplo:**

```python 
def is_pt(value):
    return value.find("pt:") > -1
```
* **Foram criadas funções para analisar os valores k e value das tags node e ways **  
   
 ```python
 def audit_node_tags_k(value):
    if is_residential(value):
        return "Residencial"
    if is_highway(value):
        return "Auto estrada"
    if is_stop(value):
        return "Parada"
    if is_train(value):
        return "Trem"
 	.
	.
	# outras funções
  return value
  
 def audit_node_tags_value(value):
     if is_pt(value):
        return "Ponte em "
     if is_motorway_junction(value):
        return "Junção de auto-estrada"
     if is_milestone(value):
        return "Marco Histórico"
     if is_traffic_signals(value):
        return "Sinal de Trânsito"
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
# 3. Visão geral dos dados
### Tamanho dos arquivos:

* `barueri_e_cidades_vizinhas.osm : 70.259 MB`
* `nodes_csv: 26.935 KB`
* `nodes_tags.csv: 238 KB`
* `ways_csv: 2.554 KB`
* `ways_nodes.csv: 9.138 KB`
* `ways_tags.csv: 2.8 KB`
* `openstreet_map.db: 35.840 KB`


###Números de nodes:
``` python
sqlite> SELECT COUNT(*) FROM nodes
```
**Output:**
```
313187
```



### Número de usuários Únicos:
```python
sqlite> SELECT COUNT(DISTINCT(e.uid))          
FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways) e;
```
**Output:**
```
338
```

### Top usuários contribuintes:
```python
sqlite> SELECT e.user, COUNT(*) as num
FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e
GROUP BY e.user
ORDER BY num DESC
LIMIT 10;
```
**Output:**

```
Bonix-importer		150456
Bonix-mapper		73726
Ajbelnuovo		34235
Ygorre			17160
Cxs			14636
O fim			8829
Elias lopes		5891
Rub21			5585
Naoliv			3569
Marcos daniel		2824
```

### Número de usuários que contribuiram apenas uma vez:
```python
sqlite> SELECT COUNT(*) 
FROM
    (SELECT e.user, COUNT(*) as num
     FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e
     GROUP BY e.user
     HAVING num=1) u;
```
**Output:**
```
77
```

# 4. Exploração de dados adicionais

### Ammenities Comuns:
```python
sqlite> SELECT value, COUNT(*) as num
FROM nodes_tags
WHERE key='amenity'
GROUP BY value
ORDER BY num DESC
LIMIT 10;

```
**Output:**
```
Pizza Italiana tradicional	73
Restaurante			41
Religião			33
Banco				25
Farmácia			22
Posto de gasolina		21
Escola				18
Restaurante de Fast Food	9
Caixa eletrônico		8
Estacionamento			8
```


### Religião com mais adeptos:
```python
sqlite> SELECT nodes_tags.value, COUNT(*) as num
FROM nodes_tags 
    JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='Religião') i
    ON nodes_tags.id=i.id
WHERE nodes_tags.key='religion'
GROUP BY nodes_tags.value
ORDER BY num DESC
LIMIT 1;
```
**Output:**
```
Cristianismo	28
```

### Cozinhas populares
```python
sqlite> SELECT nodes_tags.value, COUNT(*) as num
FROM nodes_tags 
    JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='Restaurante') i
    ON nodes_tags.id=i.id
WHERE nodes_tags.key='Cozinha'
GROUP BY nodes_tags.value
ORDER BY num DESC;
```
**Output:**
```
Pizza			7
Comidas regionais	3
Rede de grelhados	3
Amburgueria		1
```

# 5. Conclusion
Os dados do openstreetmap são interessanets e de qualidade, mas os erros causados por entradas inválidas dos usuários são significativos. Nós limpamos e traduzimos uma quantidade significativa de dados necessários para este projeto, mas há muita melhoria necessária no conjunto de dados. O conjunto de dados contém muito menos informações adicionais, como amenidades, atrações turísticas, lugares populares e outros interesses úteis.O conjunto de dados contém informações muito antigas tornando difícil a comparação com o Google Maps ou o Bing Maps, porém acho que há várias oportunidades para a limpeza e validação dos dados no futuro.
 
