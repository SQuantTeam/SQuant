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
    url(r'strategy/getFinishedAlgo$', views.get_finished_algo, ),
    url(r'strategy/getAllAlgo$', views.get_all_algo, ),
    url(r'strategy/getAllStra$', views.get_all_stra, ),
    url(r'strategy/deleteStra$', views.delete_stra, ),
    url(r'strategy/deleteAlgo$', views.delete_algo, ),
    url(r'strategy/runExistedAlgo$', views.run_existed_algo, ),
]

if settings.DEBUG:
    media_root = os.path.join(settings.BASE_DIR, 'output')
    urlpatterns += static('/output/', document_root=media_root)