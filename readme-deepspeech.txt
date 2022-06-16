README DeepSpeech
sudo apt install virtualenv
virtualenv --python=/usr/bin/python2.6 <path/to/new/virtualenv/>

en caso de no tener python 3.6:
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.6

pip3 install tensorflow-cpu==2.3.0


Para mapear Windows en linux: 
https://www.tecmint.com/install-virtualbox-guest-additions-in-ubuntu/
https://www.maketecheasier.com/mount-windows-share-folder-linux/


DeepSpeech:
http://www.michaelvenz.com/2018/10/mozilla-deepspeech-on-ubuntu-18-04/
https://github.com/nahuelproietto/deepspeech-spanish-model
https://www.caito.de/
https://deepspeech.readthedocs.io/en/latest/TRAINING.html
https://deepspeech.readthedocs.io/en/v0.7.1/Flags.html

Compilar codigo fuente: https://www.tensorflow.org/install/source?hl=es-419
Con git me baje el tag 1.15.4 que es el de DeepSpeech, realice el configure. Tuve que modificar log_linux como dije mas abajo
Tensorflow: baje el r2.3
La compile de la siguiente forma :  bazel build --verbose_failures --cxxopt=-std=c++11 -c opt --config=mkl //tensorflow/tools/pip_package:build_pip_package
Una vez que dio ok genere el pkg: ./bazel-bin/tensorflow/tools/pip_package/build_pip_package /home/muke/tensorflow_pkg
Y luego fui al venv de DeepSpeech y lo instale ahi: pip install /home/mituser/tensorflow_pkg/tensorflow-1.15.4-cp36-cp36m-linux_x86_64.whl

Problemas:
1. fue necesario cargar la libpython3.6-dev xq no se encontraba el include/python3.6m.
https://packages.ubuntu.com/bionic/amd64/libpython3.6-dev/filelist

2. Error debido a cambios en la glibc:
external/grpc/src/core/lib/gpr/log_linux.cc:43:13: error: ambiguating new declaration of 'long int gettid()'
   43 | static long gettid(void) { return syscall(__NR_gettid); }
      |             ^~~~~~
In file included from /usr/include/unistd.h:1170,
                 from external/grpc/src/core/lib/gpr/log_linux.cc:41:
Es necesario hacer un patch.https://github.com/tensorflow/tensorflow/issues/33758, https://github.com/grpc/grpc/pull/18950
Los patch existentes a este problema son para lass versiones nuevas de tensorflow. Asi que lo modificamos a mano.
Hay que ir a log_linux.cc y cambiar la definicion de gettid() por sys_gettid() y todas las llamadas en ese archivo. es una funcion local.
nano tensorflow/bazel-tensorflow/external/grpc/src/core/lib/gpr/log_linux.cc
3. Hubo que instalar Bazel desde 0 para compilar la aplicacion: https://docs.bazel.build/versions/master/install-ubuntu.html

test:
python client.py --model /home/muke/models/output_graph.pb --audio /home/muke/Grabaciones/Chile/aabcastro_1_150316093450089_ACD_59808-c1-114529.wav

train:
python -u DeepSpeech.py --noshow_progressbar --train_files /home/muke/Grabaciones/Chile/chile_train.csv --test_files /home/muke/Grabaciones/Chile/chile_test.csv --audio_sample_rate 8000 --train_batch_size 120 --test_batch_size 80 --n_hidden 500 --epochs 200 --checkpoint_dir /home/muke/tmp --export_dir /home/muke/models

python -u DeepSpeech.py --log_level 2 --train_files /home/muke/Grabaciones/Chile/chile_train.csv --test_files /home/muke/Grabaciones/Chile/chile_test.csv --audio_sample_rate 8000 --feature_win_len 24 --feature_win_step 10  --train_batch_size 100 --test_batch_size 100 --n_hidden 50 --epochs 20 --checkpoint_dir /home/muke/tmp --export_dir /home/muke/models

