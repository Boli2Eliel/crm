import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View

from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.urls import reverse_lazy, reverse

from .forms import AddCommentForm, AddFileForm, AddLeadForm
from client.models import Client, Comment as ClientComment
from lead.models import Lead
from team.models import Team


# ############# FOR STAFF and SUPERUSER ##########################
class LeadListAllView(LoginRequiredMixin, ListView):
    model = Lead
    template_name = "lead/lead_list_all.html"

    # Function
    def get_queryset(self):
        team = self.request.user.userprofile.active_team
        queryset = super(LeadListAllView, self).get_queryset()

        return queryset.filter(converted_to_client=False)


class LeadUpdateAllView(LoginRequiredMixin, UpdateView):
    model = Lead
    template_name = "lead/lead_update_all.html"
    form_class = AddLeadForm

    def get_success_url(self):
        return reverse("leads:list_all")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Modification prospect'
        return context

    def get_queryset(self):
        queryset = super(LeadUpdateAllView, self).get_queryset()
        return queryset.filter(pk=self.kwargs.get('pk'))


class LeadDetailAllView(LoginRequiredMixin, DetailView):
    model = Lead

    # get_context to add an extra data to class based views
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddCommentForm()
        context['fileform'] = AddFileForm()
        context['fileform'] = AddFileForm()
        return context

    def get_queryset(self):
        queryset = super(LeadDetailAllView, self).get_queryset()

        return queryset.filter(pk=self.kwargs.get('pk'))


class LeadDeleteForSuperUserView(LoginRequiredMixin, DeleteView):
    model = Lead
    success_url = reverse_lazy('leads:list_all')

    def get_queryset(self):
        queryset = super(LeadDeleteForSuperUserView, self).get_queryset()
        return queryset.filter(pk=self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


# ############# FOR USER ##########################
class LeadListView(LoginRequiredMixin, ListView):
    model = Lead
    template_name = "lead/lead_list.html"

    # Function
    def get_queryset(self):
        queryset = super(LeadListView, self).get_queryset()

        return queryset.filter(created_by=self.request.user,
                               converted_to_client=False)  # converted_to_client = False : Pour faire de sorte qu'une fois converti en client le prospect doit disparaitre de cette liste


class LeadDetailView(LoginRequiredMixin, DetailView):
    model = Lead

    # get_context to add an extra data to class based views
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddCommentForm()
        context['fileform'] = AddFileForm()
        context['fileform'] = AddFileForm()
        return context

    def get_queryset(self):
        queryset = super(LeadDetailView, self).get_queryset()

        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))


class LeadDeleteView(LoginRequiredMixin, DeleteView):
    model = Lead
    success_url = reverse_lazy('leads:list')

    def get_queryset(self):
        queryset = super(LeadDeleteView, self).get_queryset()
        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class LeadUpdateView(LoginRequiredMixin, UpdateView):
    model = Lead
    template_name = "lead/lead_update.html"
    form_class = AddLeadForm

    def get_success_url(self):
        return reverse("leads:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Modification prospect'
        return context

    def get_queryset(self):
        queryset = super(LeadUpdateView, self).get_queryset()
        return queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))


class LeadCreateView(LoginRequiredMixin, CreateView):
    model = Lead
    # fields = ('name', 'email', 'description', 'priority', 'status',)
    form_class = AddLeadForm
    success_url = reverse_lazy('leads:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.request.user.userprofile.active_team
        context['team'] = team
        context['title'] = 'Ajout prospect'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        # self.object.team = self.request.user.userprofile.active_team
        self.object.save()
        return redirect(self.get_success_url())


class AddFileView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        form = AddFileForm(request.POST, request.FILES)

        if form.is_valid():
            file = form.save(commit=False)
            file.team = self.request.user.userprofile.active_team
            file.lead_id = pk
            file.created_by = request.user
            file.save()

        return redirect('leads:detail', pk=pk)


class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        content = request.POST.get('content')

        form = AddCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.team = self.request.user.userprofile.active_team
            comment.created_by = request.user
            comment.lead_id = pk
            comment.save()

        return redirect('leads:detail', pk=pk)


class ConvertToClientView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')

        lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
        team = self.request.user.userprofile.active_team

        client = Client.objects.create(
            firm=lead.firm,
            first_name=lead.first_name,
            name=lead.name,
            email=lead.email,
            phone_number=lead.phone_number,
            description=lead.description,
            created_by=request.user,
            profile_picture=lead.profile_picture,
            # Make sure that team is set when converting lead to client
            # team=team,
            converted_date=datetime.datetime.now()
        )

        lead.converted_to_client = True
        lead.save()

        # --- Convert also lead comments to client comments ------
        comments = lead.comments.all()

        for comment in comments:
            ClientComment.objects.create(
                client=client,
                content=comment.content,
                created_by=comment.created_by,
                team=team
            )
        # ---------------------------------------------------------

        # --------------- Show message and redirect ---------------
        messages.success(request, 'Le prospect a été converti en client avec succès!')

        return redirect('leads:list')
