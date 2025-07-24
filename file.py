import streamlit as st
from streamlit_option_menu import option_menu
import pymongo as py
import pandas as pd
import plotly.express as px
import mysql.connector as sql
from googleapiclient.discovery import build
from datetime import datetime
from streamlit import *
from streamlit_lottie import st_lottie
import json as js
import requests
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

pd.set_option('display.max_columns', None)

# Set page configuration and title
st.set_page_config(page_title="YouTube Data Harvesting and Warehousing | by vinothkumar", layout="wide")

# option menu 


selected = option_menu(
    menu_title="Youtupe Analysis",
    options=['Home', 'Migrate and Store', 'View'],
    icons=['mic-fill', 'cash-stack', 'phone-flip'],
    menu_icon='alexa',
    default_index=0,
)



# Connect to databases (MongoDB, MySQL)
# MongoDB
vinoth = py.MongoClient("mongodb://localhost:27017/")
db = vinoth["youtube_channel_data"]



# MySQL
mydb = sql.connect(host="localhost",
                  user="root",
                  password="vino8799",
                  database="youtube_project")
cursor = mydb.cursor()



# Build a connection with the YouTube API to access channel data
# API Key
api_key = "AIzaSyBmP4LvAdSLp_FttkA78tfNOSBjsInYRgc"



# Build access service
youtube = build("youtube", "v3", developerKey=api_key)



# Function to get channel details
def channel_details(channel_id):
    channel_data = []
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=channel_id)
    response = request.execute()

    for i in range(len(response["items"])):
        data = {
            "channel_id": channel_id,
            "channel_name": response["items"][i]["snippet"]["title"],
            "channel_description": response["items"][i]["snippet"]["description"],
            "subscribers": response["items"][i]["statistics"]["subscriberCount"],
            "channel_views": response["items"][i]["statistics"]["viewCount"],
            "channel_total_videos": response["items"][i]["statistics"]["videoCount"],
            "playlist_id": response["items"][i]["contentDetails"]["relatedPlaylists"]["uploads"],
            "channel_country": response["items"][i]["snippet"].get("country")
        }
        channel_data.append(data)

    return channel_data


# Get the upload playlist ID to get video details
def get_video_ids(channel_id):
    video_ids = []
    request = youtube.channels().list(
        part="contentDetails",
        id=channel_id)
    response = request.execute()
    playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    next_page_token = None

    while True:
        request = youtube.playlistItems().list(
            playlistId=playlist_id,
            part="contentDetails",
            maxResults=50,
            pageToken=next_page_token).execute()

        for i in range(len(request["items"])):
            video_ids.append(request["items"][i]["contentDetails"]["videoId"])
            next_page_token = request.get("nextPageToken")

        if next_page_token is None:
            break

    return video_ids

# Function to get video details
def get_video_details(video_ids):
    video_data = []
    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=",".join(video_ids[i:i+50])).execute()
        for video in request["items"]:
            video_details = {
                "channel_name": video['snippet']["channelTitle"],
                "channel_id": video["snippet"]["channelId"],
                "video_id": video["id"],
                "title": video["snippet"]["title"],
                "tags": video["snippet"].get("tags", []),
                "thumbnail": video["snippet"]["thumbnails"]["default"]["url"],
                "Description": video['snippet']['description'],
                "Published_date": video['snippet']['publishedAt'],
                "Duration": video['contentDetails']['duration'],
                "Views": video['statistics']['viewCount'],
                "Likes": video['statistics'].get('likeCount'),
                "Comments": video['statistics'].get('commentCount'),
                "Favorite_count": video['statistics']['favoriteCount'],
                "Definition": video['contentDetails']['definition'],
                "Caption_status": video['contentDetails']['caption']
            }
            video_data.append(video_details)
    return video_data

# Function to get channel name in MongoDB
def get_channel_name():
    channel_names = []
    for doc in db.channel_details.find():
        channel_names.append({"channel_name": doc["channel_name"]})
    return channel_names


#Lottie file viwer function
def lottie(filepath):
    with open(filepath, 'r') as file:
        return js.load(file)
                        
