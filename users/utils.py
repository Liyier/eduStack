import base64, uuid


def convert_password(password):
    return base64.b64encode(password.encode('utf-8')).decode()
