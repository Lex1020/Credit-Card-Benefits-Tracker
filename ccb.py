# Credit Card Benefits Tracker as a Web App in Docker using Streamlit

# Section 1: Import Libraries
import streamlit as st
import json
import os
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Default file to store the benefits data
# The location can be customized with the BENEFITS_DATA_FILE environment variable.
DEFAULT_DATA_FILE = "credit_card_benefits.json"


def get_data_file():
    """Return the path to the benefits data file."""
    return os.getenv("BENEFITS_DATA_FILE", DEFAULT_DATA_FILE)

# Section 2: Load and Save Benefits Data
def load_benefits():
    data_file = get_data_file()
    if os.path.exists(data_file):
        try:
            with open(data_file, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError) as e:
            st.error(f"Error loading benefits file: {e}")
            return {}
    else:
        st.warning("No existing benefits file found. A new one will be created upon adding a benefit.")
    return {}

def save_benefits():
    data_file = get_data_file()
    try:
        with open(data_file, "w") as file:
            json.dump(benefits, file, indent=4)
    except IOError as e:
        st.error(f"Error saving benefits file: {e}")

# Section 3: Handle Reset Intervals
def calculate_reset_time(interval):
    now = datetime.now()
    if interval == "Monthly":
        return (now + timedelta(days=30)).strftime("%Y-%m-%d")
    elif interval == "Yearly":
        return (now + timedelta(days=365)).strftime("%Y-%m-%d")
    elif interval == "5 Years":
        return (now + timedelta(days=1825)).strftime("%Y-%m-%d")

def check_resets():
    now = datetime.now().strftime("%Y-%m-%d")
    for name, details in benefits.items():
        if details.get("next_reset") and details["next_reset"] <= now:
            benefits[name]["used"] = 0.0
            benefits[name]["next_reset"] = calculate_reset_time(details["reset_interval"])
    save_benefits()

# Section 4: Load Benefits Data
benefits = load_benefits()
check_resets()

# Section 5: Streamlit UI
def main():
    st.title("Credit Card Benefits Tracker")

    # Add a new benefit
    st.header("Add a New Benefit")
    name = st.text_input("Benefit Name")
    description = st.text_input("Description")
    reset_interval = st.selectbox("Reset Interval", ["Monthly", "Yearly", "5 Years"])

    if st.button("Add Benefit"):
        if name and description:
            benefits[name] = {"description": description, "used": 0.0, "reset_interval": reset_interval, "next_reset": calculate_reset_time(reset_interval)}
            save_benefits()
            st.success(f"Benefit '{name}' added successfully!")
            st.rerun()
        else:
            st.warning("Please enter both name and description.")

    # Update benefit usage
    st.header("Update Benefit Usage")
    if benefits:
        benefit_to_update = st.selectbox("Select a Benefit", list(benefits.keys()))
        percent_used = st.slider("Usage Percentage", 0, 100, int(benefits.get(benefit_to_update, {}).get("used", 0) * 100))
        if st.button("Update Usage"):
            benefits[benefit_to_update]["used"] = percent_used / 100.0
            save_benefits()
            st.success(f"Updated usage for '{benefit_to_update}'")
            st.rerun()
    else:
        st.write("No benefits available to update.")

    # Delete a benefit
    st.header("Delete a Benefit")
    if benefits:
        benefit_to_delete = st.selectbox("Select a Benefit to Delete", list(benefits.keys()))
        if st.button("Delete Benefit"):
            del benefits[benefit_to_delete]
            save_benefits()
            st.success(f"Deleted '{benefit_to_delete}'")
            st.rerun()
    else:
        st.write("No benefits available to delete.")

    # Display benefits
    st.header("Current Benefits")
    if benefits:
        for name, details in benefits.items():
            st.write(f"**{name}**: {details['description']} - Used: {details['used'] * 100:.0f}%, Resets: {details['next_reset']}")
    else:
        st.write("No benefits recorded yet.")

    # Display usage graph
    st.header("Usage Graph")
    if benefits:
        names = list(benefits.keys())
        # convert stored fractional usage values to percentages for visualization
        usage_percentages = [details["used"] * 100 for details in benefits.values()]
        if not names or not usage_percentages:
            st.write("No valid benefits available for visualization.")
            return
        colors = ["green" if u < 50 else "orange" if u < 80 else "red" for u in usage_percentages]

        fig, ax = plt.subplots()
        ax.bar(names, usage_percentages, color=colors)
        ax.set_xlabel("Benefit")
        ax.set_ylabel("Usage (%)")
        ax.set_title("Credit Card Benefits Usage")
        plt.xticks(rotation=45, ha='right')
        
        st.pyplot(fig)
    else:
        st.write("No benefits recorded yet.")

# Run the Streamlit app in Docker
if __name__ == "__main__":
    main()
