# DeepSpeech

## Documentacion

La documentacion original de DeepSpeech se encuentra en la siguiente pagina

https://deepspeech.readthedocs.io/en/latest/?badge=latest

## instalacion

para instalarlo es recomendable realizar un entornno virtual utilizando una python >= 3.6 y una distribucion de Ubunu. 

para el entorno virtual:
```bash
python3 -m venv NOMBRE_ENTORNO_VIRTUAL
```
Para activar el entorno virtual
```bash
source NOMBRE_ENTORNO_VIRTUAL/bin/activate
```

Luego es posible instalar DeepSpeech de su repositorio de GitHub 

```bash
git clone https://github.com/mozilla/DeepSpeech
```
en donde la ultima version disponible es la v0.9.0-alpha.8 .

Luego es necesario instalar DeepSpeech codigo de entrenamiento y sus dependencias utilizando el comando ```pip3```

```bash
cd DeepSpeech
pip3 install --upgrade pip==20.0.2 wheel==0.34.2 setuptools==46.1.3
pip3 install --upgrade -e .
```

El paquete de Python ```webrtcvad``` requiere asegurarnos de tener las herramientas necesarias para crear modulos de Python:

```bash
sudo apt-get install python3-dev
```

## Descarga e importacion de gravaciones

Una vez instalado DeepSpeech se puede descargar grabaciones en español de la siguiente pagina, https://commonvoice.mozilla.org/en/datasets . 

Descomprimir en alguna carpeta, luego:

```bash
cd DeepSpeech
bin/import_cv2.py --filter_alphabet path/to/some/alphabet.txt /path/to/extracted/language/archive
```

El comando anterior requiere de un alfabeto que se utiliza para la validacion de las gravaciones, un posible alfabeto es el siguiente [alphabet.txt](./alphabet.txt) . Es un comando que demora en ejecutarce y demanda 70 GB de disco. 

## Entrenamiento


Para entrenar se puede utilizar el siguiente comando:
```bash
python -u DeepSpeech.py --noshow_progressbar   --train_files ./train_sample.csv   --test_files ./test_sample.csv   --train_batch_size 50   --test_batch_size 50   --n_hidden 100   --epochs 200   --checkpoint_dir ./cheeckpoints   --export_dir ./model
python -u DeepSpeech.py --log_level 2 --train_files ../latino5.train.csv --test_files ../latino5.test.csv --audio_sample_rate 8000 --feature_win_len 24 --feature_win_step 10  --train_batch_size 200 --test_batch_size 100 --n_hidden 50 --epochs 20 --checkpoint_dir ../tmp --export_dir ../models
```

En donde en este ejemplo se utilizo los archivos train_sample.csv y test_sample.csv que contienen una muestra del 1% del dataset utilizado. Claro esta que falta completar el path de los archivos .csv

## Resultado del entrenamiento. 

Dada la limitada capacidad de computo utilice como datos de testeo los mismo datos de entrenamiento, unicamente para fines demostrativos. 

```bash
I Test epoch...
Test on /home/emiliano/Desktop/DataDeepSeech/es/clips/test_sample.csv - WER: 0.579971, CER: 0.155340, loss: 27.475317
--------------------------------------------------------------------------------
Best WER: 
--------------------------------------------------------------------------------
WER: 0.000000, CER: 0.000000, loss: 5.040998
 - wav: file:///home/emiliano/Desktop/DataDeepSeech/es/clips/common_voice_es_20078239.wav
 - src: "fue comendador de mora en la orden de santiago"
 - res: "fue comendador de mora en la orden de santiago"
--------------------------------------------------------------------------------
WER: 0.000000, CER: 0.000000, loss: 2.934779
 - wav: file:///home/emiliano/Desktop/DataDeepSeech/es/clips/common_voice_es_19195403.wav
 - src: "es un actor español"
 - res: "es un actor español"
--------------------------------------------------------------------------------
WER: 0.071429, CER: 0.012500, loss: 13.448547
 - wav: file:///home/emiliano/Desktop/DataDeepSeech/es/clips/common_voice_es_20234332.wav
 - src: "en el lugar aparece un interesante bosque de galería formado por chopos y sauces"
 - res: "en el lugar aparece un interesante bosque de galería pormado por chopos y sauces"
--------------------------------------------------------------------------------
WER: 0.125000, CER: 0.021739, loss: 5.573032
 - wav: file:///home/emiliano/Desktop/DataDeepSeech/es/clips/common_voice_es_19446782.wav
 - src: "es miembro fundador de la inter comercio justo"
 - res: "es miembro fundador de la inter comercio just"
--------------------------------------------------------------------------------
WER: 0.166667, CER: 0.029851, loss: 11.375363
 - wav: file:///home/emiliano/Desktop/DataDeepSeech/es/clips/common_voice_es_19710369.wav
 - src: "los juveniles son parecidos a las hembras pero con el pecho listado"
 - res: "los juvenides son parecidos a las embras pero con el pecho listado"
--------------------------------------------------------------------------------
Median WER: 
--------------------------------------------------------------------------------
WER: 0.600000, CER: 0.148148, loss: 8.358116
 - wav: file:///home/emiliano/Desktop/DataDeepSeech/es/clips/common_voice_es_20288396.wav
 - src: "fue en ese momento decisivo"
 - res: "fue en esemomento de cicio"
--------------------------------------------------------------------------------
WER: 0.615385, CER: 0.130952, loss: 38.960266
 - wav: file:///home/emiliano/Desktop/DataDeepSeech/es/clips/common_voice_es_20723052.wav
 - src: "esto basado en la filosofía de las artes marciales chinas y japonesas principalmente"
 - res: "esto basao en la filasofia de la rtes marciares chinas japonesa pricipamente"
```

Los archivos .csv utilizados en este entrenamiento se encuentran en la carpeta clips, no se pueden utilizar para realizar entrenamientos reales ya que el archivos test_sample.csv es una sub muestra del train_sample.csv. Este entrenamiento es unicamente para ver el alcance. 


# Transcribir un archivo de audio
Una vez obtenido el modelo output_graph.pbmm se pueden transcribir archivos de audio .wav . para esto es necesario crear otro entorno virtual y ejecutar dentro del entorno virtual el siguiente comando. 
```bash
pip install deepspeech
```

Luego descargar el archivo client.py de https://deepspeech.readthedocs.io/en/latest/Python-Examples.html#full-source-code 

y luego dentro del entorno virtual 
```bash
python client.py --model path/to/model-output_graph.pbmm --audio path/to/audio.wav
```

# Streamming
Para hablar a un microfono y que se transcriba el audio es necesario clonar el siguiente repositorio.
```bash
git clone https://github.com/mozilla/DeepSpeech-examples.git
```
ir al directorio
```bash
/deepspeech_streamming/DeepSpeech-examples/mic_vad_streaming
```

y ejecutar
```bash
python mic_vad_streaming.py --model path/to/model-output_graph.pbmm
```
## Nota
A esta ultima opcion no la probe del todo porque no tengo audio en la computadora de mitrol. Pero se ejecuta correctamente y para testearlo es necesario reproducir las mismas frases con las que fue entrenado. 









