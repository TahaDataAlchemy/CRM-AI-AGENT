# 🤖 HubSpot AI Agent - Autonomous CRM Workflow Automation

A sophisticated AI-powered autonomous agent system for HubSpot CRM workflow automation with a multi-agent architecture. This system enables natural language interaction with HubSpot CRM through intelligent agents that can manage contacts, deals, and send automated notifications.


**Note: Test Backend seperately as the UI is not upto mark**


## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Code Flow](#code-flow)
- [API Endpoints](#api-endpoints)
- [Features](#features)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

The HubSpot AI Agent is a comprehensive CRM automation system that combines:

- **Multi-Agent Architecture**: Global Orchestrator, HubSpot Agent, Email Agent
- **Natural Language Processing**: Conversational interface for CRM operations
- **Automated Workflows**: Contact management, deal tracking, email notifications
- **Streamlit UI**: User-friendly web interface for interaction
- **GROQ LLM Integration**: Advanced language model for intelligent responses

## 🏗️ Architecture

### Multi-Agent System
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Orchestrator   │    │  HubSpot Agent  │    │  Email Agent    │
│     Agent       │◄──►│                 │◄──►│                 │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Query         │    │   HubSpot       │    │   SMTP          │
│ Decomposer      │    │   API           │    │   Email         │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Core Components
1. **Orchestrator Agent**: Coordinates all operations and manages workflow
2. **HubSpot Agent**: Handles CRM operations (contacts, deals, companies)
3. **Email Agent**: Manages email notifications and templates
4. **Query Decomposer**: Breaks down complex user queries into actionable tasks
5. **GROQ LLM**: Provides intelligent response processing

## 📁 Project Structure

```
Code/
├── app/                          # Main application directory
│   ├── __init__.py
│   ├── AuthFlowHubspot/          # HubSpot authentication
│   │   ├── __init__.py
│   │   ├── authroutes.py         # OAuth routes and handlers
│   │   └── token_manager.py      # Token storage and management
│   │
│   ├── controllers/              # API endpoints and routing
│   │   ├── __init__.py
│   │   ├── agent/
│   │   │   └── agent_endpoint.py # Main agent processing endpoint
│   │   ├── contacts/
│   │   │   ├── __init__.py
│   │   │   └── contact_endpoints.py # Contact CRUD operations
│   │   └── Deals/
│   │       ├── __init__.py
│   │       └── deals_endpoint.py # Deal management endpoints
│   │
│   ├── domain/                   # Business logic and domain models
│   │   ├── __init__.py
│   │   ├── AiAgent/              # AI agent implementations
│   │   │   ├── __init__.py
│   │   │   ├── ContactAgent/     # Contact-specific AI agent
│   │   │   │   ├── __init__.py
│   │   │   │   ├── data/
│   │   │   │   └── usecase/
│   │   │   │       ├── __init__.py
│   │   │   │       └── contact_agent.py # Contact agent logic
│   │   │   ├── DealAgent/        # Deal management agent
│   │   │   │   ├── __init__.py
│   │   │   │   ├── data/
│   │   │   │   └── usecase/
│   │   │   │       └── __init__.py
│   │   │   ├── EmailAgent/       # Email automation agent
│   │   │   │   ├── __init__.py
│   │   │   │   ├── data/
│   │   │   │   └── usecase/
│   │   │   │       ├── __init__.py
│   │   │   │       └── email_agent.py # Email agent implementation
│   │   │   └── OrchestratorAgent/ # Main orchestrator agent
│   │   │       ├── __init__.py
│   │   │       ├── data/
│   │   │       │   ├── __init__.py
│   │   │       │   └── DataModel.py # Data models for orchestrator
│   │   │       ├── prompts/      # AI prompts for different operations
│   │   │       │   ├── __init__.py
│   │   │       │   ├── contact_search_prompt.py
│   │   │       │   ├── orchestrator_prompt.py
│   │   │       │   ├── payload_createrPrompt.py
│   │   │       │   └── Query_Decomposer_Prompt.py
│   │   │       └── usecase/
│   │   │           ├── __init__.py
│   │   │           ├── OrchestrationAgent.py # Main orchestrator logic
│   │   │           └── query_decomposer.py # Query processing
│   │   │
│   │   ├── CRM/                  # CRM-specific business logic
│   │   │   ├── __init__.py
│   │   │   ├── contacts/         # Contact management
│   │   │   │   ├── __init__.py
│   │   │   │   ├── data/
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── ContactDataModel.py # Contact data models
│   │   │   │   └── usecase/
│   │   │   │       ├── __init__.py
│   │   │   │       └── contacts_Operations.py # Contact operations
│   │   │   └── Deals/            # Deal management
│   │   │       ├── __init__.py
│   │   │       ├── data/
│   │   │       │   ├── __init__.py
│   │   │       │   └── DealProperties.py # Deal property models
│   │   │       └── usecase/
│   │   │           ├── __init__.py
│   │   │           └── deals_operations.py # Deal operations
│   │   │
│   ├── GROQ_CLIENT/              # GROQ LLM integration
│   │   ├── __init__.py
│   │   └── groq_api.py           # GROQ API client implementation
│   │
│   ├── infra/                    # Infrastructure and configuration
│   │   ├── __init__.py
│   │   ├── config.py             # Application configuration
│   │   └── constant.py           # Constants and enums
│   │
│   ├── repository/               # Data access layer
│   │   └── __init__.py
│   │
│   ├── server.py                 # FastAPI server entry point
│   │
│   └── shared/                   # Shared utilities and resources
│       ├── __init__.py
│       ├── io_files/             # File I/O operations
│       │   ├── __init__.py
│       │   └── token.json        # OAuth token storage
│       ├── logs/                 # Logging system
│       │   ├── __init__.py
│       │   ├── app_errors/
│       │   │   ├── __init__.py
│       │   │   └── error_logs.txt
│       │   └── app_logs/
│       │       ├── __init__.py
│       │       └── app_logs.txt
│       └── utils/                # Utility functions
│           ├── __init__.py
│           ├── common_functions.py # Common utility functions
│           └── error.py          # Error handling utilities
│
├── streamlit_app.py              # Streamlit web interface
└── README.md                     # This file
```

## 🚀 Installation

### Prerequisites
- Python 3.12+
- Poetry (for dependency management)
- HubSpot Developer Account
- GROQ API Key
- SMTP credentials (for email notifications)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Code
   ```

2. **Install dependencies with Poetry**
   ```bash
   poetry install
   poetry shell
   ```

3. **Configure environment variables**
   Create a `.env` file in the root directory:
   ```env
   # HubSpot Configuration
   HUBSPOT_CLIENT_ID=your_hubspot_client_id
   HUBSPOT_CLIENT_SECRET=your_hubspot_client_secret
   HUBSPOT_REDIRECT_URI=http://localhost:8000/auth/callback
   
   # GROQ Configuration
   GROQ_API_KEY=your_groq_api_key
   
   # Email Configuration
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your_email@gmail.com
   SMTP_PASSWORD=your_app_password
   ```

4. **Configure HubSpot OAuth**
   - Create a HubSpot app in the developer portal
   - Set redirect URI to `http://localhost:8000/auth/callback`
   - Add required scopes: `contacts`, `deals`, `companies`

## ⚙️ Configuration

### HubSpot Setup
1. **Developer Portal**: Create app at https://developers.hubspot.com/
2. **OAuth Scopes**: Configure required permissions
3. **Redirect URI**: Set to `http://localhost:8000/auth/callback`

### Email Configuration
1. **Gmail Setup**: Enable 2FA and generate app password
2. **SMTP Settings**: Configure SMTP server details
3. **Templates**: Email templates are stored in the Email Agent

### GROQ LLM
1. **API Key**: Get from https://console.groq.com/
2. **Model**: Uses `llama3-8b-8192` for processing
3. **Rate Limits**: Configure appropriate limits

## 💻 Usage

### Starting the Backend API
```bash
# Start the FastAPI server
python app/server.py
```
Server runs on `http://localhost:8000`

### Starting the Streamlit Interface
```bash
# Start the Streamlit app
streamlit run streamlit_app.py
```
Interface runs on `http://localhost:8501`

### Using the Application

1. **Access Streamlit Interface**
   - Open `http://localhost:8501`
   - Configure API settings in sidebar

2. **Connect to HubSpot**
   - Click "Connect to HubSpot" button
   - Complete OAuth authorization
   - Return to application

3. **Start Chatting**
   - Type natural language queries
   - Examples:
     - "Create a new contact for John Doe with email john@example.com"
     - "Show me all contacts"
     - "Create a deal for Acme Corp worth $5000"

## 🔄 Code Flow

### 1. User Interaction Flow
```
User Input (Streamlit) 
    ↓
Streamlit Interface (streamlit_app.py)
    ↓
API Request to Backend
    ↓
FastAPI Server (server.py)
    ↓
Agent Endpoint (agent_endpoint.py)
    ↓
Orchestrator Agent (OrchestrationAgent.py)
    ↓
Query Decomposer (query_decomposer.py)
    ↓
Specific Agent (Contact/Deal/Email Agent)
    ↓
HubSpot API / Email Service
    ↓
Response Processing
    ↓
GROQ LLM Enhancement
    ↓
User Response
```

### 2. Authentication Flow
```
User Clicks "Connect to HubSpot"
    ↓
Auth Endpoint (authroutes.py)
    ↓
HubSpot OAuth Redirect
    ↓
User Authorization
    ↓
Callback Handler (authroutes.py)
    ↓
Token Storage (token_manager.py)
    ↓
Authorization Complete
```

### 3. Agent Processing Flow
```
User Query: "Create contact John Doe"
    ↓
Query Decomposer
    ↓
Identifies: CREATE_CONTACT operation
    ↓
Orchestrator Agent
    ↓
Contact Agent (contact_agent.py)
    ↓
HubSpot API Call
    ↓
Response Processing
    ↓
Email Notification (email_agent.py)
    ↓
GROQ LLM Enhancement
    ↓
User-Friendly Response
```

### 4. Email Notification Flow
```
Agent Operation Complete
    ↓
Email Agent Trigger
    ↓
Template Selection
    ↓
SMTP Connection
    ↓
Email Composition
    ↓
Email Delivery
    ↓
Delivery Confirmation
```

## 🔌 API Endpoints

### Authentication
- `GET /auth/authorize_user` - Initiate HubSpot OAuth
- `GET /auth/callback` - OAuth callback handler
- `GET /auth/status` - Check authorization status

### Agent Operations
- `POST /agent/process` - Main agent processing endpoint
- `GET /agent/status` - Agent status check

### Contact Management
- `POST /contacts/create` - Create new contact
- `GET /contacts/list` - List all contacts
- `PUT /contacts/update` - Update contact
- `DELETE /contacts/delete` - Delete contact

### Deal Management
- `POST /deals/create` - Create new deal
- `GET /deals/list` - List all deals
- `PUT /deals/update` - Update deal
- `DELETE /deals/delete` - Delete deal

### Email Operations
- `POST /email/send` - Send email notification
- `GET /email/templates` - List email templates
- `POST /email/test` - Test email connection

## ✨ Features

### 🤖 AI-Powered Operations
- **Natural Language Processing**: Understands conversational queries
- **Query Decomposition**: Breaks complex requests into simple tasks
- **Intelligent Responses**: GROQ LLM enhances API responses
- **Context Awareness**: Maintains conversation context

### 🔄 Dynamic Query Processing
- **Multi-Task Execution**: Handle multiple operations in a single query
- **Batch Operations**: Process multiple contacts/deals simultaneously
- **Complex Workflows**: Execute sequential and parallel tasks
- **Smart Parsing**: Automatically identify and categorize multiple intents

#### Multi-Task Examples:
```
"Create contacts for John Doe (john@example.com) and Sarah Smith (sarah@company.com), 
then create a deal for John worth $5000 and update Sarah's phone to 123-456-7890"
```
**Gets decomposed into:**
1. Create contact: John Doe
2. Create contact: Sarah Smith  
3. Create deal: John Doe ($5000)
4. Update contact: Sarah Smith (phone)

### 🛡️ Comprehensive Error Handling
- **Graceful Degradation**: System continues operating even if some tasks fail
- **Detailed Error Reporting**: Specific error messages for each operation
- **Retry Mechanisms**: Automatic retry for transient failures
- **Partial Success Handling**: Reports which operations succeeded/failed
- **Validation Errors**: Pre-operation data validation
- **API Rate Limiting**: Automatic backoff and retry strategies

#### Error Handling Features:
- **Task-Level Error Isolation**: One failed task doesn't affect others
- **Error Recovery**: Automatic cleanup on partial failures
- **User-Friendly Messages**: Technical errors translated to user language
- **Error Logging**: Comprehensive error tracking and debugging
- **Fallback Mechanisms**: Alternative approaches when primary methods fail

### 📊 CRM Management
- **Contact Operations**: Create, read, update, delete contacts
- **Deal Management**: Full deal lifecycle management
- **Company Operations**: Company creation and management
- **Data Validation**: Ensures data integrity

### 📧 Email Automation
- **Template System**: Predefined email templates
- **SMTP Integration**: Supports multiple email providers
- **Notification System**: Automated status notifications
- **Delivery Tracking**: Email delivery confirmation

### 🔐 Security & Authentication
- **OAuth 2.0**: Secure HubSpot authentication
- **Token Management**: Secure token storage and refresh
- **Error Handling**: Comprehensive error management
- **Logging**: Detailed operation logging

### 🎨 User Interface
- **Streamlit Web App**: Modern, responsive interface
- **Real-time Chat**: Conversational interaction
- **Status Indicators**: Visual feedback for operations
- **Responsive Design**: Works on desktop and mobile

## 🔄 Advanced Code Flows

### Multi-Task Processing Flow
```
Complex User Query: "Create 3 contacts and 2 deals"
    ↓
Query Decomposer Analysis
    ↓
Task Extraction & Validation
    ↓
Parallel Task Execution
    ├── Contact Creation Task 1
    ├── Contact Creation Task 2  
    ├── Contact Creation Task 3
    ├── Deal Creation Task 1
    └── Deal Creation Task 2
    ↓
Individual Task Results Collection
    ↓
Success/Failure Aggregation
    ↓
Comprehensive Response Generation
    ↓
User-Friendly Summary Report
```

### Error Handling Flow
```
Task Execution
    ↓
Pre-Validation Check
    ↓
Primary Operation Attempt
    ↓
Error Detection
    ├── Validation Error → User-Friendly Message
    ├── API Error → Retry with Backoff
    ├── Network Error → Alternative Method
    └── System Error → Graceful Degradation
    ↓
Error Logging & Analysis
    ↓
Recovery Action
    ├── Rollback Changes
    ├── Partial Success Report
    └── Alternative Solution
    ↓
User Notification
```

### Dynamic Query Examples

#### Contact Batch Operations
```python
# Single Query - Multiple Operations
"Create contacts for Alice (alice@company.com), Bob (bob@corp.com), 
and Charlie (charlie@startup.com), then update Alice's phone to 555-1234"

# Gets processed as:
1. Create Contact: Alice Johnson (alice@company.com)
2. Create Contact: Bob Smith (bob@corp.com)  
3. Create Contact: Charlie Brown (charlie@startup.com)
4. Update Contact: Alice Johnson (phone: 555-1234)
```

#### Mixed Operations
```python
# Complex Workflow
"Create a contact for David (david@tech.com), create a deal for him worth $10,000,
then send me an email summary of all deals created today"

# Gets processed as:
1. Create Contact: David Wilson (david@tech.com)
2. Create Deal: David Wilson ($10,000)
3. Query Deals: Created today
4. Generate Email Summary
5. Send Email Notification
```

#### Error Recovery Examples
```python
# Partial Success Scenario
"Create contacts for Eve, Frank, and Grace, then create deals for all three"

# If Eve and Frank succeed but Grace fails:
✅ Contact Created: Eve Johnson
✅ Contact Created: Frank Miller  
❌ Contact Creation Failed: Grace Davis (Invalid email format)
✅ Deal Created: Eve Johnson ($0)
✅ Deal Created: Frank Miller ($0)
⚠️ Deal Creation Skipped: Grace Davis (Contact not found)

# User receives:
"Successfully created contacts for Eve and Frank, and deals for both. 
Grace's contact creation failed due to invalid email format. 
Would you like to retry with a valid email address?"
```

## 🛠️ Error Handling Architecture

### Error Categories
1. **Validation Errors**: Invalid data format, missing required fields
2. **API Errors**: HubSpot API failures, rate limiting
3. **Network Errors**: Connection timeouts, DNS failures
4. **Authentication Errors**: Token expiration, invalid credentials
5. **System Errors**: Internal processing failures

### Error Recovery Strategies
- **Automatic Retry**: Transient failures with exponential backoff
- **Alternative Methods**: Different API endpoints or approaches
- **Data Validation**: Pre-operation validation to prevent errors
- **Graceful Degradation**: Continue with available functionality
- **User Guidance**: Suggest solutions for user-correctable errors

### Error Reporting
- **Task-Level Reporting**: Individual operation success/failure
- **Aggregated Summaries**: Overall operation results
- **Debug Information**: Technical details for troubleshooting
- **User-Friendly Messages**: Simplified explanations for users
- **Actionable Suggestions**: Next steps for error resolution

## 🛠️ Troubleshooting

### Common Issues

1. **OAuth Authorization Failed**
   - Check HubSpot app configuration
   - Verify redirect URI matches exactly
   - Ensure required scopes are enabled

2. **GROQ API Errors**
   - Verify GROQ API key is correct
   - Check API rate limits
   - Ensure model name is correct

3. **Email Delivery Issues**
   - Verify SMTP credentials
   - Check firewall settings
   - Ensure app password is used (not regular password)

4. **Connection Errors**
   - Verify API server is running
   - Check network connectivity
   - Ensure correct API base URL

### Debug Mode
Enable debug logging by setting:
```env
LOG_LEVEL=DEBUG
APP_ENV=development
```

### Log Files
- **Application Logs**: `app/shared/logs/app_logs/app_logs.txt`
- **Error Logs**: `app/shared/logs/app_errors/error_logs.txt`

## 🏗️ Clean Architecture Implementation

This project follows **Clean Architecture** principles with proper separation of concerns  The codebase is organized into distinct layers with clear boundaries and responsibilities.

### Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │   FastAPI       │  │   Streamlit     │  │   REST API   │ │
│  │   Endpoints     │  │   Web UI        │  │   Controllers│ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                   Application Layer                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │   Use Cases     │  │   Services      │  │   DTOs       │ │
│  │   (Orchestrator)│  │   (Email, CRM)  │  │   (Requests) │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                     Domain Layer                            │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │   Entities      │  │   Value Objects │  │   Interfaces │ │
│  │   (Contact,     │  │   (Email, ID)   │  │   (Repos)    │ │
│  │    Deal)        │  │                 │  │              │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                  Infrastructure Layer                       │
│  ┌─────────────────┐  ┌─────────────────┐  ┌──────────────┐ │
│  │   External APIs │  │   Database      │  │   Services   │ │
│  │   (HubSpot,     │  │   (Token Store) │  │   (SMTP)     │ │
│  │    GROQ)        │  │                 │  │              │ │
│  └─────────────────┘  └─────────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Dependency Flow
- **Dependencies point inward**: Outer layers depend on inner layers
- **Domain layer has no dependencies**: Pure business logic
- **Infrastructure implements domain interfaces**: Dependency inversion
- **Application orchestrates domain and infrastructure**: Use cases


## 🚀 **Poetry Setup & Development**

### **Installation with Poetry**

```bash
# Install Poetry (if not already installed)
curl -sSL https://install.python-poetry.org | python3 -

# Clone and setup project
git clone https://github.com/TahaDataAlchemy/CRM-AI-AGENT.git

# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Install pre-commit hooks
poetry run pre-commit install
```

### **Development Commands**

```bash
# Start API server
poetry poetry run uvicorn app.server:app --reload

# Start Streamlit UI
poetry run uvicorn app.server:app --reload

```

## 🔄 **Data Flow Examples**

### **Contact Creation Flow**
```
1. User Input (Streamlit) 
   ↓
2. API Request (contact_controller.py)
   ↓
3. DTO Validation (contact_dto.py)
   ↓
4. Use Case (create_contact.py)
   ↓
5. Domain Validation (contact.py)
   ↓
6. Repository Call (hubspot_contact_repository.py)
   ↓
7. External API (hubspot_client.py)
   ↓
8. Response Processing
   ↓
9. Email Notification (email_service.py)
   ↓
10. User Response
```

### **Multi-Task Workflow Flow**
```
1. Complex Query Input
   ↓
2. Query Decomposer (query_decomposer.py)
   ↓
3. Task Extraction & Validation
   ↓
4. Orchestrator Service (orchestrator_service.py)
   ↓
5. Parallel Use Case Execution
   ├── Create Contact Use Case
   ├── Create Deal Use Case
   └── Send Email Use Case
   ↓
6. Individual Repository Calls
   ↓
7. External API Operations
   ↓
8. Result Aggregation
   ↓
9. Response Generation
   ↓
10. User Notification
```

## 🛡️ **Error Handling Architecture**

### **Error Propagation**
```
External API Error
    ↓
Infrastructure Layer (hubspot_client.py)
    ↓
Repository Layer (hubspot_contact_repository.py)
    ↓
Application Layer (create_contact.py)
    ↓
Presentation Layer (contact_controller.py)
    ↓
User-Friendly Response
```


### **Environment Variables**
```env
# HubSpot Configuration
HUBSPOT_CLIENT_ID=your_client_id
HUBSPOT_CLIENT_SECRET=your_client_secret
HUBSPOT_REDIRECT_URI=http://localhost:8000/auth/callback

# GROQ Configuration
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama3-8b-8192

# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# Application Configuration
APP_ENV=development
LOG_LEVEL=INFO
API_HOST=0.0.0.0
API_PORT=8000
STREAMLIT_PORT=8501
```

### **Configuration Classes**
- **`Settings`**: Main application settings
- **`HubSpotSettings`**: HubSpot-specific configuration
- **`EmailSettings`**: Email service configuration
- **`LoggingSettings`**: Logging configuration

## 📈 **Monitoring & Logging**

### **Logging Structure**
```
logs/
├── app.log              # Application logs
├── error.log            # Error logs

```


## 🔒 **Security Considerations**

### **Authentication & Authorization**
- **OAuth 2.0**: Secure HubSpot authentication
- **Token Management**: Secure token storage and refresh
- **Input Validation**: Comprehensive input sanitization
- **Rate Limiting**: API rate limiting protection

### **Data Protection**
- **Environment Variables**: Sensitive data in environment variables
- **Input Validation**: Pydantic models for request validation
- **Error Handling**: No sensitive data in error messages
- **Logging**: No sensitive data in logs



**Built with ❤️ using FastAPI, Streamlit, GROQ LLM, and HubSpot API** 




**Visuals of Streamlit and postman**

**Converstaion UI**
![image](https://github.com/user-attachments/assets/59ed5052-ce52-4a49-b1d9-379299482d22)
![image](https://github.com/user-attachments/assets/b19d4626-fd6a-4ca4-b262-ab21ca299b4f)
![image](https://github.com/user-attachments/assets/b738e944-9f82-4f0b-a7fe-7aa151ccab83)

**postman Api Responsis**
![image](https://github.com/user-attachments/assets/5404a589-7ad2-4adb-80d5-e6208588769c)
![image](https://github.com/user-attachments/assets/63398ade-3701-4c4c-ac4b-e19ed76f0292)


**APIS TO SEE FLOW OF CODE AND AUTH**
http://localhost:8000/agent/process : all Operation performs through this of Ai-agent 

http://localhost:8000/auth/authorize_user : this is use for authorizing user

http://localhost:8000/auth/callback : this is redirect url

**All apis**


![image](https://github.com/user-attachments/assets/7c572fbc-7e9b-4d12-a8f6-2d7ab9e22bcb)


**Email Responses**

![image](https://github.com/user-attachments/assets/ceedb31e-d047-4df1-aa92-fb5bb9252a46)

![image](https://github.com/user-attachments/assets/3503e586-54b0-44a4-bcd2-01c4c5e94644)

![image](https://github.com/user-attachments/assets/d10cb2dc-1ac8-42fa-a449-47575df56dce)

![image](https://github.com/user-attachments/assets/8804e115-5793-41b6-abea-49656b24fd07)



