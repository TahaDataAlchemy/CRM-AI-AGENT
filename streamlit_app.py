# import streamlit as st
# import requests
# import json
# from typing import Dict, Any
# from datetime import datetime
# import time

# # Page configuration
# st.set_page_config(
#     page_title="HubSpot AI Agent",
#     page_icon="🤖",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Custom CSS for better styling
# st.markdown("""
# <style>
#     .main-header {
#         font-size: 3rem;
#         font-weight: bold;
#         text-align: center;
#         color: #ff7a59;
#         margin-bottom: 1rem;
#         text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
#     }
#     .subtitle {
#         font-size: 1.2rem;
#         color: #666;
#         text-align: center;
#         margin-bottom: 2rem;
#     }
#     .hubspot-card {
#         background: linear-gradient(135deg, #ff7a59 0%, #ff6b6b 100%);
#         color: white;
#         padding: 3rem;
#         border-radius: 20px;
#         text-align: center;
#         margin: 2rem 0;
#         box-shadow: 0 10px 40px rgba(255, 122, 89, 0.3);
#         border: 3px solid rgba(255, 255, 255, 0.2);
#     }
#     .chat-container {
#         background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
#         border-radius: 20px;
#         padding: 2rem;
#         margin: 1rem 0;
#         max-height: 500px;
#         overflow-y: auto;
#         border: 2px solid #dee2e6;
#         box-shadow: inset 0 2px 10px rgba(0,0,0,0.1);
#     }
#     .user-message {
#         background: linear-gradient(135deg, #ff7a59 0%, #ff6b6b 100%);
#         color: white;
#         padding: 1rem 1.5rem;
#         border-radius: 20px 20px 5px 20px;
#         margin: 1rem 0;
#         text-align: right;
#         max-width: 75%;
#         margin-left: auto;
#         box-shadow: 0 4px 15px rgba(255, 122, 89, 0.3);
#     }
#     .ai-message {
#         background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
#         color: #333;
#         padding: 1rem 1.5rem;
#         border-radius: 20px 20px 20px 5px;
#         margin: 1rem 0;
#         text-align: left;
#         max-width: 75%;
#         border: 2px solid #e9ecef;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.1);
#     }
#     .message-timestamp {
#         font-size: 0.8rem;
#         opacity: 0.7;
#         margin-top: 0.5rem;
#     }
#     .stButton > button {
#         width: 100%;
#         height: 3.5rem;
#         font-size: 1.1rem;
#         font-weight: bold;
#         border-radius: 15px;
#         background: linear-gradient(135deg, #ff7a59 0%, #ff6b6b 100%);
#         border: none;
#         color: white;
#         transition: all 0.3s ease;
#         box-shadow: 0 4px 15px rgba(255, 122, 89, 0.3);
#     }
#     .stButton > button:hover {
#         transform: translateY(-2px);
#         box-shadow: 0 8px 25px rgba(255, 122, 89, 0.4);
#     }
#     .status-indicator {
#         display: flex;
#         align-items: center;
#         padding: 0.5rem 1rem;
#         border-radius: 20px;
#         margin: 1rem 0;
#         font-weight: bold;
#     }
#     .status-connected {
#         background-color: #d4edda;
#         color: #155724;
#         border: 2px solid #c3e6cb;
#     }
#     .status-disconnected {
#         background-color: #f8d7da;
#         color: #721c24;
#         border: 2px solid #f5c6cb;
#     }
#     .welcome-card {
#         background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
#         padding: 2rem;
#         border-radius: 15px;
#         margin: 1rem 0;
#         text-align: center;
#         border: 2px solid #90caf9;
#     }
#     .example-queries {
#         background: white;
#         padding: 1.5rem;
#         border-radius: 15px;
#         margin: 1rem 0;
#         border: 2px solid #e9ecef;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.1);
#     }
#     .chat-input-container {
#         background: white;
#         padding: 1.5rem;
#         border-radius: 15px;
#         margin: 1rem 0;
#         border: 2px solid #e9ecef;
#         box-shadow: 0 4px 15px rgba(0,0,0,0.1);
#     }
#     .sidebar-section {
#         background: #f8f9fa;
#         padding: 1rem;
#         border-radius: 10px;
#         margin: 1rem 0;
#         border: 1px solid #dee2e6;
#     }
# </style>
# """, unsafe_allow_html=True)

