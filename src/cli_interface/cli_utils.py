import json
import os

def save_profile(profile):
    filename = input("Enter filename to save your profile (e.g., profile.json): ").strip()
    if not filename.endswith('.json'):
        filename += '.json'
    try:
        with open(filename, 'w') as f:
            json.dump(profile, f, indent=2)
        print(f"✅ Profile saved to {filename}")
    except Exception as e:
        print(f"❌ Error saving profile: {e}")

def load_profile():
    filename = input("Enter filename to load your profile from (e.g., profile.json): ").strip()
    if not os.path.isfile(filename):
        print("❌ File not found.")
        return None
    try:
        with open(filename, 'r') as f:
            profile = json.load(f)
        print(f"✅ Profile loaded from {filename}")
        return profile
    except Exception as e:
        print(f"❌ Error loading profile: {e}")
        return None
