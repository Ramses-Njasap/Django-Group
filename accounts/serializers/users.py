from rest_framework import serializers

from accounts.models.users import User
import re


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

        read_only_fields = (
            'is_staff', 'is_admin', 'is_superuser', 'is_active', 'date_joined',
            'date_updated', 'last_login', 'last_logout'
        )

        extra_kwargs = {
            'username': {'required': False},
            'phone': {'required': False},
            'password': {
                'write_only': True
            }
        }

        def validate_username(self, value):
            # Check if the username starts with a number or special character
            if re.match(r'^[\W\d]', value):
                raise serializers.ValidationError('Username cannot start with a number or special character.')

            # Check if the username contains numbers between letters
            if re.search(r'[a-zA-Z]+\d+[a-zA-Z]+', value):
                raise serializers.ValidationError('Username cannot have numbers in between letters.')

            # Check if the username contains spaces or special characters other than "_"
            if re.search(r'[\s!@#$%^&*()+\-=\[\]{};\\:"|<,./<>?]', value):
                raise serializers.ValidationError("Username cannot contain spaces or special characters other than _")
            
            # Check if the username ends with a number and if the username can only be separated by "_"
            if re.match(r'.*\d$', value) and re.match(r'^[a-zA-Z0-9]+(_[a-zA-Z0-9]+)*$', value):
                return value
                
            raise serializers.ValidationError("Username can only be separated by _")
        
        def validate_phone(self, value):
            if User.objects.filter(phone=value).exists():
                raise serializers.ValidationError('A user with this phone already exists. Proceed to login.')
            
            # Regular expression pattern for a basic phone number address validation
            regex_pattern = r"^\+[0-9]{7,15}$"

            # Compile the regex pattern
            pattern = re.compile(regex_pattern)

            if not pattern.match(value):
                raise serializers.ValidationError('Wrong Phone Number Pattern')
            
            return value
        
        def validate_password(self, value):
            if len(value) < 11:
                raise serializers.ValidationError('Password Length Should Be Greater Than 11 Character.')
            
            # Define password strength criteria
            criteria = [
                (len(value) >= 12, "Password must be at least 12 characters long", 400),
                (re.search(r'[A-Z]', value), "Password must contain at least one uppercase letter", 400),
                (re.search(r'[a-z]', value), "Password must contain at least one lowercase letter", 400),
                (re.search(r'\d', value), "Password must contain at least one digit", 400),
                (re.search(r'[!@#$%^&*()_+{}\":<>?]', value), "Password must contain at least one special character", 400)
            ]

            failed_criteria = [(message, status_code) for condition, message, status_code in criteria if not condition]

            if failed_criteria:
                error_messages = [message for message, _ in failed_criteria]
                raise serializers.ValidationError(error_messages)
            
            return value
        
        def _create_user_with_password(self, validated_data):
            password = validated_data.pop('password', None)

            try:
                user_instance = User.objects.create(**validated_data)
            except Exception as e:
                raise serializers.ValidationError(str(e))

            if password:
                user_instance.set_password(password)
                user_instance.save()
            else:
                raise serializers.ValidationError('Password is a required field.')

            return user_instance

        def create(self, validated_data):
            user_instance = self._create_user_with_password(validated_data)

            return user_instance