# def initialize_session_state():
#     """Initialize session state variables"""
#     if 'chat_history' not in st.session_state:
#         st.session_state.chat_history = []
#     if 'is_authorized' not in st.session_state:
#         st.session_state.is_authorized = False
#     if 'user_email' not in st.session_state:
#         st.session_state.user_email = ""

# def add_message_to_history(role: str, message: str, timestamp: str = None):
#     """Add a message to chat history"""
#     if timestamp is None:
#         timestamp = datetime.now().strftime("%H:%M:%S")
    
#     st.session_state.chat_history.append({
#         "role": role,
#         "message": message,
#         "timestamp": timestamp
#     })

# def display_chat_history():
#     """Display the chat history"""
#     if not st.session_state.chat_history:
#         return
    
#     st.markdown("### 💬 Conversation History")
    
#     with st.container():
#         for msg in st.session_state.chat_history:
#             if msg["role"] == "user":
#                 st.markdown(f"""
#                 <div class="user-message">
#                     <div><strong>You:</strong> {msg['message']}</div>
#                     <div class="message-timestamp">{msg['timestamp']}</div>
#                 </div>
#                 """, unsafe_allow_html=True)
#             else:
#                 st.markdown(f"""
#                 <div class="ai-message">
#                     <div><strong>🤖 AI Agent:</strong> {msg['message']}</div>
#                     <div class="message-timestamp">{msg['timestamp']}</div>
#                 </div>
#                 """, unsafe_allow_html=True)

# def handle_hubspot_authorization(api_base_url: str):
#     """Handle HubSpot authorization"""
#     try:
#         with st.spinner("🔄 Connecting to HubSpot..."):
#             response = requests.get(f"{api_base_url}/auth/authorize_user", timeout=10)
            
#         if response.status_code == 200:
#             # Try to parse JSON response, fallback to direct URL if not JSON
#             try:
#                 auth_data = response.json()
#                 auth_url = auth_data.get("authorization_url", f"{api_base_url}/auth/authorize_user")
#             except:
#                 # If response is not JSON, use the response URL directly
#                 auth_url = response.url
            
#             st.success("🔑 HubSpot authorization initiated!")
#             st.info("📱 Please complete the authorization in the popup window.")
            
#             # Create a more prominent authorization link
#             st.markdown(f"""
#             <div style="text-align: center; margin: 2rem 0;">
#                 <a href="{auth_url}" target="_blank" style="
#                     display: inline-block;
#                     background: linear-gradient(135deg, #ff7a59 0%, #ff6b6b 100%);
#                     color: white;
#                     padding: 15px 30px;
#                     text-decoration: none;
#                     border-radius: 25px;
#                     font-weight: bold;
#                     font-size: 1.1rem;
#                     box-shadow: 0 4px 15px rgba(255, 122, 89, 0.3);
#                     transition: all 0.3s ease;
#                 ">🔗 Complete HubSpot Authorization</a>
#             </div>
#             """, unsafe_allow_html=True)
            
#             # JavaScript to open popup
#             st.markdown(f"""
#             <script>
#                 window.open('{auth_url}', 'hubspot_auth', 'width=600,height=700,scrollbars=yes,resizable=yes');
#             </script>
#             """, unsafe_allow_html=True)
            
#             # Set authorization to True after initiating (this is the key fix)
#             st.session_state.is_authorized = True
#             add_message_to_history("ai", "🔗 HubSpot authorization window opened. Please complete the process and return here.")
            
