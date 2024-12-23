# YouTube Data Harvesting and Warehousing

A **Streamlit application** designed to allow users to access and analyze data from multiple YouTube channels with ease.

## Project Overview

### Developer Information:
- **Name**: Vinoth Kumar S
- **Batch**: DTM-2
- **Domain**: Data Science

### Application Features:

1. **Retrieve YouTube Channel Data**:
   - Input a YouTube channel ID and fetch relevant data using the Google YouTube API.
   - Data includes:
     - Channel name
     - Subscriber count
     - Total video count
     - Playlist ID
     - Video details (ID, likes, dislikes, comments, etc.)

2. **Store Data in MongoDB Data Lake**:
   - Save retrieved data into a MongoDB database.
   - Collect data for up to **10 YouTube channels** and store it in a data lake with a single click.

3. **Migrate Data to SQL Database**:
   - Migrate selected channel data from the MongoDB data lake to a SQL database.
   - Organize data into structured tables.

4. **Search and Query SQL Database**:
   - Use advanced search options to retrieve data from the SQL database.
   - Perform SQL joins to access detailed channel insights.

5. **Streamlit App Integration**:
   - Display all retrieved and analyzed data in an interactive Streamlit app.
   - User-friendly interface for data visualization and interaction.

## Technical Stack

### APIs and Libraries:
- **YouTube API**: Retrieve channel and video data.
- **Google API Client for Python**: Simplify API requests.
- **MongoDB**: Store unstructured and semi-structured data.
- **SQL Database**: Use MySQL or PostgreSQL for data warehousing.
- **SQLAlchemy**: Interact with the SQL database in Python.
- **Streamlit**: Build an interactive user interface.

## Configuration

1. Open the `file.py` in the project directory.
2. Configure the following:
   - YouTube API key.
   - Database connection details for both SQL and MongoDB.
   - Provide the YouTube Channel ID to harvest data.
3. Modify additional settings as required.

## Usage Guide

1. **Launch the App**:
   - Run the command: `streamlit run file.py`.
   - Ensure `file.py` and SQL files are in the same folder.
2. **Explore Data**:
   - Input a YouTube Channel ID to fetch data.
   - View the harvested data and visualizations in the browser.

## Contribution Guidelines

Contributions are always welcome! Follow these steps to contribute:

1. **Fork the Repository**.
2. **Create a New Branch**:
   ```
   git checkout -b feature/your-feature-name
   ```
3. **Commit Your Changes**:
   ```
   git commit -m "Add your commit message here"
   ```
4. **Push Your Branch**:
   ```
   git push origin feature/your-feature-name
   ```
5. **Open a Pull Request**:
   - Provide a clear explanation of your changes and why they should be merged.

---

**Explore the power of YouTube data harvesting with this streamlined application!**
