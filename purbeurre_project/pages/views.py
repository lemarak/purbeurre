"""takes a Web request and returns a Web response."""
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    """Class-based views override the template name for Home Page."""
    template_name = 'pages/home.html'


class LegalNotices(TemplateView):
    """Class-based views override the template name for Legal Notices Page."""
    template_name = 'pages/legal_notices.html'