#         else:
#             st.error("❌ Failed to initiate HubSpot authorization")
#             add_message_to_history("ai", "❌ Failed to connect to HubSpot. Please check your API connection and try again.")
            
#     except Exception as e:
#         st.error(f"❌ Connection error: {str(e)}")
#         add_message_to_history("ai", f"❌ Error connecting to HubSpot: {str(e)}")

# def process_ai_query(query: str, api_base_url: str):
#     """Process user query with AI Agent"""
#     if not query.strip():
#         return
    
#     # Add user message to history
#     add_message_to_history("user", query)
    
#     try:
#         with st.spinner("🤖 AI Agent is processing your request..."):
#             response = requests.post(
#                 f"{api_base_url}/agent/process",
#                 json={
#                     "query": query, 
#                     "user_email": st.session_state.user_email
#                 },
#                 timeout=30
#             )
        
#         if response.status_code == 200:
#             result = response.json()
#             if result.get("success"):
#                 # Format the AI response
#                 ai_response = "✅ Task completed successfully!"
                
#                 if result.get("message"):
#                     ai_response = result["message"]
#                 elif result.get("results"):
#                     responses = []
#                     for task_result in result["results"]:
#                         if task_result.get("message"):
#                             responses.append(task_result["message"])
#                         if task_result.get("data"):
#                             responses.append(f"📊 Data: {json.dumps(task_result['data'], indent=2)}")
#                     ai_response = "\n\n".join(responses) if responses else ai_response
                
#                 add_message_to_history("ai", ai_response)
#                 st.success("✅ Request processed successfully!")
                
#             else:
#                 error_msg = result.get("error", "Unknown error occurred")
#                 add_message_to_history("ai", f"❌ Error: {error_msg}")
#                 st.error(f"❌ AI Agent error: {error_msg}")
                
#         else:
#             error_msg = f"API Error: {response.status_code} - {response.text}"
#             add_message_to_history("ai", f"❌ {error_msg}")
#             st.error(f"❌ {error_msg}")
            
#     except requests.exceptions.Timeout:
#         error_msg = "Request timeout - please try again"
#         add_message_to_history("ai", f"❌ {error_msg}")
#         st.error(f"❌ {error_msg}")
        
#     except Exception as e:
#         error_msg = f"Connection error: {str(e)}"
#         add_message_to_history("ai", f"❌ {error_msg}")
#         st.error(f"❌ {error_msg}")

# def main():
#     # Initialize session state
#     initialize_session_state()
    
#     # Main header
#     st.markdown('<h1 class="main-header">🤖 HubSpot AI Agent</h1>', unsafe_allow_html=True)
#     st.markdown('<p class="subtitle">Your intelligent conversational assistant for HubSpot CRM automation</p>', unsafe_allow_html=True)
    
#     # Sidebar
#     with st.sidebar:
#         st.header("🔧 Configuration")
        
#         # API Configuration
#         st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
#         st.subheader("🌐 API Settings")
#         api_base_url = st.text_input(
#             "API Base URL",
#             value="http://localhost:8000",
#             help="Base URL for the HubSpot AI Agent API"
#         )
        
#         # User email
#         st.session_state.user_email = st.text_input(
#             "📧 Your Email",
#             value=st.session_state.user_email,
#             help="Email address for receiving notifications"
#         )
#         st.markdown('</div>', unsafe_allow_html=True)
        
#         # Connection test
#         st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
#         st.subheader("🔌 Connection Test")
#         if st.button("🔗 Test API Connection"):
#             try:
#                 with st.spinner("Testing connection..."):
#                     response = requests.get(f"{api_base_url}/", timeout=5)
#                 if response.status_code == 200:
#                     st.success("✅ API Connected!")
#                 else:
#                     st.error("❌ Connection failed")
#             except Exception as e:
#                 st.error(f"❌ Connection error: {str(e)}")
#         st.markdown('</div>', unsafe_allow_html=True)
        
#         # Authorization status
#         st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
#         st.subheader("🔐 HubSpot Status")
        
