"""
Script to populate the database with activity categories and types
"""
from app import app, db
from app.models import Category, ActivityType

#Define the categories and their associated activity types
ACTIVITIES_DATA = {
    "Sports & Fitness": [
        "Walking",
        "Running",
        "Gym / Workout",
        "Tennis",
        "Football",
        "Swimming",
        "Cycling",
        "Yoga / Stretching"],
    "Study & Work": [
        "Studying together",
        "Library study session",
        "Exam preparation",
        "Group assignment"],
    "Social & Casual": [
        "Coffee / Chat",
        "Lunch / Dinner",
        "Board games",
        "Card games",
        "Movie night"],
    "Outdoor & Leisure": [
        "City walk",
        "Nature walk",
        "Picnic",
        "Photography walk",
        "Exploring the city"],
    "Hobbies & Entertainment": [
        "Video games",
        "Chess",
        "Music practice",
        "Drawing / Art",
        "Reading"],
    "University & Student Life": [
        "Campus activities",
        "Student events",
        "Language exchange",
        "International meet-up"],
    "Other / Custom": [
        "Other"]}


def populate_database():
    """Populate the database with categories and activity types"""
    with app.app_context():
        print("Starting database population...")

        #Check if data already exists
        existing_categories = Category.query.count()
        if existing_categories > 0:
            print(f"Found {existing_categories} existing categories.")
            response = input("Do you want to clear existing data and repopulate? Answer with yes or no: ")
            if response.lower() == 'yes':
                print("Clearing existing data...")
                ActivityType.query.delete()
                Category.query.delete()
                db.session.commit()
            else:
                print("Keeping existing data")
                return

        #Create categories and their activity types
        for category_name, activity_types in ACTIVITIES_DATA.items():
            print(f"\nCreating category: {category_name}")

            #Create category
            category = Category(
                name=category_name,
                description=f"Activities related to {category_name.lower()}"
            )
            db.session.add(category)
            db.session.flush()

            #Create activity types for this category
            for type_name in activity_types:
                activity_type = ActivityType(
                    name=type_name,
                    category_id=category.id
                )
                db.session.add(activity_type)
                print(f"  - Added activity type: {type_name}")

        db.session.commit()
        print("\nDatabase populated successfully!")

        total_categories = Category.query.count()
        total_types = ActivityType.query.count()
        print(f"\nSummary:")
        print(f"  Total categories: {total_categories}")
        print(f"  Total activity types: {total_types}")

        #Display all categories and their types
        print("\nCategories and Activity Types:")
        for category in Category.query.all():
            print(f"\n{category.name}:")
            types = ActivityType.query.filter_by(category_id=category.id).all()
            for activity_type in types:
                print(f"  - {activity_type.name}")


if __name__ == "__main__":
    populate_database()