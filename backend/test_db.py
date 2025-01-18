from datetime import date, timedelta
import random
from faker import Faker
from app import create_app
from extensions import db
from models import User, Student, Supervisor, Admin, PrivacyLevel, FileType, EntityType, RecommendationStatus, File, Event, Notification, History, Recommendation, Email

def init_db():
    app = create_app()
    fake = Faker()

    with app.app_context():
        # Add privacy levels if they don't exist
        if not PrivacyLevel.query.first():
            privacy_levels = [
                PrivacyLevel(level="public", description="Visible to everyone"),
                PrivacyLevel(level="private", description="Visible only to the user"),
                PrivacyLevel(level="supervisors", description="Visible to supervisors and admins")
            ]
            db.session.add_all(privacy_levels)

        # Add file types if they don't exist
        if not FileType.query.first():
            file_types = [
                FileType(type_name="document"),
                FileType(type_name="image"),
                FileType(type_name="video")
            ]
            db.session.add_all(file_types)

        # Add entity types if they don't exist
        if not EntityType.query.first():
            entity_types = [
                EntityType(type="user", description="User actions"),
                EntityType(type="file", description="File actions"),
                EntityType(type="event", description="Event actions")
            ]
            db.session.add_all(entity_types)

        # Add recommendation statuses if they don't exist
        if not RecommendationStatus.query.first():
            recommendation_statuses = [
                RecommendationStatus(status="pending", description="Recommendation is pending"),
                RecommendationStatus(status="accepted", description="Recommendation is accepted"),
                RecommendationStatus(status="rejected", description="Recommendation is rejected")
            ]
            db.session.add_all(recommendation_statuses)

        db.session.commit()

        # Create users
        users = []
        roles = ["student", "supervisor", "admin"]
        for _ in range(12):  # 12 users
            role = random.choice(roles)
            user = User(
                username=fake.user_name(),
                email=fake.email(),
                role=role,
                full_name=fake.name(),
                dob=fake.date_of_birth(minimum_age=18, maximum_age=65),
                status=random.choice(["active", "idle", "offline"]),
            )
            user.set_password(f"{role}pass")
            users.append(user)

        db.session.add_all(users)
        db.session.commit()

        # Create profiles for students, supervisors, and admins
        for user in users:
            if user.role == "student":
                student = Student(
                    user_id=user.user_id,
                    institution=fake.company(),
                    major=fake.job(),
                    privacy_level=random.choice(["public", "private", "supervisors"]),
                    bio=fake.text(),
                )
                db.session.add(student)
            elif user.role == "supervisor":
                supervisor = Supervisor(
                    user_id=user.user_id,
                    institution=fake.company(),
                    department=fake.job(),
                    bio=fake.text(),
                )
                db.session.add(supervisor)
            elif user.role == "admin":
                admin = Admin(
                    user_id=user.user_id,
                    created_by=random.choice([u.user_id for u in users if u.role == "admin"]),
                    permissions={
                        "manage_users": random.choice([True, False]),
                        "manage_content": random.choice([True, False])
                    },
                    role="admin",
                )
                db.session.add(admin)

        db.session.commit()

        # Create files
        for user in users:
            for _ in range(random.randint(1, 5)):
                file = File(
                    user_id=user.user_id,
                    file_name=fake.file_name(extension=random.choice(["pdf", "jpg", "mp4"])),
                    file_path=f"/path/to/{fake.file_path()}",
                    file_type=random.choice(["document", "image", "video"]),
                    file_type_id=random.randint(1, 3),
                    visibility=random.choice(["public", "private", "supervisors"]),
                )
                db.session.add(file)

        db.session.commit()

        # Create events
        for user in users:
            for _ in range(random.randint(1, 3)):
                event = Event(
                    user_id=user.user_id,
                    title=fake.sentence(),
                    description=fake.text(),
                    date=fake.date_between(start_date="-30d", end_date="+30d"),
                    location=fake.address(),
                )
                db.session.add(event)

        db.session.commit()

        # Create notifications
        for user in users:
            for _ in range(random.randint(1, 5)):
                notification = Notification(
                    user_id=user.user_id,
                    message=fake.sentence(),
                )
                db.session.add(notification)

        db.session.commit()

        # Create history entries
        actions = ["login", "logout", "file_upload", "event_create"]
        for user in users:
            for _ in range(random.randint(1, 10)):
                history = History(
                    user_id=user.user_id,
                    action_type=random.choice(actions),
                    action_details=fake.sentence(),
                    entity_type=random.choice(["user", "file", "event"]),
                    entity_id=random.randint(1, 100),
                )
                db.session.add(history)

        db.session.commit()

        # Create recommendations
        events = Event.query.all()
        for event in events:
            for _ in range(random.randint(1, 2)):
                recommendation = Recommendation(
                    user_id=random.choice([u.user_id for u in users]),
                    event_id=event.event_id,
                    status=random.choice(["pending", "accepted", "rejected"]),
                )
                db.session.add(recommendation)

        db.session.commit()

        # Create emails
        for _ in range(20):
            sender = random.choice(users)
            recipient = random.choice([u for u in users if u != sender])
            email = Email(
                sender_id=sender.user_id,
                recipient_id=recipient.user_id,
                subject=fake.sentence(),
                message=fake.text(),
            )
            db.session.add(email)

        db.session.commit()

        print("Test data created successfully!")

if __name__ == "__main__":
    init_db()
