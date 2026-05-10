from app.database import SessionLocal
from app.models.user import User
from app.utils.security import hash_password


def create_admin():
    db = SessionLocal()

    try:
        admin_email = "admin@gigscore.com"
        admin_password = "admin123"

        existing_admin = db.query(User).filter(User.email == admin_email).first()

        if existing_admin:
            print("Admin already exists")
            print(f"Email: {admin_email}")
            return

        admin = User(
            name="GigScore Admin",
            email=admin_email,
            password_hash=hash_password(admin_password),
            role="admin",
        )

        db.add(admin)
        db.commit()
        db.refresh(admin)

        print("Admin created successfully")
        print(f"Email: {admin_email}")
        print(f"Password: {admin_password}")

    finally:
        db.close()


if __name__ == "__main__":
    create_admin()