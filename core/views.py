from .models import Survey, Answer, AnswerItem, Question, AnswerOptions
from rest_framework.serializers import ModelSerializer
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
import datetime
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class AnswerItemsSerializer(ModelSerializer):
    class Meta:
        model = AnswerItem
        fields = ['option']


class AnswerSerializer(ModelSerializer):
    answers = AnswerItemsSerializer(many=True, allow_empty=False, write_only=True, required=False)

    class Meta:
        model = Answer
        fields = ['id', 'text', 'author', 'question', 'answers']


@swagger_auto_schema(method='get', operation_description="""Получение списка активных опросов

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
""")
@api_view(['GET'])
def survey_list_api(request):
    surveys = Survey.objects.filter(start_at__lte=datetime.datetime.now(), finish_at__gte=datetime.datetime.now())

    dumped_surveys = []
    for survey in surveys:
        dumped_survey = {
            'id': survey.id,
            'start_at': survey.start_at,
            'finish_at': survey.finish_at,
            'title': survey.title,
            'description': survey.description,
        }
        questions = Question.objects.filter(survey_id=survey.id)
        dumped_questions = []
        for question in questions:
            dumped_question = {
                'id': question.id,
                'type': question.type,
                'text': question.text,
            }
            if not question.type == 'T':
                answer_options = AnswerOptions.objects.filter(question_id=question.id)
                dumped_options = []
                for answer_option in answer_options:
                    dumped_answer_option = {
                        'id': answer_option.id,
                        'option': answer_option.option,
                    }
                    dumped_options.append(dumped_answer_option)
                dumped_question['options'] = dumped_options
            dumped_questions.append(dumped_question)
        dumped_survey['question'] = dumped_questions
        dumped_surveys.append(dumped_survey)
    return Response(dumped_surveys)


@swagger_auto_schema(method='get',
                     manual_parameters=[openapi.Parameter('author', openapi.IN_PATH, "Уникальный ID пользователя", type=openapi.TYPE_INTEGER)],
                     operation_description="""Получение пройденных пользователем опросов с детализацией по ответам (что выбрано) по уникальному ID пользователя
                     
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
                     """)
@api_view(['GET'])
def answer_list_api(request, author):
    answers = Answer.objects.filter(author=author)

    dumped_answers = []
    for answer in answers:
        dumped_answer = {
            'id': answer.id,
            'survey': answer.question.survey.title,
            'survey_id':answer.question.survey.id,
            'question': answer.question.text,
            'question_id': answer.question.id,
        }
        if answer.question.type == 'T':
            dumped_answer['text'] = answer.text
        else:
            answer_items = AnswerItem.objects.filter(answer_id=answer.id)
            dumped_answer_items = []
            for answer_item in answer_items:
                dumped_answer_item = {
                    'id': answer_item.id,
                    'option': answer_item.option.option,
                }
                dumped_answer_items.append(dumped_answer_item)
            dumped_answer['options'] = dumped_answer_items
        dumped_answers.append(dumped_answer)
    return Response(dumped_answers)


@swagger_auto_schema(method='post',
                     operation_description="""Прохождение опроса: в качестве идентификатора пользователя в API передаётся числовой ID, по которому сохраняются ответы пользователя на вопросы
                        
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
                     """)
@api_view(['POST'])
def register_answer(request):
    serializer = AnswerSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    with transaction.atomic():
        answer = Answer.objects.create(
            text=serializer.validated_data['text'],
            author=serializer.validated_data['author'],
            question=serializer.validated_data['question'],
        )
        if 'answers' in serializer.validated_data:
            answer_items_fields = serializer.validated_data['answers']
            answer_items = [AnswerItem(answer=answer, **fields) for fields in answer_items_fields]
            AnswerItem.objects.bulk_create(answer_items)

    answer_ser = AnswerSerializer(answer)
    return Response(answer_ser.data, status=status.HTTP_201_CREATED)