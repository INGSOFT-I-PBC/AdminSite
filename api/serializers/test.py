from rest_framework.serializers import ModelSerializer

from api.models.test import ChildTest, TestModel


class TestChildSerializer(ModelSerializer):
    class Meta:
        model = ChildTest
        fields = "__all__"


class TestSerializer(ModelSerializer):

    childs = TestChildSerializer(required=False, many=True)

    def create(self, validated_data):
        child_data = validated_data.pop("childs", None)
        test = TestModel.objects.create(**validated_data)
        child_serializer = self.fields["childs"]

        if child_data:
            for each in child_data:
                each["parent"] = test
            child_serializer.create(child_data)
        return test

    class Meta:
        model = TestModel
        fields = "__all__"
