from .models import User
# from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer


class LogoutView(APIView):
    """
    API endpoint that implement the logout action in the system
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if self.request.data.get('all'):
            token: OutstandingToken
            for token in OutstandingToken.objects.filter(user=request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response({"status": "goodbye"})
        refresh_token = self.request.data.get('refresh_token')
        token = RefreshToken(token=refresh_token)
        token.blacklist()
        return Response({"status": "OK, goodbye"})


class PermissionsView(APIView):

    def get(self, request, *args, **kwargs):
        user = request.user
        breakpoint()
        print(User.objects.all().query)
        # permissions = User.objects.filter(id=2).select_related('permissions', 'user_permissions')
        # print(**user)
        return Response({
            # 'fullname': f'{user.name} {user.lastname}',
            'id': user.id,
            'permissions': [
            ]
        })
