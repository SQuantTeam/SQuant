from django.conf.urls import url, include
import views
import user_views

urlpatterns = [
    # url(r'add_book$', views.add_book, ),
    # url(r'show_books$', views.show_books, ),
    url(r'user/(?P<email>[A-Za-z0-9_\-\.\u4e00-\u9fa5])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,8})$', user_views.get_user, ),
    url(r'user/add', user_views.add_user, ),
    url(r'user/update$', user_views.update_user, ),
    url(r'user/delete/(?P<email>[A-Za-z0-9_\-\.\u4e00-\u9fa5])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,8})$', user_views.delete_user, ),
    url(r'market/connect$', views.connect, ),
    url(r'market/quote/(?P<symbol>[0-9]{6}\.S[HZ])$', views.quote, ),
    url(r'market/placeOrder$', views.placeOrder, ),
    url(r'market/cancelPortfolioOrder$', views.cancelPortfolioOrder, ),
    url(r'market/queryPosition$', views.queryPosition, ),
    url(r'market/queryOrder$', views.queryOrder, ),
    url(r'market/queryTrade$', views.queryTrade, ),
    url(r'market/bar/(?P<symbol>[0-9]{6}\.S[HZ])/(?P<trade_date>[0-9]{4}\-[0-9]{2}\-[0-9]{2})$', views.bar, ),
    url(r'market/daily/(?P<symbol>[0-9]{6}\.S[HZ])/(?P<start_date>[0-9]{4}\-[0-9]{2}\-[0-9]{2})/(?P<end_date>'
        r'[0-9]{4}\-[0-9]{2}\-[0-9]{2})$', views.daily, ),
    ]