from rest_framework import serializers
from apps.professionals.models import Professional


class PublicProfessionalBriefSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(source="id", read_only=True)
    avatar = serializers.CharField(read_only=True, allow_null=True)

    class Meta:
        model = Professional
        fields = [
            "uid",
            "full_name",
            "position",
            "avatar",
            "rating",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")

        if instance.avatar and request:
            data["avatar"] = request.build_absolute_uri(instance.avatar.url)
        else:
            data["avatar"] = None

        return data
