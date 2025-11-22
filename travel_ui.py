import streamlit as st
import requests

st.set_page_config(page_title="ADK-Powered Travel Planner", page_icon="✈️")

st.title("🌍 ADK-Powered Travel Planner")

# ✨ Add start location here
origin = st.text_input("Where are you flying from?", placeholder="e.g., New York")

destination = st.text_input("Destination", placeholder="e.g., Paris")
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")
budget = st.number_input("Budget (in USD)", min_value=100, step=50)

# Traveler type selection
traveler_type = st.selectbox(
    "What type of traveler are you?",
    ["Nature Lover", "Activity Lover", "History Enthusiast", "Foodie", "Adventure Seeker", "Relaxation Seeker", "Culture Explorer", "General Traveler"],
    help="Select your travel preference to get personalized recommendations"
)

if st.button("Plan My Trip ✨"):
    if not all([origin, destination, start_date, end_date, budget]):
        st.warning("Please fill in all the details.")
    else:
        payload = {
            "origin": origin,
            "destination": destination,
            "start_date": str(start_date),
            "end_date": str(end_date),
            "budget": budget,
            "traveler_type": traveler_type.lower()
        }
        
        with st.spinner("Planning your trip... This may take a moment."):
            response = requests.post("http://localhost:8000/run", json=payload, timeout=120)

        if response.ok:
            data = response.json()
            
            st.subheader("✈️ Flights")
            st.markdown(data.get("flights", "No flights returned."))
            
            st.subheader("🏨 Stays")
            st.markdown(data.get("stay", "No stay options returned."))
            
            st.subheader("🗺️ Activities")
            st.markdown(data.get("activities", "No activities found."))
            
            st.subheader("📍 Places to Visit")
            places_data = data.get("places", "No places to visit returned.")
            if isinstance(places_data, str):
                st.markdown(places_data)
            else:
                st.markdown(places_data)
            
            st.subheader("📸 Popular Photo Spots & Locations")
            photos_data = data.get("photos", "No photo locations returned.")
            if isinstance(photos_data, list):
                for idx, place in enumerate(photos_data, 1):
                    with st.expander(f"📷 {place.get('name', f'Place {idx}')}"):
                        st.write(f"**Description:** {place.get('description', 'N/A')}")
                        st.write(f"**Photo Description:** {place.get('photo_description', 'N/A')}")
                        maps_location = place.get('google_maps_location', '')
                        if maps_location:
                            # Create a clickable Google Maps link
                            maps_url = f"https://www.google.com/maps/search/?api=1&query={maps_location.replace(' ', '+')}"
                            st.markdown(f"**📍 Google Maps:** [View on Google Maps]({maps_url})")
                            st.caption(f"Location: {maps_location}")
            else:
                st.markdown(photos_data)
        else:
            st.error("Failed to fetch travel plan. Please try again.")
            if response.status_code == 500:
                st.info("One or more agents may not be running. Please check the server logs.")