if selected == 'Home':

    def load_lottieurl(url):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    # Use local CSS
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    

    lottie_coding = lottie(r"V:\VKfusion\LOTTIE FILE\Intro .json")


    # ---- HEADER SECTION -----``
    with st.container():
        col1,col2=st.columns(2)
        with col1:
            st.markdown( f"<h1 style='font-size: 70px;'><span style='color: #00BFFF;'> Hi,  </span><span style='color: white;'> I am vinoth kumar </h1>",unsafe_allow_html=True)
            st.markdown(
                f"<h1 style='font-size: 40px;'><span style='color: white;'>A Data Scientist,</span><span style='color: #00BFFF;'> From India</span></h1>",
                unsafe_allow_html=True
                )
            st.write(f'<h1 style="color:#B0C4DE; font-size: 20px;">A data scientist skilled in extracting actionable insights from complex datasets, adept at employing advanced analytics and machine learning techniques to solve real-world problems. Proficient in Python, statistical modeling, and data visualization, with a strong commitment to driving data-driven decision-making.</h1>', unsafe_allow_html=True)    

            st.write("[view more projects >](https://github.com/Vk-lap?tab=repositories)")

        with col2:
            st_lottie(lottie_coding, height=400, key="coding")    

    # ---- WHAT I DO ----
    with st.container():
        st.write("---")
        col1,col2,col3=st.columns(3)

        with col1:
            file = lottie(r"V:\VKfusion\LOTTIE FILE\data science.json")
            st_lottie(file,height=300,key=None)

        with col2:
            st.markdown( f"<h1 style='font-size: 70px;text-align: center;'><span style='color: #00BFFF;'> WHAT  </span><span style='color: white;'> I DO </h1>",unsafe_allow_html=True)
            file=lottie(r'V:\VKfusion\LOTTIE FILE\icon toutupe.json')
            st_lottie(file,height=500,key=None)
        with col3:
            file = lottie(r"V:\VKfusion\LOTTIE FILE\Working.json")
            st_lottie(file,height=300,key=None)    
        
        st.markdown( f"<h1 style='font-size: 40px;'><span style='color: #00BFFF;'>Retrieving data from the  </span><span style='color: white;'>YouTube API</h1>",unsafe_allow_html=True)
        st.write(f'<h1 style="color:#B0C4DE; font-size: 30px;">utilizes the Google API to retrieve comprehensive data from YouTube channels. The data includes information on channels, playlists, videos, and comments.</h1>', unsafe_allow_html=True)
    
        st.markdown( f"<h1 style='font-size: 40px;'><span style='color: #00BFFF;'> Store Data in  </span><span style='color: white;'>MongoDB-Atlas Cloud</h1>",unsafe_allow_html=True)
        st.write(f'<h1 style="color:#B0C4DE; font-size: 30px;">Retrieved data is stored in a MongoDB database based on user authorization. If the data already exists in the database, it can be overwritten with user consent. This storage process ensures efficient data management and preservation, allowing for seamless handling of the collected data.</h1>', unsafe_allow_html=True) 

        st.markdown( f"<h1 style='font-size: 40px;'><span style='color: #00BFFF;'> Migrating data to a  </span><span style='color: white;'>MYSQL data warehouse</h1>",unsafe_allow_html=True)
        st.write(f'<h1 style="color:#B0C4DE; font-size: 30px;">Migrate data from MongoDB to a SQL data warehouse. Then choose which channels data to migrate. To ensure compatibility with a structured format, the data is cleansed using the powerful pandas library. Following data cleaning, the information is segregated into separate tables, including channels, playlists, videos, and comments, utilizing SQL queries.</h1>', unsafe_allow_html=True)

        st.markdown( f"<h1 style='font-size: 40px;'><span style='color: #00BFFF;'> Data   </span><span style='color: white;'>Analysis</h1>",unsafe_allow_html=True)
        st.write(f'<h1 style="color:#B0C4DE; font-size: 30px;">provides comprehensive data analysis capabilities using Plotly and Streamlit. With the integrated Plotly library, users can create interactive and visually appealing charts and graphs to gain insights from the collected data.</h1>', unsafe_allow_html=True)

        st.markdown( f"<h1 style='font-size: 40px;'><span style='color: #00BFFF;'> Interactive  </span><span style='color: white;'>Streamlit UI</h1>",unsafe_allow_html=True)
        st.write(f'<h1 style="color:#B0C4DE; font-size: 30px;">Crafted an engaging and user-friendly interface for seamless data exploration and presentation.</h1>', unsafe_allow_html=True)

        
        st.markdown("[🔗 GitHub Repo >](https://github.com/Vk-lap/YouTube-Data-Harvesting-and-Warehousing.git)")    



    with st.container():
        st.write("---")
        st.markdown( f"<h1 style='font-size: 40px;'><span style='color: #00BFFF;'> Used-Tech  </span><span style='color: white;'>& Skills</h1>",unsafe_allow_html=True)

        col1,col2,col3 =st.columns(3)
        with col1:
            
            file = lottie(r"V:\VKfusion\LOTTIE FILE\Python.json")
            st.markdown("<h1 style='color: #00BFFF; text-align: center; font-size: 30px;'>python</h1>", unsafe_allow_html=True)
            st_lottie(file,height=200,key=None)

            file = lottie(r"V:\VKfusion\LOTTIE FILE\Mongo db.json")
            st.markdown("<h1 style='color: #00BFFF; text-align: center; font-size: 30px;'>Mongo-DB</h1>", unsafe_allow_html=True)
            st_lottie(file,height=200,key=None)

            file = lottie(r"V:\VKfusion\LOTTIE FILE\Data Exploration.json")
            st.markdown("<h1 style='color: #00BFFF; text-align: center; font-size: 30px;'>Data Exploaration</h1>", unsafe_allow_html=True)
            st_lottie(file,height=200,key=None)

        with col2:

            file = lottie(r"V:\VKfusion\LOTTIE FILE\ABI integration.json")
            st.markdown("<h1 style='color: #00BFFF; text-align: center; font-size: 30px;'>API Integration</h1>", unsafe_allow_html=True)
            st_lottie(file,height=200,key=None)

            file = lottie(r"V:\VKfusion\LOTTIE FILE\data fetch.json")
            st.markdown("<h1 style='color: #00BFFF; text-align: center; font-size: 30px;'>Data Fetching</h1>", unsafe_allow_html=True)
            st_lottie(file,height=200,key=None)

            file = lottie(r"V:\VKfusion\LOTTIE FILE\Data Base.json")
            st.markdown("<h1 style='color: #00BFFF; text-align: center; font-size: 30px;'>DataBase</h1>", unsafe_allow_html=True)
            st_lottie(file,height=200,key=None)

            

        with col3:    
            file = lottie(r"V:\VKfusion\LOTTIE FILE\Data Collection.json")
            st.markdown("<h1 style='color: #00BFFF; text-align: center; font-size: 30px;'>Data Collection</h1>", unsafe_allow_html=True)
            st_lottie(file,height=200,key=None)

            file = lottie(r"V:\VKfusion\LOTTIE FILE\Data Cleaning.json")
            st.markdown("<h1 style='color: #00BFFF; text-align: center; font-size: 30px;'>Data Cleaning</h1>", unsafe_allow_html=True)
            st_lottie(file,height=200,key=None)

            file = lottie(r"V:\VKfusion\LOTTIE FILE\Frame work.json")
            st.markdown("<h1 style='color: #00BFFF; text-align: center; font-size: 30px;'>Web application development with Streamlit</h1>", unsafe_allow_html=True)
            st_lottie(file,height=200,key=None)


            
       

    # ---- PROJECTS ----
    with st.container():
        st.write("---")
        st.markdown( f"<h1 style='font-size: 70px;'><span style='color: #00BFFF;'> About  </span><span style='color: white;'> Projects </h1>",unsafe_allow_html=True)
        col1,col2=st.columns(2)
        with col1:
            file = lottie(r"V:\VKfusion\LOTTIE FILE\Youtupe icon.json")
            st_lottie(file,height=300,key=None)
        with col2:
            st.write("##")
            st.write(f'<h1 style="color:#B0C4DE; font-size: 30px;">YouTube Data Harvesting and Warehousing is a project aimed at developing a user-friendly Streamlit application that leverages the power of the Google API to extract valuable information from YouTube channels. The extracted data is then stored in a MongoDB database, subsequently migrated to a SQL data warehouse, and made accessible for analysis and exploration within the Streamlit app.</h1>', unsafe_allow_html=True)
        st.markdown( f"<h1 style='font-size: 70px;'><span style='color: #00BFFF;'> Re</span><span style='color: white;'>sults</h1>",unsafe_allow_html=True)
        st.write(f'<h1 style="color:#B0C4DE; font-size: 30px;">The project provides a user-friendly interface for exploring Youtupe channel Data.</h1>', unsafe_allow_html=True)    
        

    # ---- CONTACT ----
    with st.container():
        st.write("---")
        st.markdown( f"<h1 style='font-size: 70px;'><span style='color: #00BFFF;'> Get In Touch  </span><span style='color: white;'> With Me </h1>",unsafe_allow_html=True)
        st.write("##")

        # Documention: https://formsubmit.co/ !!! CHANGE EMAIL ADDRESS !!!
        contact_form = """
        <form action="https://formsubmit.co/vinoharish8799@gmail.com" method="POST">
            <input type="hidden" name="_captcha" value="false">
            <input type="text" name="name" placeholder="Your name" required>
            <input type="email" name="email" placeholder="Your email" required>
            <textarea name="message" placeholder="Your message here" required></textarea>
            <button type="submit" style="background-color: #00BFFF; color: white;">Send</button>
        </form>
        """
        left_column, right_column = st.columns(2)
        with left_column:
            st.markdown(contact_form, unsafe_allow_html=True)
        with right_column:
            st.empty()



