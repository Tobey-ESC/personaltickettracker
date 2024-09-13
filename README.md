Personal Ticket Tracker

Web application built with Streamlit that helps manage and track tickets, providing an intuitive interface for creating, updating, and monitoring tickets across various categories.

## Features

- **Create Tickets**: Easily add new tickets with details such as title, category, link, lead's comment, action plan, and other relevant information.
- **Update Tickets**: Modify existing ticket information as the status changes or more details become available.
- **View Ticket Details**: Click on any ticket to expand and view its full details.
- **Delete Tickets**: Remove individual tickets or clear all tickets at once.
- **Prevent Duplicates**: The app checks for existing ticket links to avoid duplicate entries.
- **Search and Filter**: Quickly find tickets using the search function or filter by category.
- **Pagination**: Navigate through tickets with an easy-to-use pagination system.
- **Visual Status Indicators**: Each ticket displays a color-coded status indicator (green or red) based on the presence of an action plan.
- **Loading Animations**: Visual feedback during operations like saving, updating, or deleting tickets.
- **Responsive Design**: The app adapts to different screen sizes for a consistent experience across devices.

## Setup and Installation

1. Clone this repository:
   ```
   git clone https://github.com/your-username/ticket-tracker.git
   cd ticket-tracker
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```
   streamlit run ticket_manager.py
   ```

4. Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

## Usage

1. **Adding a Ticket**: Fill in the ticket details in the form at the top of the page and click "Save Ticket".
2. **Updating a Ticket**: Click on an existing ticket, modify the details in the form, and click "Update Ticket".
3. **Viewing Ticket Details**: Click on a ticket in the list to expand and view its full details.
4. **Deleting a Ticket**: Click the "❌" button next to a ticket to remove it.
5. **Removing All Tickets**: Use the "Remove All Tickets" button at the bottom of the page to clear all tickets.
6. **Searching Tickets**: Enter keywords in the search box to find specific tickets.
7. **Filtering by Category**: Use the category dropdown to filter tickets by a specific category.
8. **Navigating Pages**: Use the pagination controls at the bottom to move between pages of tickets.

## Contributing

Contributions to improve Ticket Tracker are welcome. Please feel free to submit a Pull Request.

## License

[Specify your license here, e.g., MIT License]
