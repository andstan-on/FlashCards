from django.shortcuts import get_object_or_404, redirect, render
from .models import Deck, Card

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .forms import CardForm




# Create your views here.
def index(request):
    """View function for home page of site."""

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    context = {
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context)


from .forms import CustomUserCreationForm

def registerPage(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    context = {'form': form}
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'register.html', context)


class CustomLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

class DeckListView(LoginRequiredMixin, ListView):
    model = Deck
    template_name = 'deck_list.html'
    context_object_name = 'decks'
    ordering = ['name']
    paginate_by = 10

    def get_queryset(self):
        return Deck.objects.filter(owner=self.request.user)

class DeckDetailView(LoginRequiredMixin, DetailView):
    model = Deck
    template_name = 'deck_detail.html'
    context_object_name = 'deck'

class DeckCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Deck
    template_name = 'deck_form.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('decks')
    success_message = 'Deck was created successfully.'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class DeckUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Deck
    template_name = 'deck_form.html'
    fields = ['name', 'description']
    success_message = 'Deck was updated successfully.'

class DeckDeleteView(LoginRequiredMixin, DeleteView):
    model = Deck
    template_name = 'deck_confirm_delete.html'
    success_url = reverse_lazy('decks')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['confirm_delete'] = True  # add a flag to context
        return context

class DeckConfirmDeleteView(LoginRequiredMixin, DeleteView):
    model = Deck
    template_name = 'deck_confirm_delete.html'
    success_url = reverse_lazy('decks')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Deck was deleted successfully.')
        return super().delete(request, *args, **kwargs)



class CardCreateView(CreateView):
    model = Card
    fields = ['question', 'answer']
    template_name = 'card_form.html'

    def form_valid(self, form):
        deck = get_object_or_404(Deck, pk=self.kwargs['deck_pk'])
        form.instance.deck = deck
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('card_detail', args=[self.kwargs['deck_pk'], self.object.pk])


class CardDetailView(DetailView):
    model = Card
    template_name = 'card_detail.html'
    success_url = reverse_lazy('card_detail')

class CardUpdateView(UpdateView):
    model = Card
    fields = ['question', 'answer']
    template_name = 'card_form.html'
    def get_success_url(self):
        deck_pk = self.kwargs['deck_pk']
        return reverse_lazy('deck_detail', kwargs={'pk': deck_pk})

class CardDeleteView(LoginRequiredMixin, DeleteView):
    model = Card
    template_name = 'card_confirm_delete.html'

    def get_success_url(self):
        deck_pk = self.kwargs['deck_pk']
        return reverse_lazy('deck_detail', kwargs={'pk': deck_pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['confirm_delete'] = True  # add a flag to context
        return context

class CardConfirmDeleteView(LoginRequiredMixin, DeleteView):
    model = Card
    template_name = 'card_confirm_delete.html'

    def get_success_url(self):
        deck_pk = self.kwargs['deck_pk']
        return reverse_lazy('deck_detail', kwargs={'pk': deck_pk})

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Card was deleted successfully.')
        return super().delete(request, *args, **kwargs)