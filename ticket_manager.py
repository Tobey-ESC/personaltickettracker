import streamlit as st
import sqlite3
import datetime
from urllib.parse import urlparse
import requests
import math
import time

# Set page config at the very beginning
st.set_page_config(page_title="Ticket Tracker", page_icon="🎫", layout="wide")

# Database setup
conn = sqlite3.connect('tickets.db')
c = conn.cursor()

# Define category options
category_options = ["Approvals", "Billing", "Cancellations", "Deliverability"]

# Initialize session state variables
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False
if 'expanded_ticket' not in st.session_state:
    st.session_state.expanded_ticket = None
if 'page' not in st.session_state:
    st.session_state.page = 1

# Loading animation function
def show_loading_animation():
    with st.spinner('Loading...'):
        time.sleep(1)  # Simulate some processing time

# Function to check if a URL is valid
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

# Function to check if a ticket with the given link already exists
def ticket_link_exists(link):
    c.execute("SELECT COUNT(*) FROM tickets WHERE link = ?", (link,))
    return c.fetchone()[0] > 0

# Function to add a ticket to the database
def add_ticket(title, category, link, lead_comment, action_plan, other_details):
    created_at = datetime.datetime.now()
    c.execute("INSERT INTO tickets (title, category, link, lead_comment, action_plan, other_details, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (title, category, link, lead_comment, action_plan, other_details, created_at))
    conn.commit()
    return created_at

# Function to update a ticket in the database
def update_ticket_in_db(ticket_id, title, category, link, lead_comment, action_plan, other_details):
    c.execute("""UPDATE tickets 
                 SET title=?, category=?, link=?, lead_comment=?, action_plan=?, other_details=?
                 WHERE id=?""",
              (title, category, link, lead_comment, action_plan, other_details, ticket_id))
    conn.commit()

# Function to save ticket
def save_ticket(title, category, link, lead_comment, action_plan, other_details):
    if is_valid_url(title):
        st.error("Ticket title should not be a URL.")
    elif not is_valid_url(link):
        st.error("Please enter a valid URL for the ticket link.")
    elif not title or not category or not link:
        st.error("Please fill in the required fields (Title, Category, and Link).")
    elif ticket_link_exists(link):
        st.error("A ticket with this link already exists. Please update the existing ticket instead.")
    else:
        show_loading_animation()
        created_at = add_ticket(title, category, link, lead_comment, action_plan, other_details)
        st.success(f"Ticket saved successfully at {created_at}!")
        st.session_state.form_submitted = True

# Function to update ticket
def update_ticket(ticket_id, title, category, link, lead_comment, action_plan, other_details):
    if not ticket_id:
        st.error("Please select a ticket to update first.")
    elif is_valid_url(title):
        st.error("Ticket title should not be a URL.")
    elif not is_valid_url(link):
        st.error("Please enter a valid URL for the ticket link.")
    elif not title or not category or not link:
        st.error("Please fill in the required fields (Title, Category, and Link).")
    else:
        show_loading_animation()
        update_ticket_in_db(ticket_id, title, category, link, lead_comment, action_plan, other_details)
        st.success(f"Ticket updated successfully!")
        st.session_state.form_submitted = True

# Function to get paginated tickets
def get_paginated_tickets(page, per_page, search_term="", category=""):
    offset = (page - 1) * per_page
    query = "SELECT * FROM tickets WHERE 1=1"
    params = []
    if search_term:
        query += " AND (title LIKE ? OR category LIKE ?)"
        params.extend([f"%{search_term}%", f"%{search_term}%"])
    if category:
        query += " AND category = ?"
        params.append(category)
    query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
    params.extend([per_page, offset])
    c.execute(query, params)
    return c.fetchall()

# Function to get total number of tickets
def get_total_tickets(search_term="", category=""):
    query = "SELECT COUNT(*) FROM tickets WHERE 1=1"
    params = []
    if search_term:
        query += " AND (title LIKE ? OR category LIKE ?)"
        params.extend([f"%{search_term}%", f"%{search_term}%"])
    if category:
        query += " AND category = ?"
        params.append(category)
    c.execute(query, params)
    return c.fetchone()[0]

# Function to delete a specific ticket
def delete_ticket(ticket_id):
    show_loading_animation()
    c.execute("DELETE FROM tickets WHERE id = ?", (ticket_id,))
    conn.commit()

# Function to delete all tickets
def delete_all_tickets():
    show_loading_animation()
    c.execute("DELETE FROM tickets")
    conn.commit()

# Main app
def main():
    # CSS for styling
    st.markdown("""
    <style>
        @keyframes ripple {
            0% {
                transform: scale(0.8);
                opacity: 1;
            }
            100% {
                transform: scale(2.4);
                opacity: 0;
            }
        }
        .status-indicator {
            height: 10px;
            width: 10px;
            border-radius: 50%;
            display: inline-block;
            position: relative;
        }
        .status-indicator::before,
        .status-indicator::after {
            content: "";
            display: block;
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            border-radius: 50%;
            animation: ripple 3s linear infinite;
        }
        .status-indicator::after {
            animation-delay: -1.5s;
        }
        .status-red {
            background-color: red;
        }
        .status-red::before,
        .status-red::after {
            border: 1px solid red;
        }
        .status-green {
            background-color: green;
        }
        .status-green::before,
        .status-green::after {
            border: 1px solid green;
        }
        /* Theme-dependent styles */
        @media (prefers-color-scheme: dark) {
            .status-indicator::before,
            .status-indicator::after {
                border-color: white;
            }
        }
        @media (prefers-color-scheme: light) {
            .status-indicator::before,
            .status-indicator::after {
                border-color: black;
            }
        }
        
        .stSpinner > div {
            border-top-color: #5389a6 !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # Title
    st.markdown('<h1 class="title">Ticket Tracker</h1>', unsafe_allow_html=True)

    # Add/Update ticket section
    st.markdown('<h2 class="subtitle">Add/Update Ticket</h2>', unsafe_allow_html=True)

    # Input fields
    ticket_link = st.text_input("Ticket Link")
    ticket_title = st.text_input("Ticket Title")
    ticket_category = st.selectbox("Category", category_options)
    lead_comment = st.text_area("Lead's Comment")
    action_plan = st.text_area("Action Plan")
    other_details = st.text_area("Other Details")

    # Save and Update buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Save Ticket"):
            save_ticket(ticket_title, ticket_category, ticket_link, lead_comment, action_plan, other_details)

    with col2:
        if st.button("Update Ticket"):
            update_ticket(st.session_state.expanded_ticket[0] if st.session_state.expanded_ticket else None,
                          ticket_title, ticket_category, ticket_link, lead_comment, action_plan, other_details)

    if st.session_state.form_submitted:
        st.session_state.form_submitted = False
        st.experimental_rerun()

    # All Tickets header
    st.markdown('<h2 class="subtitle">All Tickets</h2>', unsafe_allow_html=True)

    # Search and filter
    search_term = st.text_input("Search tickets by title or category", key="search_input")
    category_filter = st.selectbox("Filter by category", [""] + category_options, key="category_filter")

    # Pagination
    tickets_per_page = 6
    total_tickets = get_total_tickets(search_term, category_filter)
    total_pages = math.ceil(total_tickets / tickets_per_page)

    # Ensure current page is valid
    st.session_state.page = min(st.session_state.page, max(1, total_pages))

    # Display paginated tickets with animated indicators
    tickets = get_paginated_tickets(st.session_state.page, tickets_per_page, search_term, category_filter)

    for ticket in tickets:
        col1, col2, col3 = st.columns([0.1, 3.3, 0.1])
        
        with col1:
            if ticket[5].strip():  # Check if action_plan is not empty
                st.markdown('<div class="status-indicator status-green"></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="status-indicator status-red"></div>', unsafe_allow_html=True)
        
        with col2:
            if st.button(f"{ticket[1]} ({ticket[2]})", key=f"view_{ticket[0]}"):
                if st.session_state.expanded_ticket == ticket:
                    st.session_state.expanded_ticket = None
                else:
                    st.session_state.expanded_ticket = ticket
                st.experimental_rerun()

        with col3:
            if st.button("❌", key=f"remove_{ticket[0]}"):
                delete_ticket(ticket[0])
                st.success(f"Successfully removed the ticket.")
                st.experimental_rerun()

        # Display ticket details if expanded
        if st.session_state.expanded_ticket == ticket:
            st.markdown("---")
            st.markdown(f"**Title:** {ticket[1]}")
            st.markdown(f"**Category:** {ticket[2]}")
            st.markdown(f"**Link:** [{ticket[3]}]({ticket[3]})")
            st.markdown(f"**Lead's Comment:** {ticket[4]}")
            st.markdown(f"**Action Plan:** {ticket[5]}")
            st.markdown(f"**Other Details:** {ticket[6]}")
            st.markdown(f"**Created At:** {ticket[7]}")
            st.markdown("---")

    # Pagination controls
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        if st.button("⏪ First", key="first_page_button") and st.session_state.page != 1:
            st.session_state.page = 1
            st.experimental_rerun()
    with col2:
        if st.button("◀️ Previous", key="previous_page_button") and st.session_state.page > 1:
            st.session_state.page -= 1
            st.experimental_rerun()
    with col3:
        if st.button("Next ▶️", key="next_page_button") and st.session_state.page < total_pages:
            st.session_state.page += 1
            st.experimental_rerun()
    with col4:
        if st.button("Last ⏩", key="last_page_button") and st.session_state.page != total_pages:
            st.session_state.page = total_pages
            st.experimental_rerun()

    st.write(f"Page {st.session_state.page} of {total_pages}")

    # Add a "Remove All Tickets" button
    if st.button("Remove All Tickets"):
        delete_all_tickets()
        st.success("Successfully removed all tickets.")
        st.experimental_rerun()

if __name__ == "__main__":
    main()