from django.shortcuts import render
from ListBoard.models import Worklist
from django.views.generic import ListView,CreateView, DetailView, UpdateView , DeleteView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
import request

# Create your views here.

class WorkListListView(ListView):
    model = Worklist
    paginate_by = 20
    ordering = ['id']

    def get_context_data(self, **kwargs):
        context = super(WorkListListView, self).get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5  # Display only 5 page numbers
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        return context

class WorkListCreate(CreateView):
    model = Worklist
    fields = ['유형','명칭','nid','lcode','준공일','구축시한','실사구분','poi구분','poi구축일','net구분','net구축일','map구분','map구축일','데이터확인','서비스확인','자료정보']
    success_url = reverse_lazy('index')

class WorkListDetail(DetailView):
    medel = Worklist

class WorkListUpdate(UpdateView):
    model = Worklist
    fields = ['유형','명칭','nid','lcode','준공일','구축시한','실사구분','poi구분','poi구축일','net구분','net구축일','map구분','map구축일','데이터확인','서비스확인','자료정보']
    success_url = reverse_lazy('index')

class WorkListDelete(DeleteView):
    model = Worklist
    success_url = reverse_lazy('index')




