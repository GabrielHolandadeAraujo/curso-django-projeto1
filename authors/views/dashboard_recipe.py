from authors.forms.recipe_form import AuthorRecipeForm
from django.contrib import messages
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from recipes.models import Recipe

class DashboardRecipe(View):
    def get(self, request, id):
        #filtramos a receita não publicadas do usuário pelo id
        recipe = Recipe.objects.filter(
            is_published=False,
            author=request.user,
            pk=id,
            #essa função first é para retornar apenas o primeiro elemento encontrado, pois o filter retorna uma lista 
            # de elementos encontrados. ao invés dessa função, poderiamos usar o get no lugar do filter que retorna só um
            # porém o get gera um erro se não encontrar, isso tornaria o if abaixo obsoleto. Optamos por nós mesmos 
            # conferirmos se o elemento existe
        ).first()
        # se a receita não existir da um 404
        if not recipe:
            raise Http404()
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
            return redirect(reverse('authors:dashboard_recipe_edit', args=(id,)))

        return render(
            request,
            'authors/pages/dashboard_recipe.html',
            context={
                'form': form
            }
        )