'''
    Descrição:
      Esta função verifica se há mais de um telefone

    Utilização:
      update_phones('+551199991111;+551199991111')

    Parâmetros:
      phones
        Valor do tipo texto a ser pesquisado. No caso 'station'

    Retorno
      string
'''
def update_phones(phones):
    if phones.find(";") > -1:
       numbers = phones.split(";")
       return str(numbers[:1])
    return phones


'''
    Descrição:
      Esta função verifica se o valor da variavel value possui um formato válido de telefone

    Utilização:
      update_phone('+551199991111')

    Parâmetros:
      phone
        Valor do tipo texto a ser pesquisado. No caso 'station'

    Retorno
      string
'''
def update_phone(phone):
    ret_phone = update_phones(phone)
    rem_trace = ret_phone.replace('-','')
    rem_parentheses_left = rem_trace.replace('(','')
    rem_parentheses_right = rem_parentheses_left.replace(')','')
    rem_signal = rem_parentheses_right.replace('+55','')
    rem_one_one = rem_signal.replace('11 ','').strip()
    return "{0}{1}".format('011',rem_one_one)
    


'''
    Descrição:
      Esta função encontra padrões nos CEPs os atualiza para o formato 00000000 sem traços

    Utilização:
      update_postcode('00000999')

    Parâmetros:
      value
        Valor do tipo texto a ser analisado.
    
    Retorno
        str
''' 
def update_postcode(value):
    return "{0}{1}".format(value[0:5],value[6:9])