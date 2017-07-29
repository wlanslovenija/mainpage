# -*- coding: utf-8 -*-

# PostgreSQL database password
DB_PASSWORD = '...'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '...'

#You can find them at: https://www.google.com/recaptcha/admin
RECAPTCHA_PUBLIC_KEY = '...'
RECAPTCHA_PRIVATE_KEY = '...-ijA'

PAYPAL_IDENTITY_TOKEN_PRODUCTION = '...'


class SecretNotDefined(Exception):
    exit()

if DB_PASSWORD == '...':
    raise SecretNotDefined("Database password is not set")
elif SECRET_KEY == '...':
    raise SecretNotDefined("Secret is not set")
elif RECAPTCHA_PRIVATE_KEY == '...' or RECAPTCHA_PUBLIC_KEY == '...':
    raise SecretNotDefined("Recaptcha keys not set")
elif PAYPAL_IDENTITY_TOKEN_PRODUCTION == '...':
    raise SecretNotDefined("Paypal identity toekn not set")