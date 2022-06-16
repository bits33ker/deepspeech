import json
import numpy as np
import sys
n = len(sys.argv)
if n<2:
    #quit()
    sys.exit('python tfresults -file filename')

a=1
printnames = 0
nombre = ''
minwer= 0
maxwer = 0
minwords = 0
maxwords = 0
while a<n:
    key = sys.argv[a]
    print(key)
    #if key.startswith('-'):
    if key =='-file':
        a = a + 1
        nombre = sys.argv[a]
    elif key == '-names':
        printnames = 1
    elif key == '-maxwer':
        a = a + 1
        maxwer = float(sys.argv[a])
    elif key == '-minwer':
        a = a + 1
        minwer = float(sys.argv[a])
    elif key == '-maxwords':
        a = a + 1
        maxwords = float(sys.argv[a])
    elif key == '-minwords':
        a = a + 1
        minwords = float(sys.argv[a])
    a = a+1
#print(nombre)
with open(nombre) as json_file:
    palabras = 0
    wdistance = 0
    wer = 0
    data = json.load(json_file)
    procesados = 0
    for j in data:
        #kv = j.items()
        #j es un array de diccionarios
        w = float(j['wer'])
        p = j['word_length']
        if (minwer==0 and maxwer==0 and minwords==0 and maxwords==0) or ((minwer<=w or minwer==0) and (maxwer==0 or maxwer>=w) and (minwords<=p or minwords==0) and (maxwords>=p or maxwords==0)):
            palabras = palabras + p #palabras originales
            wdistance = wdistance+ j['word_distance'] #palabras erroneas
            wer = wer + round(w * int(j['word_length']))
            if printnames:
                print(j['wav_filename'])
            procesados = procesados + 1
    print('Cantidad de Archivos procesados: ' + str(procesados))
    print('Cantidad de palabras: ' + str(palabras))
    print('distancia de palabras: ' + str(wdistance))
    print('Cantidad de palabras erroneas: ' + str(wer))
    print('WER: ' + str(float(wer)/palabras))
    