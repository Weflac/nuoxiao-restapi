from django.contrib.auth.models import User, Group

from rest_framework import viewsets, permissions, renderers
from rest_framework.decorators import detail_route,action
from rest_framework.response import Response

from nuoxiao.models import Snippet, Users, Blogs
from nuoxiao.permissions import IsOwnerOrReadOnly
from nuoxiao.serializers import SnippetSerializer, AccountSerializer, GroupSerializer, UserSerializer


class AccountViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = AccountSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class SnippetViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, )

    @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
    # @action(detail=True)
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# 用户
class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all().order_by('dateTime')
    serializer_class = UserSerializer(queryset, many=True)

