from django.core.exceptions import ValidationError


# Custom validators for enforcing 100 words for transaction description
def validate_max_words(value):
    words = value.split()
    
    if len(words) > 100:
        raise ValidationError(
            "Transaction description cannot be more than 100 words."
        )
        
        