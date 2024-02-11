from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from team.forms import TeamForm
from team.models import Team

@login_required
def teams_list(request):
    teams = Team.objects.filter(members__in=[request.user])

    context = {
        "teams": teams,
    }

    return render(request, "team/teams_list.html", context)

@login_required
def teams_activate(request, pk):
    team = Team.objects.filter(members__in=[request.user]).get(pk=pk)
    userprofile= request.user.userprofile
    userprofile.active_team = team
    userprofile.save()

    return redirect("team:detail", pk=pk)


@login_required
def detail(request, pk):
    team = get_object_or_404(Team, members__in=[request.user], pk=pk)

    context = {
        "team":team,
    }

    return render(request, "team/detail.html", context)


@login_required
def team_edit(request, pk):
    team = get_object_or_404(Team, created_by=request.user, pk=pk)

    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)

        if form.is_valid():
            form.save()

            messages.success(request, "Modification enregistrées!")
            return redirect('myaccount')
    else:
        form = TeamForm(instance=team)

    context = {
        "team":team,
        "form": form,
    }

    return render(request, "team/team_edit.html", context)