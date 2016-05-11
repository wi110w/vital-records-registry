from django.views import generic

from vital_records.models import BirthNote


class IndexView(generic.ListView):
    template_name = 'vital_records/birth/index.html'
    context_object_name = 'note_list'
    model = BirthNote


class DetailView(generic.DetailView):
    template_name = 'vital_records/birth/detail.html'
    context_object_name = 'note'
    model = BirthNote
