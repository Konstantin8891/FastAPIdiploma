from fastapi_contrib.serializers.common import ModelSerializer

from models import User


class UserSerializer(ModelSerializer):
    count: int

    class Meta:
        model = User