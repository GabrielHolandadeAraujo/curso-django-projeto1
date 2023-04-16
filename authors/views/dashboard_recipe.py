from authors.forms.recipe_form import AuthorRecipeForm
from django.contrib import messages
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from recipes.models import Recipe

class DashboardRecipe(View):
    def get_recipe(self, id=None):
       recipe = None
       # verificamos se o id da receita existe filtrando se está publicado, se o author é o msm que está logado
       # e se o id é igual a chave primária. Como o filter retorna uma lista de valores encontrados, usamos
       # o .first() para retornar apenas o primeirpo valor encontrado, outra opção é usar o get que se retorna
       # um valor, mas levanta erro se não econtrar.
       if id is not None:
        recipe = Recipe.objects.filter(
           is_published=False,
           author=self.request.user,
           pk=id,
        ).first()
        # se a receita não existir da um 404
        if not recipe:
            raise Http404()
        
        return recipe
    # essa função é para rendereizar o formulário, criada aqui para evitar repetição desse trecho de código
    def render_recipe(self, form):
        return render(
           self.request,
           'authors/pages/dashboard_recipe.html',
           context={
                'form': form 
           }
        )
    
    def get(self, request, id=None):
        recipe = self.get_recipe(id)
        # esse instance é pora o form saber qual instância renderizar
        form = AuthorRecipeForm(instance=recipe)
        return self.render_recipe(form)

    def post(self, request, id=None):
        recipe = self.get_recipe(id)
        # instaciamos a classe de forms do authors podendo passar a requisição (caso o filtro acima encontre o elemento)
        # ou None, caso a receita ainda não exista. Depois instaciamos na própria variável acima (do filtro), caso ela exista
        # isso é para atualizar caso já exista ou criar caso não exista.
        form = AuthorRecipeForm(
            data=request.POST or None,
            # para receber uma mídia ou não
            files=request.FILES or None,
            instance=recipe
        )

        if form.is_valid():
            # Agora, o form é válido e eu posso tentar salvar, fingimos salvar para faze algumas manipulações
            recipe = form.save(commit=False)
            # garantimos que esses campos serão salvos com os dados abaixo como medida de segurança adicional
            recipe.author = request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False

            recipe.save()

            messages.success(request, 'Sua receita foi salva com sucesso!')
            return redirect(
                reverse(
                'authors:dashboard_recipe_edit', args=(
                    recipe.id,
                    )
                )
            )

        return self.render_recipe(form)