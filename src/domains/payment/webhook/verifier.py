import hmac
import hashlib


def verify_signature(
    payload: str,
    signature: str,
    secret: str,
) -> bool:
    """
    Verify webhook signature using HMAC SHA256.
    """

    if not payload:
        return False

    if not signature:
        return False

    if not secret:
        return False

    expected = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(
        expected,
        signature,
    )
