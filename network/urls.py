
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.new_post, name="new_post"),
    path('myprofile/<str:username>/<int:page_visiting>',
         views.myprofile, name="myprofile"),
    path('following/<int:page_visiting>', views.following, name="following"),
    path('pages/<int:page_visiting>', views.pages, name="pages"),
    path('comment/<int:post_id>', views.comment, name='comment'),
    path('edit_html/<int:post_id>', views.edit_html, name='edit_html'),

    # API Routes
    path('like/<int:post_id>', views.like, name='like'),
    path('edit/<int:post_id>', views.edit, name='edit'),
    path('follow/<str:user_profile>',
         views.follow, name='follow'),
    path('change/<int:page_visiting>/<str:button>/<str:from_page>/<str:username>',
         views.change, name='change')
]
