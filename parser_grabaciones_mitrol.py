
#%%
import os
import csv
import random
import wave

PATH = '/mnt/grabaciones/Chile'

ARCHIVOS_IN_PATH=sorted(os.listdir(PATH))

for i in range(len(ARCHIVOS_IN_PATH)):

    ARCHIVOS_IN_PATH[i] = ARCHIVOS_IN_PATH[i][0:-4]

ARCHIVOS_IN_PATH = list(set(ARCHIVOS_IN_PATH))
PAIS = []
archivos_mal=[]

for file in ARCHIVOS_IN_PATH:
    try:
        wav_file = str(os.path.join(PATH,file + '.wav'))
        text_file = str(os.path.join(PATH,file + '.txt'))
        wav_filename = file + '.wav'
        wav_filesize = os.path.getsize(wav_file)
        with open(text_file, encoding='ISO-8859-1') as txt:
            textos = txt.readlines()
            for texto in textos:
                if texto[0] != ';':
                    transcript = texto
        if '[' in transcript:
            continue
        elif '*' in transcript:
            continue
        elif '&' in transcript:
            continue
        elif '\n' in transcript:
            continue
        elif '@' in transcript:
            continue
        PAIS.append([wav_filename, wav_filesize, transcript.lower()])
    except:
        archivos_mal.append(file)
        continue


for audio in PAIS:
    try:
        path = PATH + '/' + audio[0]
        wave.open(path, 'rb')
    except:
        print(audio[0])
        

with open('/home/muke/Grabaciones/chile_todo.csv', 'w', newline="") as f:
    FILAS = csv.writer(f, delimiter=',')
    FILAS.writerow(['wav_filename','wav_filesize','transcript'])
    for fila in PAIS:
        FILAS.writerow(fila)

random.shuffle(PAIS)

TRAIN_SAMPLE = PAIS[0:int(len(PAIS)*0.99)]

with open('/home/muke/Grabaciones/chile_train.csv', 'w') as f:
    FILAS = csv.writer(f, delimiter=',')
    FILAS.writerow(['wav_filename','wav_filesize','transcript'])
    for fila in TRAIN_SAMPLE:
        FILAS.writerow(fila)

TEST_SAMPLE = PAIS[int(len(PAIS)*0.99):]
with open('/home/muke/Grabaciones/chile_test.csv', 'w') as f:
    FILAS = csv.writer(f, delimiter=',')
    FILAS.writerow(['wav_filename','wav_filesize','transcript'])
    for fila in TEST_SAMPLE:
        FILAS.writerow(fila)

