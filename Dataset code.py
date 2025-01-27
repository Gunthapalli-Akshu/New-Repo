import csv
import random
from faker import Faker
import datetime

# Initialize Faker instance
fake = Faker()

# Function to generate one customer feedback entry
def generate_feedback():
    # Generate fake data
    customer_name = fake.name()
    customer_email = fake.email()
    feedback = fake.text(max_nb_chars=200)
    date_time = fake.date_time_this_year()
    server_name = fake.name()
    server_empid = fake.uuid4()[:8]  # Random 8-character ID
    customer_age = random.randint(18, 75)  # Age between 18 and 75
    customer_mobile_number = fake.phone_number()
    department = random.choice(["Sales", "Marketing", "Engineering", "HR", "Operations"])
    stay_duration_days = random.randint(1, 14)  # Stay duration between 1 and 14 days
    membership_status = random.choice(["yes","no"])
    nps = random.randint(0, 10)  # NPS between 0 and 10
    food_preference = random.choice(["Vegetarian", "Non-Vegetarian", "Vegan"])
    dining_room_preference = random.choice(["yes","no"])
    sports_activities_preference = random.choice(["yes","no"])
    wellness_preference = random.choice(["yes","no"])
    pricing_preference = random.choice(["high", "medium", "low"])

    return [
        customer_name, customer_email, feedback, date_time,
        server_name, server_empid, customer_age, customer_mobile_number,
        department, stay_duration_days, membership_status, nps,
        food_preference, dining_room_preference, sports_activities_preference,
        wellness_preference, pricing_preference
    ]

# Function to generate the dataset and save it to a CSV file
def generate_csv(filename, num_rows):
    # Define the header of the CSV file
    headers = [
        "Customer_Name", "Customer_Email", "Feedback", "Date_Time", 
        "Server_Name", "Server_EmpID", "Customer_Age", "Customer_MobileNumber", 
        "Department", "Stay_Duration_days", "Membership_Status", "NPS", 
        "Food_Preference", "Dining_Room_Preference", "Sports_Activities_Preference", 
        "Wellness_Preference", "Pricing_Preference"
    ]

    # Open the CSV file for writing
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        
        # Write the header row
        writer.writerow(headers)
        
        # Generate and write the data rows
        for _ in range(num_rows):
            writer.writerow(generate_feedback())

    print(f"Generated {num_rows} rows of customer feedback and saved to {filename}")

# Generate 10,000 rows and save to 'customer_feedback.csv'
if __name__ == "__main__":
    generate_csv("customer_feedback.csv", 10000)
