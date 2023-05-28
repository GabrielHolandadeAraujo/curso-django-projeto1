from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from collections import defaultdict
from django.forms import ValidationError
# from django.contrib.contenttypes.fields import GenericRelation
from tag.models import Tag

class Category(models.Model):
    name = models.CharField(max_length=65)
    
    def __str__(self):
        return self.name
    # podemos criar essa função get_absolute_url para renderizar urls no sie de forma mais simples, basicamente
    # a url da view e com args ou kwargs passamos parâmetros adicionais das páginas, no exemplo abaixzo passamos 
    # o id de uma receita
    def get_absolute_url(self):
        return reverse("recipes:recipe", args=(self.id,))  
    # podemos sobrescrever algumas funções padrões como o save para se comportar de maneira vantajosa
    def save(self, *args, **kwargs):
        # nesse caso podemos fazer o gerador de slug a partir do título
        if not self.slug:
            slug = f'{slugify(self.title)}'
            self.slug = slug
        # sempre temos que retornar a função sobrescrita chamando a super classe
        return super().save(*args, **kwargs)
    


class Recipe(models.Model):
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=65)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to='recipes/covers/%Y/%m/%d/', blank=True, default='')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        default=None,
    )
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )

    # tags = GenericRelation(Tag, related_query_name='recipes')
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipes:recipe', args=(self.id,))

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.title)}'
            self.slug = slug

        return super().save(*args, **kwargs)

    def clean(self, *args, **kwargs):
        error_messages = defaultdict(list)

        recipe_from_db = Recipe.objects.filter(
            title__iexact=self.title
        ).first()

        if recipe_from_db:
            if recipe_from_db.pk != self.pk:
                error_messages['title'].append(
                    'Found recipes with the same title'
                )

        if error_messages:
            raise ValidationError(error_messages)