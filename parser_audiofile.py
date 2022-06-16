import os
import csv
import random
import wave

# PATH = '/home/muke/Grabaciones/Chile'
wav_file = input('Archivo: ')
with open(wav_file, encoding='ISO-8859-1') as wavs:
    tmp = wavs.readlines()

#elimino los repetidos 
wavs = list(set(tmp))

#elimino el .wav
for i in range(len(wavs)):
    wavs[i] = wavs[i][0:-4]

PAIS = []
archivos_mal=[]

for file in wavs:
    try:
		wav_file = file + '.wav'
        text_file = file + '.txt'
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
        PAIS.append([wav_file, wav_filesize, transcript.lower()])
    except:
        archivos_mal.append(file)
        continue

random.shuffle(PAIS)

TRAIN_SAMPLE = PAIS[0:int(len(PAIS)*0.90)]

train_file = input('Train: ')

with open(train_file, 'w') as f:
    FILAS = csv.writer(f, delimiter=',')
    FILAS.writerow(['wav_filename','wav_filesize','transcript'])
    for fila in TRAIN_SAMPLE:
        FILAS.writerow(fila)

TEST_SAMPLE = PAIS[int(len(PAIS)*0.90):]
test_file = input('Train: ')
with open(test_file, 'w') as f:
    FILAS = csv.writer(f, delimiter=',')
    FILAS.writerow(['wav_filename','wav_filesize','transcript'])
    for fila in TEST_SAMPLE:
        FILAS.writerow(fila)