#         if st.session_state.is_authorized:
#             st.markdown('<div class="status-indicator status-connected">✅ Connected to HubSpot</div>', unsafe_allow_html=True)
#         else:
#             st.markdown('<div class="status-indicator status-disconnected">❌ Not connected to HubSpot</div>', unsafe_allow_html=True)
        
#         st.markdown('</div>', unsafe_allow_html=True)
        
#         # Chat controls
#         st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
#         st.subheader("💬 Chat Controls")
        
#         if st.button("🗑️ Clear Chat History"):
#             st.session_state.chat_history = []
#             st.success("Chat history cleared!")
#             st.rerun()
        
#         if st.button("🔄 Refresh Status"):
#             st.rerun()
        
#         st.markdown('</div>', unsafe_allow_html=True)
    
#     # Main content area
#     if not st.session_state.is_authorized:
#         # Authorization required screen
#         st.markdown('<div class="hubspot-card">', unsafe_allow_html=True)
#         st.markdown("### 🔐 Connect to HubSpot")
#         st.markdown("**Unlock AI-powered HubSpot automation:**")
#         st.markdown("✨ **Smart Contact Management** - Create, update, and organize contacts")
#         st.markdown("💼 **Intelligent Deal Tracking** - Monitor and manage your sales pipeline")
#         st.markdown("📧 **Automated Email Notifications** - Stay informed about important updates")
#         st.markdown("🧠 **Natural Language Processing** - Communicate with your CRM naturally")
        
#         if st.button("🚀 Connect to HubSpot", key="main_auth_btn"):
#             handle_hubspot_authorization(api_base_url)
        
#         st.markdown('</div>', unsafe_allow_html=True)
        
#         # Instructions
#         st.markdown('<div class="welcome-card">', unsafe_allow_html=True)
#         st.markdown("### 📋 Getting Started")
#         st.markdown("1. **Click 'Connect to HubSpot'** to authorize the application")
#         st.markdown("2. **Complete the authorization** in the popup window")
#         st.markdown("3. **Return here** to start your AI-powered conversation")
#         st.markdown("4. **Ask questions naturally** - the AI understands your intent!")
#         st.markdown('</div>', unsafe_allow_html=True)
        
#     else:
#         # Main conversational interface
#         st.markdown("### 💬 Chat with your HubSpot AI Agent")
        
#         # Chat history display
#         if st.session_state.chat_history:
#             st.markdown('<div class="chat-container">', unsafe_allow_html=True)
#             display_chat_history()
#             st.markdown('</div>', unsafe_allow_html=True)
#         else:
#             # Welcome message for first-time users
#             st.markdown('<div class="welcome-card">', unsafe_allow_html=True)
#             st.markdown("### 👋 Welcome to HubSpot AI Agent!")
#             st.markdown("I'm here to help you manage your HubSpot CRM. You can talk to me naturally!")
#             st.markdown('</div>', unsafe_allow_html=True)
            
#             # Example queries
#             st.markdown('<div class="example-queries">', unsafe_allow_html=True)
#             st.markdown("### 💡 Try these examples:")
#             st.markdown("🔹 **'Create a new contact for John Doe with email john@example.com'**")
#             st.markdown("🔹 **'Show me all my contacts'**")
#             st.markdown("🔹 **'Update John Doe's phone number to 123-456-7890'**")
#             st.markdown("🔹 **'Create a deal for Acme Corp worth $5,000'**")
#             st.markdown("🔹 **'Delete the contact named John Doe'**")
#             st.markdown("🔹 **'Send me an email summary of today's activities'**")
#             st.markdown('</div>', unsafe_allow_html=True)
        
#         # Chat input area - THIS IS THE KEY FIX
#         st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
#         st.markdown("### 💭 What would you like to do?")
        
#         # Text input for user query
#         user_query = st.text_area(
#             "",
#             placeholder="Type your message here... (e.g., 'Create a new contact for Sarah Johnson with email sarah@company.com')",
#             height=100,
#             key="user_input"
#         )
        
