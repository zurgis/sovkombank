import logging
import csv
import xlwt
import datetime
from django.shortcuts import render, reverse
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.http import HttpResponse, HttpResponseRedirect

from django_filters.views import FilterMixin

from .models import Application
from .forms import ApplicationForm
from .filters import ApplicationFilter


logger = logging.getLogger('django')

# Create your views here.

def app(request):
    object_list = Application.objects.order_by('date')
    myfilter = ApplicationFilter(request.GET, queryset=object_list)
    object_list = myfilter.qs
    context = {'object_list': object_list, 'filter': myfilter}
    return render(request, 'main/application_filter.html', context)


class ApplicationListView(ListView, FilterMixin):
    model = Application
    template_name = 'main/main.html'
    filterset_class = ApplicationFilter
        
    def get(self, request, *args, **kwargs):
        self.filterset = self.get_filterset(self.get_filterset_class())
        self.object_list = self.filterset.qs

        context = self.get_context_data(filter=self.filterset, object_list=self.object_list)
        
        return self.render_to_response(context)


class ApplicationUpdateView(UpdateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'main/application_update.html'

    def form_valid(self, form):
        logger.info('Record changed')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('main:main')

    # def dispatch(self, request, *args, **kwargs):
    #     application = self.get_object()
    #     return super().dispatch(request, *args, **kwargs)


class ApplicationDeleteView(DeleteView):
    model = Application

    def dispatch(self, request, *args, **kwargs):
        self.application = self.get_object()
        self.application.delete()

        logger.info('Record deleted')

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('main:main')


class ApplicationCreateView(CreateView):
    form_class = ApplicationForm
    template_name = 'main/application_create.html'

    def form_valid(self, form):
        logger.info('Record created')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('main:main')


def exportCSV(request):
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow(['Date', 'Product', 'Phone', 'Solution', 'Comment'])

    for application in Application.objects.all().values_list('date', 
        'product', 'phone', 'solution', 'comment'):
        writer.writerow(application)

    response['Content-Disposition'] = 'attachment; filename="applications.csv"'
    
    return response


def exportExcel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="applications.xls"'

    wb = xlwt.Workbook()
    ws = wb.add_sheet('Applications')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Date', 'Product', 'Phone', 'Solution', 'Comment']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Application.objects.all().values_list('date', 'product', 'phone', 'solution', 'comment')

    rows = [[i.strftime("%Y-%m-%d %H:%M") if isinstance(i, datetime.datetime) else i for i in row] for row in rows ]

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response