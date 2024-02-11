import datetime





from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from client.forms import AddClientForm, AddCommentForm, AddFileForm
from team.models import Team
from .models import Client

import csv
import xlwt

# Export CSV
@login_required
def clients_csv_export(request):
    clients = Client.objects.filter(created_by=request.user)

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="PopCRM-clients.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow(["Client", "Email", "Description", "Créé le ", "Créé par", "Equipe"])

    for client in clients:
        writer.writerow([client.name, client.email, client.description, client.created_at, client.created_by])

    return response

# Export Xlsx
"""
def export_excel(request):
  response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=PopCRM'+\
        str(datetime.datetime.now())+ '.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('PopCRM')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ["Client", "Email", "Description", "Créé le ", "Créé par", "Equipe"]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    font_style.font.italic =True

    rows = Client.objects.all().values_list('id', 'email', 'description', 'created_at', 'created_by', 'team',)

    for row in rows:
        row_num += 1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)
    wb.save(response)
    return response

    clients = Client.objects.filter(created_by=request.user)

    # create our spreadsheet.  I will create it in memory with a StringIO
    output = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    worksheet.write(["Client", "Email", "Description", "Créé le ", "Créé par", "Equipe"])

    workbook.close()

    # create a response
    response = HttpResponse(content_type='application/vnd.ms-excel')

    # tell the browser what the file is named
    response['Content-Disposition'] = 'attachment;filename="PopCRM-Clients.xlsx"'

    # put the spreadsheet data into the response
    response.write(output.getvalue())

    # return the response
    return response"""

class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "client/clients_list.html"

    # Function
    def get_queryset(self):
        queryset = super(ClientListView, self).get_queryset()
        team = self.request.user.userprofile.active_team
        # converted_to_client = False : Pour faire de sorte qu'une fois converti en client le prospect doit disparaitre de cette liste
        return queryset.filter(created_by=self.request.user,)

class ClientListAllView(LoginRequiredMixin, ListView):
    model = Client
    template_name = "client/clients_list_all.html"

    # Function
    def get_queryset(self):
        team = self.request.user.userprofile.active_team
        queryset = super(ClientListAllView, self).get_queryset()

        return queryset.all()

class ClientCreateView(LoginRequiredMixin,CreateView):
    model = Client
    template_name = "client/add_client.html"
    form_class = AddClientForm
    success_url = reverse_lazy('clients:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.request.user.userprofile.active_team
        context['team'] = team
        context['title'] = 'Ajout client'
        return context

    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        #self.object.team = self.request.user.userprofile.active_team
        self.object.save()
        return redirect(self.get_success_url())

class ClientDetailView(LoginRequiredMixin,DetailView):
    model = Client
    template_name = "client/clients_detail.html"

    # get_context to add an extra data to class based views
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddCommentForm()
        context['fileform'] = AddFileForm()
        return context

    def get_queryset(self):
        queryset = super(ClientDetailView, self).get_queryset()

        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))

class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    template_name = "client/clients_edit.html"
    form_class = AddClientForm

    def get_success_url(self):
        return reverse("leads:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Modification Client'
        return context

    def get_queryset(self):
        queryset = super(ClientUpdateView, self).get_queryset()
        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))

class ClientDeleteView(LoginRequiredMixin,DeleteView):
    model = Client
    success_url = reverse_lazy('clients:list')


    def get_queryset(self):
        queryset = super(ClientDeleteView, self).get_queryset()
        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


@login_required
def clients_add_file(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)

    # --- Add files of client ---
    if request.method == 'POST':
        form = AddFileForm(request.POST, request.FILES)

        if form.is_valid():
            file = form.save(commit=False)
            file.team = request.user.userprofile.active_team
            file.client_id = pk
            file.created_by = request.user
            file.save()

            return redirect('clients:detail', pk=pk)
        return redirect('clients:detail', pk=pk)


@login_required
def clients_detail(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)

    # --- Add comments of client ---
    if request.method == 'POST':
        form = AddCommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.team = request.user.userprofile.active_team
            comment.created_by = request.user
            comment.client = client
            comment.save()

            return redirect('clients:detail', pk=pk)
    else:
        form = AddCommentForm()
    # -------------------------

    context = {
        "client": client,
        "form": form,
        "fileform": AddFileForm(),
    }
    return render(request, "client/clients_detail.html", context)


@login_required
def clients_add(request):
    team = request.user.userprofile.active_team

    if request.method == 'POST':
        form = AddClientForm(request.POST)

        if form.is_valid():
            client = form.save(commit=False)
            client.created_by = request.user
            # Make sure that team is set when creating client
            client.team = team
            client.save()

            messages.success(request, 'Le client a été créé avec succès!')

            return redirect('clients:list')
    else:
        form = AddClientForm()

        context = {
            'form': form,
            'team': team,
        }
    return render(request, "client/add_client.html", context)


@login_required
def clients_edit(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)

    if request.method == 'POST':
        form = AddClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()

            messages.success(request, 'Le client a été modifié avec succès!')

            return redirect('clients:list')
    else:
        form = AddClientForm(instance=client)

        context = {
            "form": form,
            "client": client,

        }
    return render(request, "client/clients_edit.html", context)


@login_required
def clients_delete(request, pk):
    lead = get_object_or_404(Client, created_by=request.user, pk=pk)
    lead.delete()

    messages.success(request, 'Le client a été supprimé avec succès!')

    return redirect('clients:list')

"""
ARCHIVES

@login_required
def clients_list(request):
    clients = Client.objects.filter(created_by=request.user)

    context = {
        "clients": clients,
    }
    return render(request, "client/clients_list.html", context)

"""
