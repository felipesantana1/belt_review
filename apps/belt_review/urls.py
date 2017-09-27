from django.conf.urls import url
import views

urlpatterns = [
    
    url(r'^$', views.index),
    url(r'^books$', views.books),
    url(r'^books/add$', views.add),
    url(r'^add-book$', views.addBook),
    url(r'^books/(?P<id>\d+)$', views.display),
    url(r'^users/(?P<id>\d+)$', views.displayUser),
    url(r'^create$', views.create),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^home$', views.home),
    url(r'^review/(?P<id>\d+)$', views.addReview)

]