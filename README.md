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
 O principal problema que encontramos no conjunto de dados é a inconsistência nas informações e a nomenclatura em inglês.
 Algumas informações foram traduzidas para algo que faz mais sentido.
 
 * **Traduções para o português** 
    * `operator -> Concessionária`
    * `crossing_bell -> Cruzamento com sinal sonoro`
    * `public_transport -> Transporte público`
    * `toll_booth -> Pedágio`
    
* ** Foram criadas funções para tratar essas traduções e entender melhor as informações no dataset

```python 
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
    return value.find("bump")    

def is_communication(value):
    return value.find("communication") > -1    

def is_waterway(value):
    return value.find("waterway") > -1

def is_lock_gate(value):
    return value.find("lock_gate") > -1
	return name
```
    
    
 
 
