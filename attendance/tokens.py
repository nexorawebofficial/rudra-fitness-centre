from django.core import signing

_SALT = 'attendance-checkin'


def generate_checkin_token(member_id):
    """Signs a member_id into a single opaque token safe to embed in a QR code URL."""
    return signing.Signer(salt=_SALT).sign(member_id)


def resolve_checkin_token(token):
    """Returns the member_id if the token is authentic, otherwise None."""
    try:
        return signing.Signer(salt=_SALT).unsign(token)
    except signing.BadSignature:
        return None