if selected == "Migrate and Store":


    option = option_menu(menu_title='', options=['EXTRACT', 'TRANSFORM'],
                         icons=['database-fill', 'list-task'],
                         default_index=0, orientation="horizontal")

    if button and option == 'EXTRACT':

        col1,col2=st.columns(2)
        with col1:
            file = lottie(r"V:\VKfusion\LOTTIE FILE\File Transfer.json")
            st_lottie(file,height=300,key=None)
        with col2:
            st.write("")
            st.write("")
            st.write("")
            st.markdown( f"<h1 style='font-size: 40px;'><span style='color: #00BFFF;'> Data Migration </span><span style='color: white;'>section </h1>",unsafe_allow_html=True)
        
        st.markdown( f"<h1 style='font-size: 40px;'><span style='color: #00BFFF;'> Enter your  </span><span style='color: white;'>channel_id </h1>",unsafe_allow_html=True)
        channel_id = st.text_input("Enter")
        
        if channel_id and st.button("Extract"):
            channel_data = channel_details(channel_id)
            df = pd.DataFrame(channel_data)
            st.table(df)
        
        if channel_id and st.button("Upload to MongoDB"):
            st.spinner(text="In progress...")
            channel_list = channel_details(channel_id)
            video_ids = get_video_ids(channel_id)
            videos_data = get_video_details(video_ids)
            
            cll1 = db["channel_details"]
            cll1.insert_many(channel_list)

            cll2 = db["video_data"]
            cll2.insert_many(videos_data)

            st.markdown('<p style="color:lightgreen;">Successfully uploaded to MongoDB</p>', unsafe_allow_html=True)
            st.write("Our cloud storage system is MongoDB Atlas")

    # TRANSFORM TAB
    if button and option == 'TRANSFORM':  
        col1,col2=st.columns(2)
        with col1:
            file = lottie(r"V:\VKfusion\LOTTIE FILE\sql db.json")
            st_lottie(file,height=300,key=None)
        with col2:
            st.write("")
            st.write("")
            st.write("")
            st.markdown( f"<h1 style='font-size: 40px;'><span style='color: #00BFFF;'> Data store </span><span style='color: white;'>section </h1>",unsafe_allow_html=True)

        st.markdown("# Transformation")
        st.markdown("Select a channel to begin the transformation to SQL")
        ch_names = get_channel_name()
        user_inp = st.selectbox("Select channel", options=ch_names)

    def insert_into_channels():
        coll_channel=db.channel_details                          
        query = "INSERT INTO channel_details (channel_id, channel_name, channel_description, subscribers, channel_views, channel_total_videos, playlist_id, channel_country) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        for channel in coll_channel.find(user_inp):
            values = (channel["channel_id"],
                      channel["channel_name"], 
                      channel["channel_description"], 
                      channel["subscribers"], 
                      channel["channel_views"], 
                      channel["channel_total_videos"], 
                      channel["playlist_id"], 
                      channel["channel_country"])
            cursor.execute(query, values)
            mydb.commit()

            
    def insert_into_videos():
        coll_video=db.video_data
        for document in coll_video.find(user_inp):
            published_date = datetime.strptime(document['Published_date'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d %H:%M:%S')
            caption_status = 0 if document['Caption_status'].lower() == 'false' else 1
            comments = document['Comments']
    # Map MongoDB document fields to MySQL table columns
            data = {
                'channel_name': document['channel_name'],
                'channel_id': str(document['channel_id']),
                'video_id': document['video_id'],
                'title': document['title'],
                'thumbnail': document['thumbnail'],
                'Description': document['Description'],
                'Published_date': published_date,
                'Duration': document['Duration'],
                'Views': int(document['Views']),
                'Likes': int(document['Likes']),
                'Comments': int(comments) if comments is not None else 0,
                'Favorite_count': int(document['Favorite_count']),
                'Definition': document['Definition'],
                'Caption_status': caption_status
                }

    # Insert data into MySQL
            cursor.execute("""
                           INSERT INTO video_details
                           (channel_name, channel_id, video_id, title, thumbnail, Description, Published_date, Duration, Views, Likes, Comments, Favorite_count, Definition, Caption_status)
                           VALUES (%(channel_name)s, %(channel_id)s, %(video_id)s, %(title)s, %(thumbnail)s, %(Description)s, %(Published_date)s, %(Duration)s, %(Views)s, %(Likes)s, %(Comments)s, %(Favorite_count)s, %(Definition)s, %(Caption_status)s)
                           """, data)

# Commit changes and close connections
            mydb.commit()


    if st.button("Submit"):
        with st.spinner("Inserting data to MySQL..."):
            insert_into_channels()
            insert_into_videos()
        st.success("Successfully  to MySQL!")


# VIEW PAGE
if selected == "View":

    col1,col2=st.columns(2)
    with col1:
        file=lottie(r"V:\VKfusion\LOTTIE FILE\Working.json")
        st_lottie(file,height=300,key=None)

    with col2:
        st.markdown( f"<h1 style='font-size: 40px;'><span style='color: #00BFFF;'> Data Insight </span><span style='color: white;'>Report</h1>",unsafe_allow_html=True)
        st.write("##")
    st.markdown( f"<h1 style='font-size: 40px;'><span style='color: #00BFFF;'> Select any question </span><span style='color: white;'>to get Insights </h1>",unsafe_allow_html=True)
   
    questions = st.selectbox('Questions',
                             
    ['1. What are the names of all the videos and their corresponding channels?',
    '2. Which channels have the most number of videos, and how many videos do they have?',
    '3. What are the top 10 most viewed videos and their respective channels?',
    '4. How many comments were made on each video, and what are their corresponding video names?',
    '5. Which videos have the highest number of likes, and what are their corresponding channel names?',
    '6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?',
    '7. What is the total number of views for each channel, and what are their corresponding channel names?',
    '8. What are the names of all the channels that have published videos in the year 2022?',
    '9. What is the duration of top_10 videos in each channel, and what are their corresponding channel names?',
    '10. Which videos have the highest number of comments, and what are their corresponding channel names?'])
    
    if questions == '1. What are the names of all the videos and their corresponding channels?':
        cursor.execute("""SELECT title AS Video_name, channel_name AS Channel_Name
                            FROM video_details
                            ORDER BY channel_name""")
        df = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        # Plotting the vertical bar chart for the distribution of videos across channels using Plotly
        videos_per_channel = df.groupby('Channel_Name')['Video_name'].count().reset_index(name='count')

        col1,col2=st.columns(2)
        with col1:
            fig = px.bar(videos_per_channel, x='Channel_Name', y='count', text='count', color='Channel_Name',
                         title='Distribution of Videos Across Channels', labels={'Channel_Name': 'Channel Name'})
        
            fig.update_layout(width=800, height=600)
            st.plotly_chart(fig)
        with col2:
            if isinstance(df, pd.DataFrame):
                st.dataframe(df)


    elif questions == '2. Which channels have the most number of videos, and how many videos do they have?':
        cursor.execute("""SELECT channel_name AS Channel_Name, channel_total_videos AS Total_Videos
                            FROM channel_details
                            ORDER BY total_videos DESC limit 1""")
        df = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        col1,col2=st.columns(2)

        with col1:
            st.dataframe(df)
        
        #st.bar_chart(df,x= mycursor.column_names[0],y= mycursor.column_names[1])
        with col2:
            fig = px.bar(df,
                         x=cursor.column_names[0],
                         y=cursor.column_names[1],
                         orientation='v',
                         color=cursor.column_names[0]
                         )
            st.plotly_chart(fig,use_container_width=True)
        
    elif questions == '3. What are the top 10 most viewed videos and their respective channels?':
        cursor.execute("""SELECT channel_name AS Channel_Name, title AS Video_Title, views AS Views 
                            FROM video_details
                            ORDER BY views DESC
                            LIMIT 10""")
        df = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        st.dataframe(df)
        st.write("### :white[Top 10 most viewed videos :]")
        
        # Advanced visualization using Plotly
        fig = px.bar(df,
                     x='Views',
                     y='Video_Title',
                     orientation='h',
                     color='Channel_Name',
                     labels={'Channel_Name': 'Channel Name', 'Video_Title': 'Video Title'},
                     title='Top 10 Most Viewed Videos and Their Respective Channels',
                     )
        fig.update_layout(showlegend=True)
        
        # Display the Plotly chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)
        
    elif questions == '4. How many comments were made on each video, and what are their corresponding video names?':
        cursor.execute("""SELECT channel_name, video_id, title, comments FROM video_details ORDER BY comments DESC LIMIT 10;""")
        df = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        st.dataframe(df)

        # Visualization using Plotly
        fig = px.bar(df,
                     x='comments',
                     y='title',
                     orientation='h',
                     color='channel_name',
                     labels={'channel_name': 'Channel Name', 'title': 'Video Title', 'comments': 'Number of Comments'},
                     title='Top 10 Videos with the Most Comments',
                     )
        fig.update_layout(showlegend=True)
    
        # Display the Plotly chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)
          
    elif questions == '5. Which videos have the highest number of likes, and what are their corresponding channel names?':
        cursor.execute("""SELECT channel_name AS Channel_Name,title AS Title,likes AS likes FROM video_details ORDER BY likes DESC LIMIT 10;""")
        df = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        st.dataframe(df)
        st.write("### :white[Top 10 most liked videos :]")
        fig = px.bar(df,
                     x=cursor.column_names[2],
                     y=cursor.column_names[1],
                     orientation='h',
                     color=cursor.column_names[0]
                    )
        st.plotly_chart(fig,use_container_width=True)
        
    elif questions == '6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?':
        cursor.execute("""SELECT title AS Title, likes AS likes FROM video_details ORDER BY likes DESC;""")
        df = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        
        st.dataframe(df)

        st.bar_chart(df.set_index('Title')['likes'])

         
    elif questions == '7. What is the total number of views for each channel, and what are their corresponding channel names?':
        cursor.execute("""SELECT channel_name AS Channel_Name, channel_views AS views FROM channel_details ORDER BY channel_views DESC;""")
        
        df = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        st.dataframe(df)
        st.write("### :white[Channels vs Views :]")
        fig = px.bar(df,
                     x=cursor.column_names[0],
                     y=cursor.column_names[1],
                     orientation='v',
                     color=cursor.column_names[0]
                    )
        st.plotly_chart(fig,use_container_width=True)


        
    elif questions == '8. What are the names of all the channels that have published videos in the year 2022?':
        cursor.execute("""SELECT title AS Channel_Name,
                       MAX(Published_date) AS LatestVideoRelease  -- Use an aggregate function like MAX
                       FROM video_details
                       WHERE published_date LIKE '2022%'
                       GROUP BY title
                       ORDER BY title;;""")
        df = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        
        st.dataframe(df)
        
        fig = px.bar(df, x='Channel_Name', y='LatestVideoRelease',
                     labels={'Channel_Name': 'Channel Name', 'LatestVideoRelease': 'Latest Video Release'},
                     title='Channels with Latest Video Release in 2022')
    
        # Show the plot
        fig.update_layout(width=1200, height=1200) 
        st.plotly_chart(fig)
    
    
    elif questions == '9. What is the duration of top_10 videos in each channel, and what are their corresponding channel names?':
        cursor.execute("""SELECT v.title AS video_Name, MAX(v.duration) AS highest_duration, c.channel_name
                       FROM video_details v
                       JOIN channel_details c ON v.channel_id = c.channel_id
                       GROUP BY v.title, c.channel_name
                       ORDER BY highest_duration DESC
                       LIMIT 10;""")
        df = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)

        col1,col2=st.columns(2)
        with col1:
            st.dataframe(df)  
        with col2:
            fig = px.bar(df, x='highest_duration', y='video_Name', color='channel_name',
                         labels={'highest_duration': 'Highest Duration', 'video_Name': 'Video Name'},
                         title='Top 10 Videos with Highest Duration in Each Channel')
            st.plotly_chart(fig)     
      
        
    elif questions == '10. Which videos have the highest number of comments, and what are their corresponding channel names?':
        cursor.execute("""SELECT title AS Channel_Name,video_id AS Video_ID,comments AS Comments FROM video_details ORDER BY comments DESC LIMIT 10;""")
        df = pd.DataFrame(cursor.fetchall(),columns=cursor.column_names)
        st.dataframe(df)
        st.markdown('<h3 style="color:white;">Videos with most comments :</h3>', unsafe_allow_html=True)

        
        fig = px.bar(df,
                     x=cursor.column_names[1],
                     y=cursor.column_names[2],
                     orientation='v',
                     color=cursor.column_names[0]
                    )
        st.plotly_chart(fig,use_container_width=True)
