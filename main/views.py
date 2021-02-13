import logging
import csv
import xlwt
import datetime
from django.shortcuts import render, reverse
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection

from django_filters.views import FilterMixin

from .models import Application
from .forms import ApplicationForm
from .filters import ApplicationFilter


logger = logging.getLogger('django')

# Create your views here.
# FilterMixin - добавляет возможности фильтрации
class ApplicationListView(ListView, FilterMixin):
    model = Application
    template_name = 'main/index.html'
    filterset_class = ApplicationFilter
    
    # Переопределяем метод get, чтобы использовать фильтр
    def get(self, request, *args, **kwargs):    
        self.filterset = self.get_filterset(self.get_filterset_class())

        sort = request.GET.getlist('order')     
        self.object_list = self.filterset.qs.order_by(*sort, 'date')

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
        return reverse('main:index')


class ApplicationDeleteView(DeleteView):
    model = Application

    def dispatch(self, request, *args, **kwargs):
        # Переопределяем метод, чтобы убрать подтверждение удаления
        self.application = self.get_object()
        self.application.delete()

        logger.info('Record deleted')

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('main:index')


class ApplicationCreateView(CreateView):
    form_class = ApplicationForm
    template_name = 'main/application_create.html'

    def form_valid(self, form):
        logger.info('Record created')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('main:index')


# Выгрузка данных в CSV
def exportCSV(request):
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow(['Date', 'Product', 'Phone', 'Solution', 'Comment'])

    for application in Application.objects.all().values_list('date', 
        'product', 'phone', 'solution', 'comment'):
        writer.writerow(application)

    response['Content-Disposition'] = 'attachment; filename="applications.csv"'
    
    return response


# Выгрузка данных в Excel
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


# Колличесво заявок
def count_application(request):
    with connection.cursor() as cursor:
        cursor.execute("select count(id), to_char(date, 'Month') as month from main_application group by month")
        row = dictfetchall(cursor)

    context = {'row': row}
    return render(request, 'main/count_application.html', context)


# Последняя заявка
def last_application(request):
    with connection.cursor() as cursor:
        cursor.execute("select * from main_application as m where date = (select max(date) from main_application as m2 where m.phone = m2.phone)")
        row = dictfetchall(cursor)

    context = {'row': row}
    return render(request, 'main/last_application.html', context)


# Другие продукты клиентов
def another_product(request):
    with connection.cursor() as cursor:
        query = """
        with special as (select * from main_application where solution = 'Одобрено')
        select m.phone, m.product, m.solution from main_application m join special s on m.phone = s.phone and m.product != s.product
        """
        cursor.execute(query)
        row = dictfetchall(cursor)

    context = {'row': row}
    return render(request, 'main/another_product.html', context)


def dictfetchall(cursor):
    # Возвращаем результаты запроса в виде dict
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]