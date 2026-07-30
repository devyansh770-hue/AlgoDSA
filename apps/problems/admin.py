from django.contrib import admin
from .models import Topic, Problem, TestCase, Hint


class TestCaseInline(admin.TabularInline):
    model = TestCase
    extra = 2


class HintInline(admin.TabularInline):
    model = Hint
    extra = 3
    max_num = 3


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'order', 'problem_count')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order',)


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'difficulty', 'pattern', 'is_active', 'order')
    list_filter = ('difficulty', 'pattern', 'topic', 'is_active')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [TestCaseInline, HintInline]
    ordering = ('topic', 'order')


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ('problem', 'is_sample', 'order')
    list_filter = ('is_sample', 'problem__topic')


@admin.register(Hint)
class HintAdmin(admin.ModelAdmin):
    list_display = ('problem', 'level')
    list_filter = ('level',)
