from django.views.generic import TemplateView
from charts import *


class IndexPageView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_10_expensive_hotels_bar_url'] = \
            Top10ExpensiveHotelsBar('all').url
        context['hotels_price_histogram_url'] = \
            HotelPriceHistogram('all').url
        context['top_10_sale_sights_bar_url'] = \
            Top10SaleSightsBar('all').url
        context['top_10_score_sights_bar_url'] = \
            Top10ScoreSightsBar('all').url
        return context


class ChangeLanguageView(TemplateView):
    template_name = 'main/change_language.html'
