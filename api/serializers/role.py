import rest_framework.serializers as serializers

from api.models.roles import Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "name", "codename", "role_class", "created_at"]
