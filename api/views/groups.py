from rest_framework import viewsets
from rest_framework.views import APIView

from api.models import Group
from api.serializers import GroupSerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class UnpaginatedGroupViewSet(GroupViewSet):
    pagination_class = None


class GroupView(APIView):
    pass
