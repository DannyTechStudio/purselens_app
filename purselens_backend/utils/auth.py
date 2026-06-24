#----------------------------------
# Authentication Check
#----------------------------------
def ensure_authenticated(user):
    if not user or not user.is_authenticated:
        raise ValueError("Signup required to perform this operation.")
        
        