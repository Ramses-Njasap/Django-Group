from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers.users import UserSerializer
from accounts.models.users import User

class UserView(APIView):
    def post(self, request):
        data = request.data

        for user in User.objects.all():
            user.is_active = True
            user.save()

        user_serializer = UserSerializer(data=data)

        if user_serializer.is_valid():
            user = user_serializer.create(user_serializer.validated_data)
            print("Password:: ", user_serializer.validated_data.get('password', 'Not Available'))
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)