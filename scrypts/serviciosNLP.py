import spacy
import csv

import mysql.connector
from mysql.connector import Error


from spacy import displacy
from spacy.matcher import Matcher

def extract_full_name(matcher, nlp_doc, diccionario_aux):
    pattern = [{"POS": "NOUN"}, {"POS": "ADJ"}]
    matcher.add("NOUN+ADJ", [pattern])
    pattern = [{"POS": "PROPN"}, {"POS": "PROPN"}]
    matcher.add("NOUN+NOUN", [pattern])
    pattern = [{"DEP": "nmod"},{"DEP": "case"},{"DEP": "nmod"}]
    matcher.add("ORACION", [pattern])
    
    
    pattern = [{"DEP": "appos"},{"DEP": "case"},{"DEP": "nmod"},{"DEP": "case"},{"DEP": "nmod"}]
    matcher.add("1", [pattern])
    pattern = [{"DEP": "obj"},{"DEP": "case"},{"DEP": "nmod"},{"DEP": "case"},{"DEP": "nmod"}]
    matcher.add("2", [pattern])
    pattern = [{"DEP": "obj"},{"DEP": "case"},{"DEP": "det"},{"DEP": "nmod"}]
    matcher.add("3", [pattern])
    pattern = [{"DEP": "appos"},{"DEP": "case"},{"DEP": "det"},{"DEP": "nmod"}]
    matcher.add("4", [pattern])
    pattern = [{"DEP": "appos"},{"DEP": "case"},{"DEP": "nmod"}]
    matcher.add("5", [pattern])
    
    n=0
    matches = matcher(nlp_doc)
    for _, start, end in matches:
        span = nlp_doc[start:end]
        span.text.lower()
        if "." in span.text or "-" in span.text or ";" in span.text or "1" in span.text or "2" in span.text or "3" in span.text or "4" in span.text or "5" in span.text or "6" in span.text or "7" in span.text or "8" in span.text or "9" in span.text or "0" in span.text or "&" in span.text or "+" in span.text or "=" in span.text or "/" in span.text or "[" in span.text or "]" in span.text or "{" in span.text or "}" in span.text or "$" in span.text or "(" in span.text or ")" in span.text or "•" in span.text or "_" in span.text or "^" in span.text or "*" in span.text:
            break
        else:
            if((span.text.lower() in diccionario_aux) == False):
                diccionario_aux[span.text.lower()] = 1
                n+=1
            else:
                diccionario_aux[span.text.lower()] = diccionario_aux.get(span.text.lower()) + 1            
    return n

