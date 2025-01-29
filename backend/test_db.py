from datetime import datetime, timedelta
import random
from faker import Faker
from app import create_app
from extensions import db
from models import User, Student, Supervisor, Admin, PrivacyLevel, FileType, EntityType, RecommendationStatus, File, Event, Notification, History, Recommendation, Email

def init_db():
    app = create_app()
    fake = Faker()

    with app.app_context():
        # Drop all tables before creating new ones
        # db.drop_all()  # This will drop all tables in the database
        # db.create_all()  # This will recreate all tables based on the models

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

        # Create users with random created_at times
        users = []
        roles = ["student", "supervisor", "admin"]
        for _ in range(12):  # 12 users
            role = random.choice(roles)

            # Randomize user creation date between 1 and 2 years ago
            random_creation_date = fake.date_between_dates(
                date_start=datetime.now() - timedelta(days=730), date_end=datetime.now()
            )
            random_creation_date = datetime.combine(random_creation_date, datetime.min.time()) + timedelta(
                seconds=random.randint(0, 86400)  # Random time within the day
            )

            # Set dob (Date of Birth) based on the role:
            if role == "student":
                # Students should be between 18 and 30 years old
                dob = fake.date_of_birth(minimum_age=18, maximum_age=30)
            elif role == "supervisor":
                # Supervisors should be between 30 and 50 years old
                dob = fake.date_of_birth(minimum_age=30, maximum_age=50)
            else:
                # Admins should be between 25 and 60 years old
                dob = fake.date_of_birth(minimum_age=25, maximum_age=60)

            user = User(
                username=fake.user_name(),
                email=fake.email(),
                role=role,
                full_name=fake.name(),
                dob=dob,  # Logical age based on role
                status=random.choice(["active", "idle", "offline"]),
                created_at=random_creation_date,  # Random creation date for user
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

        # Create files with more logical details (uploaded_at after user creation)
        for user in users:
            for _ in range(random.randint(1, 5)):
                # Select file type and corresponding extension
                file_type = random.choice(["document", "image", "video"])
                if file_type == "image":
                    extension = "jpg"
                    directory = "images"
                elif file_type == "video":
                    extension = "mp4"
                    directory = "videos"
                else:
                    extension = "pdf"
                    directory = "documents"
                
                # Generate file name and path
                file_name = f"{fake.word()}.{extension}"
                file_path = f"/path/to/{directory}/{file_name}"
                
                # Generate a random uploaded_at date, ensuring it's after the user's creation date
                user_creation_date = user.created_at  # Now, each user has a random 'created_at' date
                min_date = user_creation_date  # Ensure the file's upload date is after user creation

                # Generate random year between 1 and 3 years ago (for variety)
                years_back = random.randint(1, 3)
                random_year = datetime.now() - timedelta(days=365 * years_back)

                # Generate random day and time for file upload after the user creation date
                uploaded_at = fake.date_between_dates(
                    date_start=random_year, date_end=datetime.now()
                )
                uploaded_at = datetime.combine(uploaded_at, datetime.min.time()) + timedelta(
                    seconds=random.randint(0, 86400)  # Random time within the day
                )
                
                # Ensure the uploaded_at is after the user's creation date
                if uploaded_at < min_date:
                    uploaded_at = min_date + timedelta(days=random.randint(1, 30))  # Add up to 30 days

                # Create file with type, path, and random uploaded_at date
                file = File(
                    user_id=user.user_id,
                    file_name=file_name,
                    file_path=file_path,
                    file_type=file_type,
                    file_type_id=random.randint(1, 3),
                    visibility=random.choice(["public", "private", "supervisors"]),
                    uploaded_at=uploaded_at,
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
