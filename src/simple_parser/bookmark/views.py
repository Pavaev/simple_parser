from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'

    # def get_context_data(self, **kwargs):
    #     cntx = super().get_context_data()
    #     return cntx


index = IndexView.as_view()