#         # Send button and reconnect option
#         col1, col2, col3 = st.columns([2, 1, 1])
        
#         with col1:
#             if st.button("🚀 Send Message", type="primary"):
#                 if user_query.strip():
#                     process_ai_query(user_query, api_base_url)
#                     st.rerun()
#                 else:
#                     st.warning("Please enter a message first!")
        
#         with col2:
#             if st.button("🔄 Reconnect", help="Reconnect to HubSpot"):
#                 st.session_state.is_authorized = False
#                 st.rerun()
        
#         with col3:
#             if st.button("📋 Examples", help="Show example queries"):
#                 st.info("Check the examples above! 👆")
        
#         st.markdown('</div>', unsafe_allow_html=True)

# if __name__ == "__main__":
#     main()

import streamlit as st
import requests
import json
from typing import Dict, Any
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="HubSpot AI Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #ff7a59;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .subtitle {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .hubspot-card {
        background: linear-gradient(135deg, #ff7a59 0%, #ff6b6b 100%);
        color: white;
        padding: 3rem;
        border-radius: 20px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 10px 40px rgba(255, 122, 89, 0.3);
        border: 3px solid rgba(255, 255, 255, 0.2);
    }
    .chat-container {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        max-height: 500px;
        overflow-y: auto;
        border: 2px solid #dee2e6;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.1);
    }
    .user-message {
        background: linear-gradient(135deg, #ff7a59 0%, #ff6b6b 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 1rem 0;
        text-align: right;
        max-width: 75%;
        margin-left: auto;
        box-shadow: 0 4px 15px rgba(255, 122, 89, 0.3);
    }
    .ai-message {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        color: #333;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 1rem 0;
        text-align: left;
        max-width: 75%;
        border: 2px solid #e9ecef;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .data-table {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
    }
    .data-item {
        background: #e9ecef;
        border-radius: 8px;
        padding: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #ff7a59;
    }
    .message-timestamp {
        font-size: 0.8rem;
        opacity: 0.7;
        margin-top: 0.5rem;
    }
    .stButton > button {
        width: 100%;
        height: 3.5rem;
        font-size: 1.1rem;
        font-weight: bold;
        border-radius: 15px;
        background: linear-gradient(135deg, #ff7a59 0%, #ff6b6b 100%);
        border: none;
        color: white;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 122, 89, 0.3);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(255, 122, 89, 0.4);
    }
    .status-indicator {
        display: flex;
        align-items: center;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 1rem 0;
        font-weight: bold;
    }
    .status-connected {
        background-color: #d4edda;
        color: #155724;
        border: 2px solid #c3e6cb;
    }
    .status-disconnected {
        background-color: #f8d7da;
        color: #721c24;
        border: 2px solid #f5c6cb;
    }
    .welcome-card {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        text-align: center;
        border: 2px solid #90caf9;
    }
    .example-queries {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 2px solid #e9ecef;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .chat-input-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 2px solid #e9ecef;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .sidebar-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #dee2e6;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'is_authorized' not in st.session_state:
        st.session_state.is_authorized = False
    if 'user_email' not in st.session_state:
        st.session_state.user_email = ""

def format_data_for_display(data):
    """Format data for better display in chat messages"""
    if not data:
        return ""
    
    try:
        # If data is a string, try to parse it as JSON
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except:
                return f"📄 {data}"
        
        # Handle different data types
        if isinstance(data, dict):
            return format_dict_data(data)
        elif isinstance(data, list):
            return format_list_data(data)
        else:
            return f"📄 {str(data)}"
    except Exception as e:
        return f"📄 {str(data)}"

def format_dict_data(data_dict):
    """Format dictionary data for display"""
    if not data_dict:
        return "📄 No data available"
    
    formatted_items = []
    for key, value in data_dict.items():
        # Format the key nicely
        formatted_key = key.replace('_', ' ').title()
        
        # Format the value based on its type
        if isinstance(value, dict):
            formatted_value = format_dict_data(value)
        elif isinstance(value, list):
            formatted_value = format_list_data(value)
        elif value is None:
            formatted_value = "Not specified"
        else:
            formatted_value = str(value)
        
        formatted_items.append(f"<div class='data-item'><strong>{formatted_key}:</strong> {formatted_value}</div>")
    
    return f"<div class='data-table'>{''.join(formatted_items)}</div>"

def format_list_data(data_list):
    """Format list data for display in a proper table if possible"""
    if not data_list:
        return "📄 No items found"
    
    # Check if the list is a list of dictionaries with similar keys
    if all(isinstance(item, dict) for item in data_list):
        # Extract all unique keys across all items
        keys = set()
        for item in data_list:
            keys.update(item.keys())
        keys = list(keys)

        # Start table HTML
        table_html = "<div class='data-table'><table style='width:100%; border-collapse: collapse;'>"
        # Table header
        table_html += "<thead><tr>" + "".join(
            f"<th style='border:1px solid #ccc; padding:8px; background:#ff7a59; color:white'>{key}</th>" for key in keys
        ) + "</tr></thead><tbody>"

        # Table rows
        for item in data_list:
            row = "<tr>" + "".join(
                f"<td style='border:1px solid #ccc; padding:8px'>{item.get(key, '')}</td>" for key in keys
            ) + "</tr>"
            table_html += row

        table_html += "</tbody></table></div>"
        return table_html
    
    # Fallback if not list of dicts
    formatted_items = []
    for i, item in enumerate(data_list, 1):
        formatted_items.append(f"<div class='data-item'><strong>Item {i}:</strong> {str(item)}</div>")
    
    return f"<div class='data-table'>{''.join(formatted_items)}</div>"

def add_message_to_history(role: str, message: str, data: Any = None, timestamp: str = None):
    """Add a message to chat history with optional data"""
    if timestamp is None:
        timestamp = datetime.now().strftime("%H:%M:%S")
    
    st.session_state.chat_history.append({
        "role": role,
        "message": message,
        "data": data,
        "timestamp": timestamp
    })

def display_chat_history():
    """Display the chat history"""
    if not st.session_state.chat_history:
        return
    
    st.markdown("### 💬 Conversation History")
    
    with st.container():
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="user-message">
                    <div><strong>You:</strong> {msg['message']}</div>
                    <div class="message-timestamp">{msg['timestamp']}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Format AI message with data if available
                message_content = msg['message']
                if msg.get('data'):
                    formatted_data = format_data_for_display(msg['data'])
                    message_content = f"{message_content}<br><br>{formatted_data}"
                
                st.markdown(f"""
                <div class="ai-message">
                    <div><strong>🤖 AI Agent:</strong> {message_content}</div>
                    <div class="message-timestamp">{msg['timestamp']}</div>
                </div>
                """, unsafe_allow_html=True)

def handle_hubspot_authorization(api_base_url: str):
    """Handle HubSpot authorization"""
    try:
        with st.spinner("🔄 Connecting to HubSpot..."):
            response = requests.get(f"{api_base_url}/auth/authorize_user", timeout=10)
            
        if response.status_code == 200:
            # Try to parse JSON response, fallback to direct URL if not JSON
            try:
                auth_data = response.json()
                auth_url = auth_data.get("authorization_url", f"{api_base_url}/auth/authorize_user")
            except:
                # If response is not JSON, use the response URL directly
                auth_url = response.url
            
            st.success("🔑 HubSpot authorization initiated!")
            st.info("📱 Please complete the authorization in the popup window.")
            
            # Create a more prominent authorization link
            st.markdown(f"""
            <div style="text-align: center; margin: 2rem 0;">
                <a href="{auth_url}" target="_blank" style="
                    display: inline-block;
                    background: linear-gradient(135deg, #ff7a59 0%, #ff6b6b 100%);
                    color: white;
                    padding: 15px 30px;
                    text-decoration: none;
                    border-radius: 25px;
                    font-weight: bold;
                    font-size: 1.1rem;
                    box-shadow: 0 4px 15px rgba(255, 122, 89, 0.3);
                    transition: all 0.3s ease;
                ">🔗 Complete HubSpot Authorization</a>
            </div>
            """, unsafe_allow_html=True)
            
            # JavaScript to open popup
            st.markdown(f"""
            <script>
                window.open('{auth_url}', 'hubspot_auth', 'width=600,height=700,scrollbars=yes,resizable=yes');
            </script>
            """, unsafe_allow_html=True)
            
            # Set authorization to True after initiating (this is the key fix)
            st.session_state.is_authorized = True
            add_message_to_history("ai", "🔗 HubSpot authorization window opened. Please complete the process and return here.")
            
        else:
            st.error("❌ Failed to initiate HubSpot authorization")
            add_message_to_history("ai", "❌ Failed to connect to HubSpot. Please check your API connection and try again.")
            
    except Exception as e:
        st.error(f"❌ Connection error: {str(e)}")
        add_message_to_history("ai", f"❌ Error connecting to HubSpot: {str(e)}")

def process_ai_query(query: str, api_base_url: str):
    """Process user query with AI Agent"""
    if not query.strip():
        return
    
    # Add user message to history
    add_message_to_history("user", query)
    
    try:
        with st.spinner("🤖 AI Agent is processing your request..."):
            response = requests.post(
                f"{api_base_url}/agent/process",
                json={
                    "query": query, 
                    "user_email": st.session_state.user_email
                },
                timeout=30
            )
        
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                # Format the AI response
                ai_response = "✅ Task completed successfully!"
                response_data = None
                
                if result.get("message"):
                    ai_response = result["message"]
                
                # Handle the results data
                if result.get("results"):
                    all_data = []
                    responses = []
                    
                    for task_result in result["results"]:
                        if task_result.get("message"):
                            responses.append(task_result["message"])
                        if task_result.get("data"):
                            all_data.append(task_result["data"])
                    
                    # Combine responses if multiple
                    if responses:
                        ai_response = " | ".join(responses)
                    
                    # Combine all data for display
                    if all_data:
                        if len(all_data) == 1:
                            response_data = all_data[0]
                        else:
                            response_data = all_data
                
                # Handle single data response
                elif result.get("data"):
                    response_data = result["data"]
                
                add_message_to_history("ai", ai_response, response_data)
                st.success("✅ Request processed successfully!")
                
            else:
                error_msg = result.get("error", "Unknown error occurred")
                add_message_to_history("ai", f"❌ Error: {error_msg}")
                st.error(f"❌ AI Agent error: {error_msg}")
                
        else:
            error_msg = f"API Error: {response.status_code} - {response.text}"
            add_message_to_history("ai", f"❌ {error_msg}")
            st.error(f"❌ {error_msg}")
            
    except requests.exceptions.Timeout:
        error_msg = "Request timeout - please try again"
        add_message_to_history("ai", f"❌ {error_msg}")
        st.error(f"❌ {error_msg}")
        
    except Exception as e:
        error_msg = f"Connection error: {str(e)}"
        add_message_to_history("ai", f"❌ {error_msg}")
        st.error(f"❌ {error_msg}")

def main():
    # Initialize session state
    initialize_session_state()
    
    # Main header
    st.markdown('<h1 class="main-header">🤖 HubSpot AI Agent</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Your intelligent conversational assistant for HubSpot CRM automation</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # API Configuration
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.subheader("🌐 API Settings")
        api_base_url = st.text_input(
            "API Base URL",
            value="http://localhost:8000",
            help="Base URL for the HubSpot AI Agent API"
        )
        
        # User email
        st.session_state.user_email = st.text_input(
            "📧 Your Email",
            value=st.session_state.user_email,
            help="Email address for receiving notifications"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Connection test
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.subheader("🔌 Connection Test")
        if st.button("🔗 Test API Connection"):
            try:
                with st.spinner("Testing connection..."):
                    response = requests.get(f"{api_base_url}/", timeout=5)
                if response.status_code == 200:
                    st.success("✅ API Connected!")
                else:
                    st.error("❌ Connection failed")
            except Exception as e:
                st.error(f"❌ Connection error: {str(e)}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Authorization status
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.subheader("🔐 HubSpot Status")
        
        if st.session_state.is_authorized:
            st.markdown('<div class="status-indicator status-connected">✅ Connected to HubSpot</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-indicator status-disconnected">❌ Not connected to HubSpot</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat controls
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.subheader("💬 Chat Controls")
        
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.success("Chat history cleared!")
            st.rerun()
        
        if st.button("🔄 Refresh Status"):
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content area
    if not st.session_state.is_authorized:
        # Authorization required screen
        st.markdown('<div class="hubspot-card">', unsafe_allow_html=True)
        st.markdown("### 🔐 Connect to HubSpot")
        st.markdown("**Unlock AI-powered HubSpot automation:**")
        st.markdown("✨ **Smart Contact Management** - Create, update, and organize contacts")
        st.markdown("💼 **Intelligent Deal Tracking** - Monitor and manage your sales pipeline")
        st.markdown("📧 **Automated Email Notifications** - Stay informed about important updates")
        st.markdown("🧠 **Natural Language Processing** - Communicate with your CRM naturally")
        
        if st.button("🚀 Connect to HubSpot", key="main_auth_btn"):
            handle_hubspot_authorization(api_base_url)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Instructions
        st.markdown('<div class="welcome-card">', unsafe_allow_html=True)
        st.markdown("### 📋 Getting Started")
        st.markdown("1. **Click 'Connect to HubSpot'** to authorize the application")
        st.markdown("2. **Complete the authorization** in the popup window")
        st.markdown("3. **Return here** to start your AI-powered conversation")
        st.markdown("4. **Ask questions naturally** - the AI understands your intent!")
        st.markdown('</div>', unsafe_allow_html=True)
        
    else:
        # Main conversational interface
        st.markdown("### 💬 Chat with your HubSpot AI Agent")
        
        # Chat history display
        if st.session_state.chat_history:
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            display_chat_history()
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            # Welcome message for first-time users
            st.markdown('<div class="welcome-card">', unsafe_allow_html=True)
            st.markdown("### 👋 Welcome to HubSpot AI Agent!")
            st.markdown("I'm here to help you manage your HubSpot CRM. You can talk to me naturally!")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Example queries
            st.markdown('<div class="example-queries">', unsafe_allow_html=True)
            st.markdown("### 💡 Try these examples:")
            st.markdown("🔹 **'Create a new contact for John Doe with email john@example.com'**")
            st.markdown("🔹 **'Show me all my contacts'**")
            st.markdown("🔹 **'Update John Doe's phone number to 123-456-7890'**")
            st.markdown("🔹 **'Create a deal for Acme Corp worth $5,000'**")
            st.markdown("🔹 **'Delete the contact named John Doe'**")
            st.markdown("🔹 **'Send me an email summary of today's activities'**")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat input area
        st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
        st.markdown("### 💭 What would you like to do?")
        
        # Text input for user query
        user_query = st.text_area(
            "",
            placeholder="Type your message here... (e.g., 'Create a new contact for Sarah Johnson with email sarah@company.com')",
            height=100,
            key="user_input"
        )
        
        # Send button and reconnect option
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            if st.button("🚀 Send Message", type="primary"):
                if user_query.strip():
                    process_ai_query(user_query, api_base_url)
                    st.rerun()
                else:
                    st.warning("Please enter a message first!")
        
        with col2:
            if st.button("🔄 Reconnect", help="Reconnect to HubSpot"):
                st.session_state.is_authorized = False
                st.rerun()
        
        with col3:
            if st.button("📋 Examples", help="Show example queries"):
                st.info("Check the examples above! 👆")
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()