models:
python -u DeepSpeech.py --log_level 2 --train_files /home/muke/Grabaciones/Chile/chile_train.csv --test_files /home/muke/Grabaciones/Chile/chile_test.csv --audio_sample_rate 8000 --feature_win_len 24 --feature_win_step 10  --train_batch_size 50 --test_batch_size 10 --n_hidden 75 --epochs 20 --checkpoint_dir /home/muke/tmp --export_dir /home/muke/models
model2:
python -u DeepSpeech.py --log_level 2 --train_files /home/muke/Grabaciones/Chile/chile_train.csv --test_files /home/muke/Grabaciones/Chile/chile_test.csv --audio_sample_rate 8000 --feature_win_len 24 --feature_win_step 10  --train_batch_size 20 --test_batch_size 5 --n_hidden 75 --epochs 20 --checkpoint_dir /home/muke/tmp --export_dir /home/muke/model2

python -u DeepSpeech.py --log_level 2 --train_files /home/muke/latino5.train.csv --test_files /home/muke/latino5.test.csv --audio_sample_rate 8000 --feature_win_len 24 --feature_win_step 10  --train_batch_size 20 --train_batch_size 80 --test_batch_size 80 --n_hidden 40 --epochs 15 --checkpoint_dir /home/muke/tmp --export_dir /home/muke/latino5

python -u DeepSpeech.py --log_level 2 --train_files /home/muke/latino5.train.csv --dev_files /home/muke/latino5.dev.csv --test_files /home/muke/latino5.test.csv --audio_sample_rate 8000 --feature_win_len 24 --feature_win_step 10  --train_batch_size 20 --train_batch_size 80 --test_batch_size 80 --n_hidden 400 --epochs 9 --test_output_file /home/muke/Modelos/latino5.2/output --checkpoint_dir /home/muke/tmp --export_dir /home/muke/Modelos/latino5.2

KenLM: toma el texto del stdin
https://stt.readthedocs.io/en/latest/LANGUAGE_MODEL.html
## no se usa. cat files/latino5.train.kenlm.txt | kenlm/build/bin/lmplz -T tmp/ -S 10G -o 3 >files/latino5.arpa
python3 data/lm/generate_lm.py --input_txt ../files/latino5.train.kenlm.txt --output_dir ../lm/ --top_k 500000 --kenlm_bins ../kenlm/build/bin --arpa_order 3 --max_arpa_memory 85% --arpa_prune "0|0|1" --binary_a_bits 255 --binary_q_bits 8 --binary_type trie
Bajo wget https://github.com/coqui-ai/STT/releases/download/v1.3.0/native_client.tflite.linux.tar.xz
./generate_scorer_package --checkpoint ../../models/latino3 --lm ../../lm/lm.binary --vocab ../../lm/vocab-500000.txt --package ../../lm/latino3.scorer --default_alpha 0.931289039105002 --default_beta 1.1834137581510284

Inference:
python3 ../client.py --model ../models/latino3/output_graph.pb --scorer ../lm/latino3.scorer --audio /mnt/mailabs/es_ES/by_book/mix/don_quijote/wavs.8000/quijote_vol1_05_cervantes_f000035.wav --candidate_transcripts 5
python3 evaluate_tflite.py --model ../models/latino3/output_graph.pb --scorer ../lm/latino3.scorer --csv ../files/latino5.test.csv
python3 client.py --model ../models/latino3/output_graph.pb --scorer ../lm/latino3.scorer --src ../files/latino5.test.csv --csv > ../logs/latino5.test.log

Instalacion de docker y docker compose
https://confluence.mitrol.net/pages/viewpage.action?pageId=44990770

Instalacion de Botfarm:
https://confluence.mitrol.net/pages/viewpage.action?pageId=35145232

https://eugenio.voss@bitbucket.mitrol.net/scm/mitct/dashboardmanager.git
https://eugenio.voss@bitbucket.mitrol.net/scm/mitct/admin-bot-trainer.git