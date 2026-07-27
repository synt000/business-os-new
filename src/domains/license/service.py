from datetime import datetime
import secrets
import string

from sqlalchemy.orm import Session

from src.domains.license.models import (
    LicenseKey,
    LicenseDevice,
    LicenseEvent
)


def generate_license_key():
    """
    Generate secure license key
    Example:
    BOS-A8F2-K91D-X72P
    """

    chars = string.ascii_uppercase + string.digits

    parts = [
        ''.join(secrets.choice(chars) for _ in range(4))
        for _ in range(4)
    ]

    return "BOS-" + "-".join(parts)



class LicenseService:


    @staticmethod
    def create_license(
        db: Session,
        tenant_id: str,
        expires_at: datetime,
        max_devices: int = 1
    ):

        key = generate_license_key()

        license_obj = LicenseKey(
            tenant_id=tenant_id,
            key=key,
            expires_at=expires_at,
            max_devices=max_devices,
            is_active=True
        )

        db.add(license_obj)
        db.commit()
        db.refresh(license_obj)


        event = LicenseEvent(
            license_id=license_obj.id,
            event_type="LICENSE_CREATED"
        )

        db.add(event)
        db.commit()


        return license_obj



    @staticmethod
    def validate_license(
        db: Session,
        license_key: str
    ):

        license_obj = (
            db.query(LicenseKey)
            .filter(
                LicenseKey.key == license_key
            )
            .first()
        )


        if not license_obj:
            return {
                "status":"INVALID",
                "reason":"LICENSE_NOT_FOUND"
            }


        if not license_obj.is_active:
            return {
                "status":"BLOCKED",
                "reason":"LICENSE_DISABLED"
            }


        if datetime.utcnow() > license_obj.expires_at:
            return {
                "status":"EXPIRED",
                "reason":"LICENSE_EXPIRED"
            }


        return {
            "status":"ACTIVE",
            "license_id":license_obj.id,
            "max_devices":license_obj.max_devices
        }



    @staticmethod
    def activate_device(
        db: Session,
        license_key: str,
        hardware_uid: str,
        device_name: str,
        client_ip: str
    ):


        license_obj = (
            db.query(LicenseKey)
            .filter(
                LicenseKey.key == license_key
            )
            .first()
        )


        if not license_obj:
            return {
                "status":"FAILED",
                "reason":"LICENSE_NOT_FOUND"
            }


        devices = (
            db.query(LicenseDevice)
            .filter(
                LicenseDevice.license_id == license_obj.id
            )
            .all()
        )


        for device in devices:

            if device.hardware_uid == hardware_uid:

                if device.is_blocked:
                    return {
                        "status":"BLOCKED",
                        "reason":"DEVICE_BLOCKED"
                    }


                device.last_login=datetime.utcnow()

                db.commit()


                return {
                    "status":"AUTHORIZED",
                    "device":"EXISTING"
                }



        if len(devices) >= license_obj.max_devices:

            return {
                "status":"DENIED",
                "reason":"DEVICE_LIMIT_REACHED"
            }



        new_device = LicenseDevice(
            license_id=license_obj.id,
            hardware_uid=hardware_uid,
            device_name=device_name,
            client_ip=client_ip
        )


        db.add(new_device)


        event = LicenseEvent(
            license_id=license_obj.id,
            event_type="DEVICE_ACTIVATED"
        )


        db.add(event)

        db.commit()


        return {
            "status":"AUTHORIZED",
            "device":"NEW"
        }



    @staticmethod
    def revoke_license(
        db: Session,
        license_id: str
    ):


        license_obj = (
            db.query(LicenseKey)
            .filter(
                LicenseKey.id == license_id
            )
            .first()
        )


        if not license_obj:
            return False


        license_obj.is_active=False


        event = LicenseEvent(
            license_id=license_id,
            event_type="LICENSE_REVOKED"
        )


        db.add(event)
        db.commit()


        return True



    @staticmethod
    def block_device(
        db: Session,
        device_id: str
    ):

        device = (
            db.query(LicenseDevice)
            .filter(
                LicenseDevice.id == device_id
            )
            .first()
        )


        if not device:
            return False


        device.is_blocked=True


        event = LicenseEvent(
            license_id=device.license_id,
            event_type="DEVICE_BLOCKED"
        )


        db.add(event)
        db.commit()


        return True
