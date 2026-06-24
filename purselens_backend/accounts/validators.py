import re
from django.core.exceptions import ValidationError


class PasswordValidator:
    
    def validate(self, password, user=None):
        
        if len(password) < 12:
            raise ValidationError("Password must be at least 12 characters long")
        if not re.search(r'[A-Z]', password):
            raise ValidationError('Password must contain at least 1 uppercase letter')
        if not re.search(r'[a-z]', password):
            raise ValidationError('Password must contain at least 1 lowercase letter')
        if not re.search(r'\d', password):
            raise ValidationError("Password must contain at least 1 number")
        if not re.search(r'[!"#$%&()*+,-./:;<=>?@[\]^_`{|}~]', password):
            raise ValidationError('Password must contain at least 1 symbol')
        return password
    
    
    def get_help_text(self):
        return "Your password must be at least 12 characters and include at least 1 uppercase and lowercase letters, 1 number, and 1 symbol."