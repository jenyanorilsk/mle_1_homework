
# Лабораторная работа 1

## Задание

**Вариант 11:** https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset

**Цель работы**:

Получить навыки разработки CI/CD pipeline для ML моделей с достижением метрик моделей и качества.

**Ход работы**:

1. - [X] Создать репозитории модели на GitHub, регулярно проводить commit + push в ветку разработки, важна история коммитов;
2. - [X] Провести подготовку данных для набора данных, согласно варианту задания;
3. - [X] Разработать ML модель с ЛЮБЫМ классическим алгоритмом классификации, кластеризации, регрессии и т. д.;
4. - [X] Конвертировать модель из *.ipynb в .py скрипты;
5. - [ ] Покрыть код тестами, используя любой фреймворк/библиотеку;
6. - [X] Задействовать DVC;
7. - [ ] Использовать Docker для создания docker image.
8. - [ ] Наполнить дистрибутив конфигурационными файлами:
    - - [X] config.ini: гиперпараметры модели;
    - - [ ] Dockerfile и docker-compose.yml: конфигурация создания контейнера и образа модели;
    - - [X] requirements.txt: используемые зависимости (библиотеки) и их версии;
    - - [ ] dev_sec_ops.yml: подписи docker образа, хэш последних 5 коммитов в репозитории модели, степень покрытия тестами;
    - - [ ] scenario.json: сценарии тестирования запущенного контейнера модели.
9. - [ ] Создать CI pipeline (Jenkins, Team City, Circle CI и др.) для сборки docker image и отправки его на DockerHub, сборка должна автоматически стартовать по pull request в основную ветку репозитория модели;
10. - [ ] Создать CD pipeline для запуска контейнера и проведения функционального тестирования по сценарию, запуск должен стартовать по требованию или расписанию или как вызов с последнего этапа CI pipeline;
11. - [ ] Результаты функционального тестирования и скрипты конфигурации CI/CD pipeline приложить к отчёту.

**Результаты работы**:

1. Отчёт о проделанной работе;
2. Ссылка на репозиторий GitHub;
3. Ссылка на docker image в DockerHub;
4. Актуальный дистрибутив модели в zip архиве.

Обязательно обернуть модель в контейнер (этап CI) и запустить тесты внутри контейнера (этап CD).

**Дополнительно** – настроить веб сервер в отдельном контейнере (Apache/nginx + Flask/Django) для обработки запросов к модели в режиме реального времени.

Выполнение дополнительного условия гарантирует четверть количества баллов за контрольный семинар, достаточного для оценки "отлично".
Таким образом, выполнение дополнительного задания для каждой работы (их 4) даст автоматически оценку "отлично" за курс.

---

## Комментарии к решению

### DVC

Добавлен DVC этап для препроцессинга и отслеживания изменений в коде препроцессинга и данных.
Команда для добавления отслеживания зависимостей:

``
dvc run -n preprocess -f -d src/preprocess.py -d data/spam.csv -o data/spam_X.csv -o data/spam_y.csv -o data/train/spam_X.csv -o data/train/spam_y.csv -o data/test/spam_X.csv -o data/test/spam_y.csv "python src/preprocess.py"
``

Мы устанавливаем зависимость данных от кода препроцессинга, исходных данных.

Можно было бы добавить и конфигурационный файл, но он переписывается при обучении модели, поэтому нет смысла этого делать в данном решении.

Можно было разбить на большее число шагов и зависимостей, чтобы выстроить конвеер, опираясь на примеры из [документации](https://dvc.org/doc/command-reference/run) и [статьи](https://habr.com/ru/company/raiffeisenbank/blog/461803/), но я не стал усложнять этот пример.

### Unit-Test

```
(mle) Z:\# MIPT\MLE\mle_1_homework>python src\unit_tests\test_preprocess.py -v
test_get_data (__main__.TestDataMaker) ... 2022-10-21 16:48:06,090 — preprocess — INFO — DataMaker is ready
2022-10-21 16:48:06,138 — preprocess — INFO — X and y data are ready
ok
test_save_splitted_data (__main__.TestDataMaker) ... 2022-10-21 16:48:06,140 — preprocess — INFO — DataMaker is ready
2022-10-21 16:48:06,140 — preprocess — INFO — DataMaker is ready
2022-10-21 16:48:06,210 — preprocess — INFO — Z:\# MIPT\MLE\mle_1_homework\data\spam_X.csv is saved
2022-10-21 16:48:06,210 — preprocess — INFO — Z:\# MIPT\MLE\mle_1_homework\data\spam_X.csv is saved
ok
test_split_data (__main__.TestDataMaker) ... 2022-10-21 16:48:06,211 — preprocess — INFO — DataMaker is ready
2022-10-21 16:48:06,351 — preprocess — INFO — Z:\# MIPT\MLE\mle_1_homework\data\test\spam_y.csv is saved
2022-10-21 16:48:06,351 — preprocess — INFO — Z:\# MIPT\MLE\mle_1_homework\data\test\spam_y.csv is saved
2022-10-21 16:48:06,351 — preprocess — INFO — Z:\# MIPT\MLE\mle_1_homework\data\test\spam_y.csv is saved
2022-10-21 16:48:06,352 — preprocess — INFO — Train and test data are ready
2022-10-21 16:48:06,352 — preprocess — INFO — Train and test data are ready
2022-10-21 16:48:06,352 — preprocess — INFO — Train and test data are ready
ok

----------------------------------------------------------------------
Ran 3 tests in 0.265s

OK
```

```
(mle) Z:\# MIPT\MLE\mle_1_homework>python src\unit_tests\test_train.py -v      
test_train_model (__main__.TestTrain) ... 2022-10-21 16:48:45,708 — train — INFO — SpamClassifier is ready
2022-10-21 16:48:45,809 — train — INFO — Z:\# MIPT\MLE\mle_1_homework\experiments\model.sav is saved
ok

----------------------------------------------------------------------
Ran 1 test in 0.121s

OK
```

```
(mle) Z:\# MIPT\MLE\mle_1_homework>python src\unit_tests\test_predict.py -v
test_predict (__main__.TestPredict) ... 2022-10-21 16:51:53,399 — predict — INFO — Predictor is ready
ok

----------------------------------------------------------------------
Ran 1 test in 0.013s

OK
```