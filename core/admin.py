from django.contrib import admin
from .models import Survey
from .models import Question
from .models import AnswerOptions
from .models import Answer
from .models import AnswerItem


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    search_fields = [
        'title',
    ]

    list_display = [
        'title',
        'start_at',
        'finish_at',
    ]
    inlines = [
        QuestionInline
    ]

    def get_readonly_fields(self, request, obj=None):
        if obj:  # when editing an object
            return ['start_at']
        return self.readonly_fields


class AnswerOptionsInline(admin.TabularInline):
    model = AnswerOptions
    extra = 0

    def get_max_num(self, request, obj=None, **kwargs):
        return 0 if obj and obj.type == 'T' else None


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    search_fields = [
        'type',
    ]
    list_filter = ['type']

    list_display = [
        'text',
        'type',
        'survey',
    ]
    inlines = [
        AnswerOptionsInline
    ]


class AnswerItemInline(admin.TabularInline):
    model = AnswerItem
    extra = 0


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    search_fields = [
        'text',
    ]

    list_filter = ['author']

    list_display = [
        'text',
        'author',
        'question',
    ]
    inlines = [
        AnswerItemInline
    ]
