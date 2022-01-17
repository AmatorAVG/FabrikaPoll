from django.db import models
from django.core.exceptions import ValidationError


class Survey(models.Model):
    title = models.CharField('название', max_length=200)
    start_at = models.DateTimeField('дата старта', blank=False)
    finish_at = models.DateTimeField('дата окончания', blank=False)
    description = models.TextField('описание')

    objects = models.Manager()

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'

    def __str__(self):
        return f"{self.title} {self.start_at} - {self.finish_at}"

    def save(self, *args, **kwargs):
        if self.finish_at < self.start_at:
            raise ValidationError("Дата окончания должна быть больше даты старта!")
        super().save(*args, **kwargs)


class Question(models.Model):
    TYPES = (
        ('T', 'Ответ текстом'),
        ('S', 'Ответ с выбором одного варианта'),
        ('P', 'Ответ с выбором нескольких вариантов'),
    )

    type = models.CharField(max_length=2, choices=TYPES, default='T', db_index=True)
    text = models.CharField(max_length=200)
    survey = models.ForeignKey(
        Survey,
        related_name='questions',
        verbose_name="опрос",
        on_delete=models.CASCADE,
    )
    objects = models.Manager()

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.text


class AnswerOptions(models.Model):
    question = models.ForeignKey(
        Question,
        related_name='answer_options',
        verbose_name="вопрос",
        on_delete=models.CASCADE,
    )
    option = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'вариант ответа'
        verbose_name_plural = 'варианты ответа'
        unique_together = [
            ['question', 'option']
        ]

    def __str__(self):
        return f"{self.question.text} - {self.option}"


class Answer(models.Model):
    text = models.TextField(blank=True)
    author = models.IntegerField('ID пользователя', help_text="Уникальный ID пользователя")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return f"{self.author} - {self.text}"


class AnswerItem(models.Model):
    answer = models.ForeignKey(
        Answer,
        related_name='answer_items',
        verbose_name="Ответ",
        on_delete=models.CASCADE,
    )
    option = models.ForeignKey(
        AnswerOptions,
        on_delete=models.CASCADE,
        related_name='answer_options',
        verbose_name='вариант ответа',
    )

    class Meta:
        verbose_name = 'выбранный вариант ответа'
        verbose_name_plural = 'выбранные варианты ответа'
        unique_together = [
            ['answer', 'option']
        ]

    def __str__(self):
        return f"{self.answer} - {self.option}"
