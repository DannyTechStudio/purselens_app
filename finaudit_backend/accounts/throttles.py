from rest_framework.throttling import AnonRateThrottle


class LoginThrottle(AnonRateThrottle):
    scope = 'login'
    

class RegisterThrottle(AnonRateThrottle):
    scope = 'register'
    

class PasswordResetThrottle(AnonRateThrottle):
    scope = 'password_reset'

