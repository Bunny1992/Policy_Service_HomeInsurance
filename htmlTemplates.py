# bot_template = '''
#     <div class="chat-message bot">
#         <div class="avatar">
#             <img src="https://www.chubb.com/content/dam/chubb-sites/chubb/us-en/home_page/CHUBB_Logo_Black_RBG.png" alt="Assistant Logo">
#         </div>
#         <div class="message" style="color: #000;">{{MSG}}</div>
#     </div>
# '''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://static.vecteezy.com/system/resources/previews/034/793/144/original/ai-generated-3d-person-cartoon-emoji-with-a-smile-raising-his-hand-on-transparent-background-image-png.png" alt="User Avatar">
    </div>
    <div class="message" style="color: #000;">{{MSG}}</div>
</div>
'''

# Inject custom CSS for the entire page and elements
page_style = """
    <style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600&display=swap');

    /* Set the background color for the entire page */
    body {
        background-color: #E6F7FF; /* Light blue background color */
        font-family: 'Poppins', sans-serif;
    }

    /* Chat message container */
    .chat-message {
        padding: 1.5rem; 
        border-radius: 0.5rem; 
        margin-bottom: 1rem; 
        display: flex;
        align-items: center; /* Aligns the image and message vertically */
    }
    .chat-message.user {
        background-color: #CCE7FF; /* Light blue for user messages */
    }
    .chat-message.bot {
        background-color: #B3D3FF; /* Slightly darker blue for bot messages */
    }
    .chat-message .avatar {
        width: 10%; /* Adjust this percentage as needed */
        margin-right: 1rem; /* Adds space between the image and the message */
    }
    .chat-message .avatar img {
        max-width: 75px; /* Adjust the size of the logo */
        max-height: 75px;
        border-radius: 15%; /* Optional: makes the image circular */
        object-fit: cover;
    }
    .chat-message .message {
        width: 90%;
        padding: 0 1.5rem;
        color: #000; /* Black text */
    }

    /* Title styling */
    .title-container {
        background-color: #B3D3FF;  /* Softer blue background */
        padding: 10px;  /* Reduced padding */
        border-radius: 8px;  /* Slightly smaller border radius */
        color: #333;  /* Darker text color */
        font-size: 20px;  /* Reduced font size */
        text-align: center;
        box-shadow: 0 3px 6px rgba(0, 0, 0, 0.1);  /* Slightly smaller shadow */
        margin-bottom: 15px;  /* Reduced margin */
    }
    </style>
    """

# Title section with custom style
title_html = """
    <div class="title-container">
        <strong>Post Purchase Policy Servicer - Home Insurance</strong>
    </div>
    """

# Inject custom CSS to style the sidebar
sidebar_style = """
    <style>
    /* Style the sidebar */
    [data-testid="stSidebar"] {
        background-color: #E6F7FF;  /* Light blue background */
        padding: 20px;
    }
    
    /* Style the sidebar subheader */
    [data-testid="stSidebar"] h2 {
        color: #0056b3;  /* Darker blue text color */
    }

    /* Style the file uploader and button */
    [data-testid="stFileUploader"] {
        border: 1px solid #CCE7FF;
        border-radius: 5px;
    }
    [data-testid="stButton"] button {
        background-color: #0056b3;
        color: white;
        border-radius: 5px;
    }
    </style>
    """

# Define the HTML and CSS for positioning and aligning the logos
logo_html = """
    <div style="display: flex; justify-content: space-between; align-items: center; width: 100%;">
        <div style="display: flex; align-items: center;">
            <img src="https://www.indiumsoftware.com/wp-content/uploads/2023/11/logo_fixed.png" width="150"> <!-- Replace with your logo URL or path -->
        </div>
    </div>
"""

font =  """
    <style>
    h1 {
        font-family: 'Courier New', monospace;
        color: darkblue;
    }
    .stText {
        font-family: 'Comic Sans MS', cursive;
        color: darkgreen;
    }
    </style>
    """

page_bg_img = f"""
    <style>
        [data-testid="stAppViewContainer"] > .main {{
        background-image: url("https://media.istockphoto.com/id/1210292829/vector/japanese-paper-pink.jpg?s=612x612&w=0&k=20&c=i6ip0nqCcus6xFpPz0iT1wRzADc0hgxw2jGYi6uZXOA=");
        background-size: cover;
        background-position: center center;
        background-repeat: no-repeat;
        background-attachment: local;
        }}
        [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
    }}
    </style>
"""

