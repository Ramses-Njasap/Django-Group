from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.forms.models import model_to_dict

from accounts.models.users import User

import json, re


class Validate:
    def __init__(self, value: str):
        self.value = value

    def phone_field(self) -> tuple:
        if User.objects.filter(phone=self.value).exists():
            return False, "Phone Number Already Exists"
        
        # Regular expression pattern for a basic phone number address validation
        regex_pattern = r"^\+[0-9]{7,15}$"

        # Compile the regex pattern
        pattern = re.compile(regex_pattern)

        if not pattern.match(self.value):
            return False, 'Wrong Phone Number Pattern'
        
        return True, "Success"
    
    def username_field(self) -> tuple:
        # Check if the username starts with a number or special character
        if re.match(r'^[\W\d]', self.value):
            return False, 'Username cannot start with a number or special character.'

        # Check if the username contains numbers between letters
        if re.search(r'[a-zA-Z]+\d+[a-zA-Z]+', self.value):
            return False, 'Username cannot have numbers in between letters.'

        # Check if the username contains spaces or special characters other than "_"
        if re.search(r'[\s!@#$%^&*()+\-=\[\]{};\\:"|<,./<>?]', self.value):
            return False, "Username cannot contain spaces or special characters other than _"
        
        # Check if the username ends with a number and if the username can only be separated by "_"
        if re.match(r'.*\d$', self.value) and re.match(r'^[a-zA-Z0-9]+(_[a-zA-Z0-9]+)*$', self.value):
            return True, "Success"
            
        return False, "Username can only be separated by _"
    
    def password_field(self) -> tuple:
        if len(self.value) < 11:
            return False, 'Password Length Should Be Greater Than 11 Character.'
        
        # Define password strength criteria
        criteria = [
            (len(self.value) >= 12, "Password must be at least 12 characters long", 400),
            (re.search(r'[A-Z]', self.value), "Password must contain at least one uppercase letter", 400),
            (re.search(r'[a-z]', self.value), "Password must contain at least one lowercase letter", 400),
            (re.search(r'\d', self.value), "Password must contain at least one digit", 400),
            (re.search(r'[!@#$%^&*()_+{}\":<>?]', self.value), "Password must contain at least one special character", 400)
        ]

        failed_criteria = [(message, status_code) for condition, message, status_code in criteria if not condition]

        if failed_criteria:
            error_messages = [message for message, _ in failed_criteria]
            return False, error_messages
        
        
        return True, "Success"


@method_decorator(csrf_exempt, name='dispatch')
class DjUserView(View):
    def post(self, request):

        # Since it is an API, I'm assuming a json data
        data = json.loads(request.body.decode('utf-8'))

        # Do not change the format. It follows the order in which the Validate class functions are defined
        # There are better ways to do this but I don't have time. Plan to wrap up everything in 30 minutes
        keys_to_validate = ["phone", "username", "password"]

        # Instantiating Validate class for keys
        validation_results = {}

        for key in keys_to_validate:
            value = data.get(key, "")
            validate = Validate(value)

            # Calling the appropriate validation method based on the key
            validation_method = getattr(validate, f"{key}_field", None)

            if validation_method:
                success, message = validation_method()
                validation_results[key] = {"success": success, "message": message}
            else:
                validation_results[key] = {"success": False, "message": "Invalid key"}

        # Check validation results
        for key, result in validation_results.items():
            if not result["success"]:
                return JsonResponse({"success": False, "message": result["message"]}, status=400)

        user_instance = User.objects.create(username=data["username"], email=data["email"], phone=data["phone"])

        user_instance.set_password(data["password"])
        user_instance.save()

        user_instance = model_to_dict(user_instance)
        user_instance.pop("password")

        return JsonResponse({"success": True, "message": "User successfully validated and processed", "user": user_instance})


