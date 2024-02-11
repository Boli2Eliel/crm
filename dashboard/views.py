import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from lead.models import Lead
from client.models import Client
from team.models import Team


# Create your views here.

@login_required
def dashboard(request):
    #team = request.user.userprofile.active_team
    thirty_days_ago = datetime.date.today() - datetime.timedelta(days=30)

    # leads = Lead.objects.filter(team=team, converted_to_client=False, created_at__gte=thirty_days_ago).order_by('-created_at')[0:4]
    leads_all = Lead.objects.filter(converted_to_client=False,
                                created_at__gte=thirty_days_ago).order_by('-created_at')[0:4]

    leads = Lead.objects.filter(created_by=request.user, converted_to_client=False,
                                created_at__gte=thirty_days_ago).order_by('-created_at')[0:4]

    clients_all = Client.objects.filter(created_at__gte=thirty_days_ago).order_by('-created_at')[0:4]

    clients = Client.objects.filter(created_by=request.user, created_at__gte=thirty_days_ago).order_by('-created_at')[0:4]

    # How many new leads in the last 30 days

    total_lead_count_all = Lead.objects.filter(converted_to_client=False).count()

    # By TEAM
    total_lead_count = Lead.objects.filter(created_by=request.user, converted_to_client=False).count()
    # total_lead_count = Lead.objects.filter(team=team).count()
    # total_client_count = Client.objects.filter(team=team).count()

    total_client_count_all = Client.objects.all().count()
    total_client_count = Client.objects.filter(created_by=request.user, ).count()

    total_leads_in_past30_all = Lead.objects.filter(
        # team=team,
        created_at__gte=thirty_days_ago
    ).count()

    total_leads_in_past30 = Lead.objects.filter(
        # team=team,
        created_by=request.user,
        created_at__gte=thirty_days_ago
    ).count()

    # How many new clients in the last 30 days

    converted_to_clients = Lead.objects.filter(created_by=request.user, converted_to_client=True).count()
    converted_to_clients_all = Lead.objects.filter(converted_to_client=True).count()

    context = {
        "leads_all": leads_all,
        "leads": leads,

        "clients_all": clients_all,
        "clients": clients,

        "total_leads_in_past30_all": total_leads_in_past30_all,
        "total_leads_in_past30": total_leads_in_past30,

        "total_lead_count_all": total_lead_count_all,
        "total_lead_count": total_lead_count,

        "total_client_count_all": total_client_count_all,
        "total_client_count": total_client_count,

        "converted_to_clients_all": converted_to_clients_all,
        "converted_to_clients": converted_to_clients
    }
    return render(request, "dashboard/dashboard.html", context)
