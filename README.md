# Это API сайта для системы опросов пользователей

Функционал для администратора системы (доступен через админку):

- авторизация в системе (регистрация не нужна)
- добавление/изменение/удаление опросов. Атрибуты опроса: название, дата старта, дата окончания, описание. После создания поле "дата старта" у опроса менять нельзя.
- добавление/изменение/удаление вопросов в опросе. Атрибуты вопросов: текст вопроса, тип вопроса (ответ текстом, ответ с выбором одного варианта, ответ с выбором нескольких вариантов).

Функционал для пользователей системы (доступен через API):

- получение списка активных опросов.
- прохождение опроса: опросы можно проходить анонимно, в качестве идентификатора пользователя в API передаётся числовой ID, по которому сохраняются ответы пользователя на вопросы; один пользователь может участвовать в любом количестве опросов.
- получение пройденных пользователем опросов с детализацией по ответам (что выбрано) по уникальному ID пользователя.


## Как запустить dev-версию сайта

Для запуска сайта нужно запустить бэкенд в терминале.

### Как собрать бэкенд

Скачайте код:
```sh
git clone https://github.com/AmatorAVG/FabrikaPoll.git
```

Перейдите в каталог проекта:
```sh
cd FabrikaPoll
```

[Установите Python](https://www.python.org/), если этого ещё не сделали.

Проверьте, что `python` установлен и корректно настроен. Запустите его в командной строке:
```sh
python --version
```
**Важно!** Версия Python должна быть не ниже 3.6.

Возможно, вместо команды `python` здесь и в остальных инструкциях этого README придётся использовать `python3`. Зависит это от операционной системы и от того, установлен ли у вас Python старой второй версии.

В каталоге проекта создайте виртуальное окружение:
```sh
python -m venv venv
```
Активируйте его. На разных операционных системах это делается разными командами:
- Windows: `.\venv\Scripts\activate`
- MacOS/Linux: `source venv/bin/activate`


Установите зависимости в виртуальное окружение:
```sh
pip install -r requirements.txt
```

Создайте файл базы данных и отмигрируйте её следующей командой:

```sh
python manage.py migrate
```

Запустите сервер:

```sh
python manage.py runserver
```

Откройте сайт в браузере по адресу [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

Вы должны увидеть страницу с описанием API Swagger:

````sh
GET
/active_surveys

Получение списка активных опросов

        Пример ответа:
        [
          {
            "id": 1,
            "start_at": "2022-01-15T09:30:03Z",
            "finish_at": "2022-01-19T09:30:08Z",
            "title": "Опрос о географии",
            "description": "Давайте побеседуем об этой науке...",
            "question": [
              {
                "id": 1,
                "type": "T",
                "text": "Что вы думаете о географии?"
              },
              {
                "id": 2,
                "type": "S",
                "text": "Какая самая длинная река в мире?",
                "options": [
                  {
                    "id": 9,
                    "option": "Амазонка"
                  },
                  {
                    "id": 8,
                    "option": "Нил"
                  },
                  {
                    "id": 7,
                    "option": "Обь"
                  }
                ]
              },
              {
                "id": 3,
                "type": "P",
                "text": "Какие из этих стран находятся в Европе?",
                "options": []
              },
              {
                "id": 4,
                "type": "P",
                "text": "На каких континентах обитают львы?",
                "options": [
                  {
                    "id": 3,
                    "option": "Австралия"
                  },
                  {
                    "id": 4,
                    "option": "Антарктида"
                  },
                  {
                    "id": 2,
                    "option": "Африка"
                  },
                  {
                    "id": 1,
                    "option": "Евразия"
                  },
                  {
                    "id": 10,
                    "option": "Океания"
                  },
                  {
                    "id": 5,
                    "option": "Северная америка"
                  },
                  {
                    "id": 6,
                    "option": "Южная америка"
                  }
                ]
              }
            ]
          },
          {
            "id": 2,
            "start_at": "2022-01-16T03:40:55Z",
            "finish_at": "2022-01-19T03:40:57Z",
            "title": "Опрос по истории",
            "description": "Как хорошо вы знаете историю...",
            "question": [
              {
                "id": 5,
                "type": "T",
                "text": "Кто такой был Юлий Цезарь?"
              },
              {
                "id": 6,
                "type": "S",
                "text": "В каком году была Грюнвальдская битва?",
                "options": [
                  {
                    "id": 12,
                    "option": "1380"
                  },
                  {
                    "id": 11,
                    "option": "1410"
                  },
                  {
                    "id": 13,
                    "option": "1560"
                  }
                ]
              },
              {
                "id": 7,
                "type": "P",
                "text": "Какие из этих стран воевали в столетней войне?",
                "options": [
                  {
                    "id": 17,
                    "option": "Австрия"
                  },
                  {
                    "id": 14,
                    "option": "Германия"
                  },
                  {
                    "id": 16,
                    "option": "Россия"
                  },
                  {
                    "id": 15,
                    "option": "Франция"
                  }
                ]
              },
              {
                "id": 9,
                "type": "T",
                "text": "Кто такой Наполеон?"
              }
            ]
          }
        ]
        
        
POST
answer

Прохождение опроса: в качестве идентификатора пользователя в API передаётся числовой ID, по которому сохраняются ответы пользователя на вопросы

                  Пример запроса:
                  {
                    "question": 2,
                    "author": 3,
                    "text": "",
                    "answers": [
                    {
                        "option": 4
                    },
                    {
                        "option": 5
                    }
                            ]
                  }

                  Еще пример:
                  {
                    "question": 1,
                    "author": 3,
                    "text": "Волга впадает в Каспийское море"
                  }
                  

GET
answers/{author}

Получение пройденных пользователем опросов с детализацией по ответам (что выбрано) по уникальному ID пользователя

                Пример ответа:
                [
                  {
                    "id": 1,
                    "survey": "Опрос о географии",
                    "survey_id": 1,
                    "question": "Какая самая длинная река в мире?",
                    "question_id": 2,
                    "options": [
                      {
                        "id": 4,
                        "option": "Амазонка"
                      }
                    ]
                  },
                  {
                    "id": 3,
                    "survey": "Опрос о географии",
                    "survey_id": 1,
                    "question": "На каких континентах обитают львы?",
                    "question_id": 4,
                    "options": [
                      {
                        "id": 1,
                        "option": "Евразия"
                      },
                      {
                        "id": 2,
                        "option": "Африка"
                      }
                    ]
                  },
                  {
                    "id": 4,
                    "survey": "Опрос о географии",
                    "survey_id": 1,
                    "question": "Что вы думаете о географии?",
                    "question_id": 1,
                    "text": "Мой любимый предмет!"
                  }
                ]
````

Cоздайте файл `.env` в каталоге проекта со следующими настройками:

- `DEBUG` — дебаг-режим. Поставьте `True`.
- `SECRET_KEY` — секретный ключ проекта. Он отвечает за шифрование на сайте. Например, им зашифрованы все пароли на вашем сайте. Не стоит использовать значение по-умолчанию, **замените на своё**.
- `ALLOWED_HOSTS` — [см. документацию Django](https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts).


## Цели проекта

Код написан в качестве реализации тестового задания для прохождения интервью.
