from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render


from calendarapp.models import Event

class DashboardView(LoginRequiredMixin, View):
    login_url = "accounts:signin"
    template_name = "calendarapp/dashboard.html"

    def get(self, request, *args, **kwargs):
        # events = Event.objects.get_all_events(user=request.user)
        events = Event.objects.all()
        running_events = Event.objects.get_running_events()
        # latest_events = Event.objects.filter(user=request.user).order_by("-id")[:10]
        latest_events = Event.objects.all().order_by("-id")[:10]
        context = {
            "total_event": events.count(),
            "running_events": running_events,
            "latest_events": latest_events,
        }
        return render(request, self.template_name, context)
