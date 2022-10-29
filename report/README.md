
# Отчёт о выполнении работы

## Ссылки

Мне достался (https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset)[Вариант 11] - классификация спама

Ссылка на репозиторий GitHub - [https://github.com/jenyanorilsk/mle_1_homework](https://github.com/jenyanorilsk/mle_1_homework)

Ссылка на docker image в DockerHub - [https://hub.docker.com/repository/docker/jenyanorilsk/mle_lab](https://hub.docker.com/repository/docker/jenyanorilsk/mle_lab)

## Основная часть:

### DVC

Добавлен DVC этап для препроцессинга и отслеживания изменений в коде препроцессинга и данных.
Команда для добавления отслеживания зависимостей:

``
dvc run -n preprocess -f -d src/preprocess.py -d data/spam.csv -o data/spam_X.csv -o data/spam_y.csv -o data/train/spam_X.csv -o data/train/spam_y.csv -o data/test/spam_X.csv -o data/test/spam_y.csv "python src/preprocess.py"
``

Мы устанавливаем зависимость данных от кода препроцессинга, исходных данных.

Можно было бы добавить и конфигурационный файл, но он переписывается при обучении модели, поэтому нет смысла этого делать в данном решении.

Можно было разбить на большее число шагов и зависимостей, чтобы выстроить конвеер, опираясь на примеры из [документации](https://dvc.org/doc/command-reference/run) и [статьи](https://habr.com/ru/company/raiffeisenbank/blog/461803/), но я не стал усложнять этот пример.

### Тестирование

Вывод команды тестирования при запуске из консоли:

```
coverage run -a src\unit_tests\test_preprocess.py && coverage run -a src\unit_tests\test_train.py && coverage run -a src\unit_tests\test_predict.py
```

```
2022-10-21 23:41:04,271 — preprocess — INFO — DataMaker is ready
2022-10-21 23:41:04,325 — preprocess — INFO — X and y data are ready
.2022-10-21 23:41:04,326 — preprocess — INFO — DataMaker is ready
2022-10-21 23:41:04,326 — preprocess — INFO — DataMaker is ready
2022-10-21 23:41:04,369 — preprocess — INFO — Z:\# MIPT\MLE\mle_1_homework\data\spam_X.csv is saved
2022-10-21 23:41:04,369 — preprocess — INFO — Z:\# MIPT\MLE\mle_1_homework\data\spam_X.csv is saved
.2022-10-21 23:41:04,370 — preprocess — INFO — DataMaker is ready
2022-10-21 23:41:04,370 — preprocess — INFO — DataMaker is ready
2022-10-21 23:41:04,370 — preprocess — INFO — DataMaker is ready
2022-10-21 23:41:04,418 — preprocess — INFO — X and y data are ready
2022-10-21 23:41:04,418 — preprocess — INFO — X and y data are ready
2022-10-21 23:41:04,418 — preprocess — INFO — X and y data are ready
2022-10-21 23:41:04,473 — preprocess — INFO — Z:\# MIPT\MLE\mle_1_homework\data\train\spam_X.csv is saved
2022-10-21 23:41:04,473 — preprocess — INFO — Z:\# MIPT\MLE\mle_1_homework\data\train\spam_X.csv is saved
2022-10-21 23:41:04,473 — preprocess — INFO — Z:\# MIPT\MLE\mle_1_homework\data\train\spam_X.csv is saved
2022-10-21 23:41:04,483 — preprocess — INFO — Z:\# MIPT\MLE\mle_1_homework\data\train\spam_y.csv is saved
2022-10-21 23:41:04,483 — preprocess — INFO — Z:\# MIPT\MLE\mle_1_homework\data\train\spam_y.csv is saved
2022-10-21 23:41:04,483 — preprocess — INFO — Z:\# MIPT\MLE\mle_1_homework\data\train\spam_y.csv is saved
2022-10-21 23:41:04,490 — preprocess — INFO — Z:\# MIPT\MLE\mle_1_homework\data\test\spam_X.csv is saved
2022-10-21 23:41:04,490 — preprocess — INFO — Z:\# MIPT\MLE\mle_1_homework\data\test\spam_X.csv is saved
2022-10-21 23:41:04,490 — preprocess — INFO — Z:\# MIPT\MLE\mle_1_homework\data\test\spam_X.csv is saved
2022-10-21 23:41:04,494 — preprocess — INFO — Z:\# MIPT\MLE\mle_1_homework\data\test\spam_y.csv is saved
2022-10-21 23:41:04,494 — preprocess — INFO — Z:\# MIPT\MLE\mle_1_homework\data\test\spam_y.csv is saved
2022-10-21 23:41:04,494 — preprocess — INFO — Z:\# MIPT\MLE\mle_1_homework\data\test\spam_y.csv is saved
2022-10-21 23:41:04,495 — preprocess — INFO — Train and test data are ready
2022-10-21 23:41:04,495 — preprocess — INFO — Train and test data are ready
2022-10-21 23:41:04,495 — preprocess — INFO — Train and test data are ready
.
----------------------------------------------------------------------
Ran 3 tests in 0.226s

OK
2022-10-21 23:41:06,925 — train — INFO — SpamClassifier is ready
2022-10-21 23:41:07,074 — train — INFO — Z:\# MIPT\MLE\mle_1_homework\experiments\model.sav is saved
.
----------------------------------------------------------------------
Ran 1 test in 0.177s

OK
2022-10-21 23:41:09,508 — predict — INFO — Predictor is ready
.
----------------------------------------------------------------------
Ran 1 test in 0.016s

OK
```

### Docker

Актуальные подробности по использованию Docker можно посмотреть в CI логах.

Результат сборки образа в консоли:

```
docker-compose build
```

```
[+] Building 113.5s (9/9) FINISHED
 => [internal] load build definition from Dockerfile
 => => transferring dockerfile: 152B
 => [internal] load .dockerignore
 => => transferring context: 2B
 => [internal] load metadata for docker.io/library/python:3.8-slim
 => [1/4] FROM docker.io/library/python:3.8-slim
 => [internal] load build context
 => => transferring context: 5.13MB
 => CACHED [2/4] WORKDIR /app
 => => exporting layers
 => => writing image sha256:d340d0e7d562ca5a31b4a59a715409aa9f43f5eebddc0b190f563f63109a6570
 => => naming to docker.io/jenyanorilsk/mle_lab:latest

 Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them
```

Попытка запушить образ в докерхаб:

```
docker login
```

```
Authenticating with existing credentials...
Login Succeeded

Logging in with your password grants your terminal complete access to your account.
For better security, log in with a limited-privilege personal access token. Learn more at https://docs.docker.com/go/access-tokens/
```

```
docker push jenyanorilsk/mle_lab
```

```
Using default tag: latest
The push refers to repository [docker.io/jenyanorilsk/mle_lab]
ca5c83166276: Pushed
95a5b306034e: Pushed
0048ef11e61d: Pushed
4531003f44fb: Pushed
2a5f58dab527: Pushed
e4adf276765a: Pushed
4cd6d007fbd6: Pushed
608f3a074261: Pushed
latest: digest: sha256:49bb83ab0f25761f5e76941df115bc52a5ba531b17b167369ab3a7bbbbb73404 size: 2001
```

После этого образ появляется на сайте, что можно проверить, пройдя [по ссылке](https://hub.docker.com/repository/docker/jenyanorilsk/mle_lab)

В целом далее, в логе CI будет видно как происходит Push в DockerHub на соответствующем шаге.


## Дополнительная часть:

Запустить web-приложение можно с помощью команды

```
docker compose -f ./docker-compose-web.yml up -d
```

Это запустит уже собранный контейнер, с последующим препроцессингом, обучением модели и запуском flask при каждом перезапуске.

В самом файле docker-compose-web.yml описан альтернативный вариант, когда препроцессинг и обучение происходят на этапе сборки за счёт использования Dockerfile из папки web.

![running in docker desktop](/report/web-container-1.png)

![browsing runing service](/report/web-container-2.png)

![and using it](/report/web-container-3.png)


