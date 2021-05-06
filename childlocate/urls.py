from django.urls.conf import path
from django.conf import settings
from django.conf.urls.static import static

from .views import UserViewSet, GetAuthToken, GetAllParents, \
    LogoutView, BusPositionViewSet, ParentsPositionView, BusViewSet, \
    BusPositionViewSet, DriverViewSet

urlpatterns = [
    path('parents/', GetAllParents.as_view()),
    path('parents/signup/', UserViewSet.as_view(), name="registration"),
    path('parents/login/', GetAuthToken.as_view(), name="login"),
    path('parents/logout/', LogoutView.as_view(), name="logout"),
    path('parents/position/', ParentsPositionView.as_view(), name="user_position"),
    path('bus/', BusViewSet.as_view(), name="bus_list"),
    path('bus/position', BusPositionViewSet.as_view(), name="bus_pistion"),
    path('driver/', DriverViewSet.as_view(), name="drivers_list")
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
