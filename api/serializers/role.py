import rest_framework.serializers as serializers

from api.models.roles import Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id','name','codename','role_class']

class UpdateRoleSerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=64, allow_blank=False, allow_null=False, required=False
    )
    codename = serializers.CharField(
        max_length=50, allow_blank=False, allow_null=False, required=False
    )
    # TODO: add a validator to `cid` field
    role_class = serializers.CharField(
        max_length=128, allow_blank=False, allow_null=False, required=False
    )

    def create(self, validated_data):
        return Role(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.codename = validated_data.get("lastname", instance.codename)
        instance.role_class = validated_data.get("role_class", instance.role_class)
        return instance
