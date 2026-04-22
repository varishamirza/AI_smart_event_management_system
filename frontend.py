# frontend.py
import streamlit as st
import requests
import json
from datetime import datetime

# Match your FastAPI backend port (default is 8000)
# Set this to the URL where your FastAPI backend is running
# The user requested port 8502
API_BASE = "http://127.0.0.1:8502"

st.set_page_config(page_title="AI Smart Event Management", layout="wide")
st.title("🎉 AI Smart Event Management System")
st.markdown("Manage venues, events, attendees and registrations with AI help!")

# Debug info
with st.sidebar:
    st.write("### 🔧 Debug Info")
    st.write(f"**API Base URL:** {API_BASE}")
    # Test connection
    try:
        resp = requests.get(f"{API_BASE}/", timeout=2)
        if resp.status_code == 200:
            st.success("✓ Backend connected!")
        else:
            st.error(f"✗ Backend returned {resp.status_code}")
    except Exception as e:
        st.error(f"✗ Cannot reach backend: {e}")

# ── Main content ────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["Venues", "Events", "Attendees", "AI"])

with tab1:
    st.subheader("Venues")
    try:
        resp = requests.get(f"{API_BASE}/venues/")
        if resp.status_code == 200:
            try:
                venues = resp.json()
                st.dataframe(venues)
            except Exception as e_json:
                st.error(f"Received non-JSON response from backend: {e_json}")
        else:
            st.error(f"Error {resp.status_code}: {resp.text}")
    except Exception as e:
        st.warning(f"Backend not reachable. Is FastAPI running on port 8502? Error: {e}")

    # Add new venue form
    with st.form("new_venue"):
        st.write("### Add New Venue")
        name = st.text_input("Venue Name")
        location = st.text_input("Location")
        capacity = st.number_input("Capacity", min_value=10, step=10)
        description = st.text_area("Description")
        submitted = st.form_submit_button("Add Venue")
        if submitted:
            if name and location:
                payload = {
                    "name": name,
                    "location": location,
                    "capacity": int(capacity),
                    "description": description
                }
                try:
                    r = requests.post(f"{API_BASE}/venues/", json=payload)
                    if r.ok:
                        st.success("✓ Venue added!")
                        st.rerun()
                    else:
                        st.error(f"Error: {r.text}")
                except Exception as e:
                    st.error(f"Connection error: {e}")
            else:
                st.error("Please fill in required fields")

with tab2:
    st.subheader("Events")
    try:
        resp = requests.get(f"{API_BASE}/events/")
        if resp.status_code == 200:
            try:
                events = resp.json()
                st.dataframe(events)
            except Exception as e_json:
                st.error(f"Received non-JSON response from backend: {e_json}")
        else:
            st.error(f"Error {resp.status_code}: {resp.text}")
    except Exception as e:
        st.warning(f"Backend not reachable. Error: {e}")
    
    with st.form("new_event"):
        st.write("### Add New Event")
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            title = st.text_input("Event Title*", help="The main name of the event")
        
        with col2:
            # We'll fetch venues dynamically if possible
            # If you don't have an endpoint to list venues yet, you can hardcode or skip for now
            try:
                venues_response = requests.get(f"{API_BASE}/venues/")
                if venues_response.ok:
                    venues = venues_response.json()
                    venue_options = {v["name"]: v["id"] for v in venues}
                    venue_names = list(venue_options.keys())
                    
                    selected_venue_name = st.selectbox(
                        "Venue*", 
                        options=["Select a venue"] + venue_names,
                        index=0
                    )
                    
                    if selected_venue_name != "Select a venue":
                        venue_id = venue_options[selected_venue_name]
                    else:
                        venue_id = None
                else:
                    st.warning("Could not load venues")
                    venue_id = st.number_input("Venue ID*", min_value=1, step=1)
            except:
                st.warning("Could not connect to venue list")
                venue_id = st.number_input("Venue ID*", min_value=1, step=1)

        col_date, col_start, col_end = st.columns(3)
        
        with col_date:
            event_date = st.date_input(
                "Date*",
                value=datetime.today(),
                min_value=datetime.today()
            )
        
        with col_start:
            start_time = st.time_input("Start Time*", value=datetime.strptime("18:00", "%H:%M").time())
        
        with col_end:
            end_time = st.time_input("End Time*", value=datetime.strptime("22:00", "%H:%M").time())

        description = st.text_area(
            "Description",
            height=120,
            placeholder="What is this event about? Who should come? Any special notes..."
        )

        submitted = st.form_submit_button("Create Event", use_container_width=True, type="primary")

        if submitted:
            if not title.strip():
                st.error("Event title is required")
            elif not venue_id:
                st.error("Please select or enter a venue")
            elif start_time >= end_time:
                st.error("End time must be after start time")
            else:
                payload = {
                    "title": title.strip(),
                    "description": description.strip(),
                    "date": event_date.isoformat(),
                    "start_time": start_time.isoformat(),    # Time format HH:MM:SS
                    "end_time": end_time.isoformat(),        # Time format HH:MM:SS
                    "venue_id": int(venue_id),
                }

                try:
                    r = requests.post(f"{API_BASE}/events/", json=payload)
                    if r.ok:
                        st.success("✓ Event created successfully!")
                        # Optional: clear form / go to events list
                        st.rerun()
                    else:
                        try:
                            error_msg = r.json().get("detail", r.text)
                        except:
                            error_msg = r.text
                        st.error(f"API Error: {error_msg}")
                except requests.exceptions.RequestException as e:
                    st.error(f"Connection error: {str(e)}")
                except Exception as e:
                    st.error(f"Unexpected error: {str(e)}")
