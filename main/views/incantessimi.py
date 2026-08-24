

from django.views.generic import TemplateView, DetailView
from main.models.incantessimi import Incantessimo
#
# class SpellView(TemplateView):
#    model = Spell
#
#     def head(self, *args, **kwargs):
#         last_book = self.get_queryset().latest("publication_date")
#         response = HttpResponse(
#             # RFC 1123 date format.
#             headers={
#                 "Last-Modified": last_book.publication_date.strftime(
#                     "%a, %d %b %Y %H:%M:%S GMT"
#                 )
#             },
#         )
#         return response

class IncantessimoDetailView(DetailView):
    model = Incantessimo
    context_object_name = 'i'
    slug_field = 'rid'
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True
