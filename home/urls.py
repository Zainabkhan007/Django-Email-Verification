from django.contrib import admin
from django.urls import path,include
from home import views
urlpatterns = [
path("",views.home,name="home"),
# path("about",views.about,name="about"),
# path("about",views.verify,name="verify"),

path("contact",views.contact,name="contact"),
path("search",views.search,name="search"),
path("signup",views.signup,name="signup"),
path("login",views.handeLogin,name="login"),
path("activate/<email_token>",views.activate_email,name="activate_email"),
path("logout",views.handelLogout,name="logout"),
]