with tab3:
    st.subheader("Attendees")
    try:
        resp = requests.get(f"{API_BASE}/attendees/")
        if resp.status_code == 200:
            try:
                attendees = resp.json()
                st.dataframe(attendees)
            except Exception as e_json:
                st.error(f"Received non-JSON response from backend: {e_json}")
        else:
            st.error(f"Error {resp.status_code}: {resp.text}")
    except Exception as e:
        st.warning(f"Backend not reachable. Error: {e}")
with st.form("new_attendee"):
    st.write("### Register New Attendee")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input(
            "Full Name*",
            placeholder="e.g. Varisha Singh",
            help="As it should appear on tickets / badges"
        )

    with col2:
        email = st.text_input(
            "Email Address*",
            placeholder="varisha@example.com",
            help="Used for confirmation, updates & login (if applicable)"
        )

    # Interests - multi-select or free text (both common patterns)
    st.subheader("Interests / Preferences", divider="gray")

    # Option A: Predefined tags (recommended for better data quality)
    interest_options = [
        "Music", "Concerts", "Stand-up Comedy", "Tech Talks",
        "Workshops", "Food & Drinks", "Art & Culture", "Networking",
        "Electronic / DJ", "Indie / Alternative", "Classical", "Sports",
        "Business", "Startup", "Education", "Other"
    ]

    interests = st.multiselect(
        "What topics / event types interest you? (select all that apply)",
        options=interest_options,
        default=[],
        placeholder="Choose your interests...",
        help="Helps us recommend relevant events"
    )

    # Option B: free-text fallback (uncomment if you prefer / or use both)
    # custom_interests = st.text_input(
    #     "Other interests not listed above",
    #     placeholder="e.g. poetry, yoga, board games..."
    # )

    # Optional: phone, city, etc. — add only if your backend needs them
    # phone = st.text_input("Phone Number (optional)")
    # city = st.text_input("City (optional)")

    submitted = st.form_submit_button("Register Attendee", type="primary", use_container_width=True)

    if submitted:
        if not name.strip():
            st.error("Name is required")
        elif not email.strip():
            st.error("Email is required")
        elif "@" not in email or "." not in email.split("@")[-1]:
            st.error("Please enter a valid email address")
        else:
            payload = {
                "name": name.strip(),
                "email": email.strip().lower(),
                "interests": ", ".join([i.strip() for i in interests if i.strip()]),  # comma-separated string
                # "custom_interests": custom_interests.strip() if using free text
                # "phone": phone.strip() or None,
                # "city": city.strip() or None,
            }

            try:
                response = requests.post(
                    f"{API_BASE}/attendees/",
                    json=payload,
                    timeout=10
                )

                if response.ok:
                    try:
                        created = response.json()
                        attendee_id = created.get("id")
                        st.success(f"✓ Attendee registered successfully!")
                        if attendee_id:
                            st.info(f"Attendee ID: **{attendee_id}**")
                    except:
                        st.success("✓ Attendee registered!")
                    
                    # Clear form / refresh
                    st.rerun()

                else:
                    try:
                        error_detail = response.json().get("detail", response.text)
                    except:
                        error_detail = response.text
                    st.error(f"Error: {error_detail}")

            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to the server. Please check your internet or contact support.")
            except requests.exceptions.Timeout:
                st.error("Request timed out. Please try again.")
            except Exception as e:
                st.error(f"Unexpected error: {str(e)}")
with tab4:
    st.subheader("AI Event Recommendations")
    st.write("Get AI-powered event recommendations for an attendee")
    
    attendee_id = st.number_input("Attendee ID", min_value=1, step=1)
    if st.button("Get AI Recommendations"):
        try:
            r = requests.get(f"{API_BASE}/ai/recommend-events/{attendee_id}")
            if r.ok:
                try:
                    result = r.json()
                except Exception as e_json:
                    st.error(f"Received non-JSON response from backend: {e_json}")
                    result = {}
                st.markdown(f"**Attendee:** {result.get('attendee', 'Unknown')}")
                st.markdown("**Recommendations:**")
                for rec in result.get('recommendations', []):
                    with st.container(border=True):
                        st.write(f"📌 **{rec['title']}** (ID: {rec['event_id']})")
                        st.write(f"Match Score: {rec['match_score']}/10")
                        st.write(f"Reason: {rec['reason']}")
            else:
                st.error(f"Error: {r.text}")
        except Exception as e:
            st.error(f"Connection error: {e}")