def generacionContenidoCSV(nombre_archivo, ruta, header, data):
    row_list = []
    row_list.append(header)
    for i in data:
        row_list.append(i)
    with open(ruta+nombre_archivo+'.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(row_list)
        f.close()

def cargaContenidoCSV(nombre_archivo, ruta, row_list):
    with open(ruta+nombre_archivo+'.csv', encoding='UTF8') as csvfile:
        reader = csv.reader(csvfile, skipinitialspace=True, delimiter=',')
        n=0
        for row in reader:
            if n == 0: 
                n+=1
                pass
            else:  
                row_list.append(row) 
        csvfile.close()
        return row_list


def generacioncontenido_palabrascompuestas( row_list, diccionario_aux, urls):
    total_palabras_claves_compuestas = 0

    nlp = spacy.load("es_dep_news_trf")

    #urls = ['https://drive.google.com/file/d/1ORxPQkKGjdwHuY5FgmTWP3s4iozvS97b/view?hl=es']
    for url in urls:
        cargaContenidoCSV(nombre_archivo=url.split('/')[-2], ruta='../recursos/contenidoHTML/', row_list=row_list)

    for dato in row_list:
        doc = nlp(dato[0])
        
        matcher = Matcher(nlp.vocab)
        text_list = list(doc.sents)
        datos = []
        for i in range(len(text_list)):
            aux = []
            aux.append(i+1)
            aux.append(text_list[i])
            datos.append(aux)
        generacionContenidoCSV(nombre_archivo=url.split('/')[-2], ruta='../recursos/contenidoOraciones/', header=['N°','oraciones'], data=datos)
        for oracion in text_list:
            total_palabras_claves_compuestas = extract_full_name(matcher, oracion, diccionario_aux) + total_palabras_claves_compuestas

    dictionary_sort_reverse = sorted(diccionario_aux.items(), key=lambda x:x[1], reverse=True)
    converted_dict = dict(dictionary_sort_reverse)
 
    with open('../recursos/palabras_claves/'+'2'+'.csv', 'w', encoding='UTF8', newline='') as f:
        w = csv.writer(f)
        for key, value in converted_dict.items():
            w.writerow([key,value])
        f.close()
    diccionario_aux.clear()
    diccionario_aux.update(converted_dict)
    return total_palabras_claves_compuestas


def generacioncontenido_palabrassimples(row_list_simp, diccionario_aux_simples, urls):
    total_palabras_claves_simples = 0

    nlp = spacy.load("es_dep_news_trf")

    #urls = ['https://drive.google.com/file/d/1ORxPQkKGjdwHuY5FgmTWP3s4iozvS97b/view?hl=es']
    for url in urls:
        cargaContenidoCSV(nombre_archivo=url.split('/')[-2], ruta='../recursos/contenidoHTML/', row_list=row_list_simp)
    for dato in row_list_simp:
        doc = nlp(dato[0])
        text_list = list(doc.sents)
        for oracion in text_list:
            for token in oracion:
                if not token.is_stop and not token.is_punct and not token.is_space and len(token)>4:
                    if token.pos_=="PROPN" or token.pos_=="NOUN" or token.pos_=="ADJ":
                        palabra_token=str(token)
                        palabra_lemma=str(token.lemma_)
                        if "." in palabra_token or "-" in palabra_token or ";" in palabra_token or "1" in palabra_token or "2" in palabra_token or "3" in palabra_token or "4" in palabra_token or "5" in palabra_token or "6" in palabra_token or "7" in palabra_token or "8" in palabra_token or "9" in palabra_token or "0" in palabra_token or "&" in palabra_token or "+" in palabra_token or "=" in palabra_token or "/" in palabra_token or "[" in palabra_token or "]" in palabra_token or "{" in palabra_token or "}" in palabra_token or "$" in palabra_token or "(" in palabra_token or ")" in palabra_token or "•" in palabra_token or "_" in palabra_token or "^" in palabra_token or "*" in palabra_token:
                            pass
                        else:
                            if((token.lemma_.lower() in diccionario_aux_simples) == False):
                                diccionario_aux_simples[token.lemma_.lower()] = 1
                                total_palabras_claves_simples+=1
                            else:
                                diccionario_aux_simples[token.lemma_.lower()] = diccionario_aux_simples.get(token.lemma_.lower()) + 1

    dictionary_sort_reverse = sorted(diccionario_aux_simples.items(), key=lambda x:x[1], reverse=True)
    converted_dict = dict(dictionary_sort_reverse)

    with open('../recursos/palabras_claves/'+'1'+'.csv', 'w', encoding='UTF8', newline='') as f:
        w = csv.writer(f)
        for key, value in converted_dict.items():
            w.writerow([key,value])
        f.close()
    diccionario_aux_simples.clear()
    diccionario_aux_simples.update(converted_dict)
    return total_palabras_claves_simples


def conexionBD():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='database_flask',
            user='root',
            password=''
        )

    except Error as ex:
        raise Exception(ex)
    return connection

def almacenamientoBaseDatos(diccionario_aux_simples, diccionario_aux_compuestas):
    try:
        connection = conexionBD()
        cursor = connection.cursor()
        list_aux_one = []
        list_aux_two = []

        list_aux_one = list(diccionario_aux_simples.keys())
        list_aux_two = list(diccionario_aux_simples.values())
        for i in range(len(diccionario_aux_simples)):
            sql = """INSERT INTO contenidos(tipo, total_veces, palabra_clave_simple) VALUES 
                    (%s, %s, %s)"""
            data = ('palabra_clave_simple', list_aux_two[i], list_aux_one[i])
            cursor.execute(sql, data)
            connection.commit()

        list_aux_one = list(diccionario_aux_compuestas.keys())
        list_aux_two = list(diccionario_aux_compuestas.values())
        for i in range(len(diccionario_aux_compuestas)):
            sql = """INSERT INTO contenidos(tipo, total_veces, palabra_clave_compuesta) VALUES 
                    (%s, %s, %s)"""
            data = ('palabra_clave_compue', list_aux_two[i], list_aux_one[i])
            cursor.execute(sql, data)
            connection.commit()
    except Exception as ex:
        raise Exception(ex)

    cursor.close()
    connection.close()
    return 0



"""
urls = ['https://drive.google.com/file/d/1ORxPQkKGjdwHuY5FgmTWP3s4iozvS97b/view?hl=es',
        'https://drive.google.com/file/d/1r-4hQ7z-k0mQ0S2T0fs3_LQAkkV1VmGg/view?hl=es',
        'https://drive.google.com/file/d/1fORpcef43VeuT192tpSNbzpF2vt8T8Hl/view?hl=es',
        'https://drive.google.com/file/d/13BDgfsTtgVWIS1tXpkKCUJVSdtzrgJI-/view?hl=es',
        'https://drive.google.com/file/d/1GHB5U0vguLBZtVqZnJ40t2Me1-R01qmp/view?hl=es',
        'https://drive.google.com/file/d/1LqE1yxAFWo2yaPTgXczRIabZBQ61qMu6/view?hl=es']
"""
row_list = []
diccionario_aux = {} 
#print(generacioncontenido_palabrascompuestas(row_list, diccionario_aux, urls))


row_list_simp = []
diccionario_aux_simples = {}
#print(generacioncontenido_palabrassimples(row_list_simp, diccionario_aux_simples, urls))

#almacenamientoBaseDatos(diccionario_aux_simples, diccionario_aux)
