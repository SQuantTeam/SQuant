from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
import os

import views

import squant.settings

urlpatterns = [
    url(r'strategy/doBacktest$', views.do_backtest, ),
    url(r'strategy/runSniperAlgo$', views.run_sniper_algo, ),
    url(r'strategy/runTwapAlgo$', views.run_twap_algo, ),
]

if settings.DEBUG:
    media_root = os.path.join(settings.BASE_DIR, 'output')
    urlpatterns += static('/output/', document_root=media_root)