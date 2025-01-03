from datetime import date
from app import create_app
from extensions import db
from models import User, Student, Supervisor, Admin, PrivacyLevel

# Create the Flask app
app = create_app()

# Use the app context to interact with the database
with app.app_context():
    # Clear existing data (optional, for testing purposes)
    db.session.query(User).delete()
    db.session.query(Student).delete()
    db.session.query(Admin).delete()
    db.session.query(Supervisor).delete()
    db.session.query(PrivacyLevel).delete()
    db.session.commit()

    # Add a privacy level
    privacy_level = PrivacyLevel(level="public", description="Visible to everyone")
    db.session.add(privacy_level)
    db.session.commit()

    # Create a student user
    student_user = User(
        username="alice_student",
        email="alice@example.com",
        role="student",
        status="active",
    )
    student_user.set_password("studentpass")
    db.session.add(student_user)
    db.session.commit()

    # Create a student profile
    student = Student(
        user_id=student_user.user_id,
        full_name="Alice Johnson",
        dob=date(2001, 2, 2),
        institution="Example University",
        major="Mathematics",
        privacy_level="public",
        bio="A dedicated student.",
    )
    db.session.add(student)
    db.session.commit()

    # Create an admin user
    admin_user = User(
        username="bob_admin", email="bob@example.com", role="admin", status="active"
    )
    admin_user.set_password("adminpass")
    db.session.add(admin_user)
    db.session.commit()

    # Create an admin profile
    admin = Admin(
        user_id=admin_user.user_id,
        created_by=admin_user.user_id,  # Self-created admin
        permissions={"manage_users": True, "manage_content": True},
        role="admin",
    )
    db.session.add(admin)
    db.session.commit()

    # Create a supervisor user
    supervisor_user = User(
        username="charlie_supervisor",
        email="charlie@example.com",
        role="supervisor",
        status="active",
    )
    supervisor_user.set_password("supervisorpass")
    db.session.add(supervisor_user)
    db.session.commit()

    # Create a supervisor profile
    supervisor = Supervisor(
        user_id=supervisor_user.user_id,
        institution="Example University",
        department="Engineering",
        bio="Experienced supervisor.",
    )
    db.session.add(supervisor)
    db.session.commit()

    print("Test data created successfully!")