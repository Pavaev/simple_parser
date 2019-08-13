from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.text import Truncator
from django.views.generic import ListView
from django.views.generic.edit import FormView

from .constants import EmbeddedMetadataTypes
from .forms import BookmarkForm


class IndexView(ListView):
    """
    Bookmarks listing view
    """
    template_name = 'index.html'
    paginate_by = 5

    context_object_name = 'bookmarks'

    def get_queryset(self):
        return self.request.user.bookmarks.select_related(
            'embedded_metadata',
        ).order_by('-date_created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_bookmark_form'] = BookmarkForm()
        context['parser'] = EmbeddedMetadataTypes(getattr(settings, 'DEFAULT_PARSER', EmbeddedMetadataTypes.DEFAULT)).label
        return context


class CreateBookmarkView(FormView):
    """
    Bookmarks creation view
    """
    form_class = BookmarkForm
    template_name = 'bookmark_form.html'

    def get_success_url(self):
        return reverse('index')

    def get(self, request, *args, **kwargs):
        return redirect(reverse('index'))

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['context'] = {'user': self.request.user}
        return kwargs

    def form_valid(self, form):
        bookmark = form.save(commit=False)
        bookmark.user = self.request.user
        bookmark.save()
        messages.success(
            self.request,
            'URL "{}" успешно добавлен. Результат парсинга будет доступен '
            'после обновления страницы.'.format(Truncator(bookmark.url).chars(45)),
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors['url'][0])
        return redirect(reverse('index'),  self.get_context_data())


index = IndexView.as_view()
create_bookmark = CreateBookmarkView.as_view()
