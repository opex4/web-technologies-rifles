from typing import Any

from django.views.generic import TemplateView

from rifles.models import Rifle


# Create your views here.
class ShowRiflesView(TemplateView):
    template_name = 'rifles/show.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['rifles'] = Rifle.objects.all()

        return context
