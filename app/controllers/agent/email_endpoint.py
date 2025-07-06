from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional, List, Any
from datetime import datetime
from app.domain.AiAgent.EmailAgent.usecase.email_agent import email_agent
from app.domain.AiAgent.EmailAgent.data.EmailDataModel import EmailType, EmailNotification
from app.infra.config import settings
from app.shared.utils.common_functions import CommonFuntions

router = APIRouter(prefix="/notifications", tags=["Email Notifications"])

class EmailTestRequest(BaseModel):
    email_type: EmailType
    to_email: Optional[str] = None
    test_data: Dict = {}

class NotificationConfig(BaseModel):
    recipient_email: str
    notification_type: EmailType
    operation_data: Dict[str, Any] = {}

@router.post("/send", summary="Send Custom Email Notification")
async def send_custom_notification(request: EmailTestRequest):
    """
    Send a custom email notification using predefined templates.
    
    **Purpose**: Allows testing and sending of specific notification types with custom data.
    
    **Parameters**:
    - `email_type`: Type of notification (contact_created, contact_updated, etc.)
    - `to_email`: Recipient email (optional, defaults to admin email)
    - `test_data`: Custom data to populate the email template
    
    **Use Cases**:
    - Testing email templates
    - Sending custom notifications
    - Manual notification triggers
    
    **Returns**: Email delivery status and message ID
    """
    try:
        CommonFuntions.write_log(f"Received custom notification request: {request.email_type.value}")
        CommonFuntions.write_log(f"Recipient: {request.to_email}")
        
        to_email = request.to_email if request.to_email else settings.EMAIL_USERNAME
        
        if request.email_type == EmailType.CONTACT_CREATED:
            response = email_agent.notify_contact_created(
                request.test_data, 
                to_email
            )
        elif request.email_type == EmailType.CONTACT_UPDATED:
            response = email_agent.notify_contact_updated(
                request.test_data, 
                to_email
            )
        elif request.email_type == EmailType.CONTACT_DELETED:
            response = email_agent.notify_contact_deleted(
                request.test_data, 
                to_email
            )
        elif request.email_type == EmailType.OPERATION_SUCCESS:
            response = email_agent.notify_operation_success(
                request.test_data.get("operation", "Test Operation"),
                request.test_data.get("details", "Test details"),
                to_email
            )
        elif request.email_type == EmailType.OPERATION_FAILED:
            response = email_agent.notify_operation_failed(
                request.test_data.get("operation", "Test Operation"),
                request.test_data.get("error", "Test error"),
                to_email
            )
        else:
            CommonFuntions.write_error_log(f"Unsupported email type: {request.email_type.value}")
            raise HTTPException(status_code=400, detail="Unsupported email type")
        
        CommonFuntions.write_log(f"Custom notification sent successfully: {response.success}")
        
        return {
            "success": response.success,
            "message": "Email sent successfully" if response.success else f"Failed to send email: {response.error}",
            "sent_to": response.sent_to,
            "message_id": response.message_id,
            "notification_type": request.email_type.value
        }
        
    except Exception as e:
        CommonFuntions.write_error_log(f"Custom notification error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/templates", summary="Get Available Notification Templates")
async def get_notification_templates():
    """
    Retrieve all available email notification templates and their descriptions.
    
    **Purpose**: Provides information about all supported notification types for integration and documentation.
    
    **Use Cases**:
    - API documentation
    - Frontend integration
    - Template selection for custom notifications
    
    **Returns**: List of all available notification types with descriptions
    """
    return {
        "notification_templates": [
            {
                "template_id": EmailType.CONTACT_CREATED.value,
                "name": "Contact Creation Notification",
                "description": "Automated notification sent when a new contact is successfully created in the CRM",
                "trigger": "POST /contacts/",
                "template_type": "success_notification"
            },
            {
                "template_id": EmailType.CONTACT_UPDATED.value,
                "name": "Contact Update Notification", 
                "description": "Automated notification sent when an existing contact is successfully updated",
                "trigger": "PATCH /contacts/{id}",
                "template_type": "update_notification"
            },
            {
                "template_id": EmailType.CONTACT_DELETED.value,
                "name": "Contact Deletion Notification",
                "description": "Automated notification sent when a contact is successfully deleted from the CRM",
                "trigger": "DELETE /contacts/{id}",
                "template_type": "deletion_notification"
            },
            {
                "template_id": EmailType.OPERATION_SUCCESS.value,
                "name": "Operation Success Notification",
                "description": "General success notification for any CRM operation completion",
                "trigger": "Any successful operation",
                "template_type": "success_notification"
            },
            {
                "template_id": EmailType.OPERATION_FAILED.value,
                "name": "Operation Failure Notification",
                "description": "Error notification sent when any CRM operation fails",
                "trigger": "Any failed operation",
                "template_type": "error_notification"
            }
        ],
        "total_templates": 5,
        "supported_formats": ["text", "html"]
    }

@router.post("/test-connection", summary="Test Email Service Connection")
async def test_email_connection():
    """
    Test the email service configuration and connectivity.
    
    **Purpose**: Validates that the email service is properly configured and can send emails.
    
    **Use Cases**:
    - System health checks
    - Configuration validation
    - Troubleshooting email issues
    - Pre-deployment testing
    
    **Returns**: Connection status and test email delivery confirmation
    """
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        # Create a simple test message
        msg = MIMEMultipart()
        msg['From'] = settings.EMAIL_USERNAME
        msg['To'] = settings.EMAIL_USERNAME
        msg['Subject'] = "CRM System - Email Service Test"
        
        body = """
        This is a test email from your CRM system.
        
        If you receive this email, it confirms that:
        ✅ Email service is properly configured
        ✅ SMTP connection is working
        ✅ Authentication is successful
        ✅ Email delivery is functional
        
        Timestamp: {timestamp}
        SMTP Server: {smtp_server}
        Port: {smtp_port}
        
        Your CRM email notifications are ready to use!
        """.format(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            smtp_server=settings.EMAIL_SMTP_SERVER,
            smtp_port=settings.EMAIL_SMTP_PORT
        )
        
        msg.attach(MIMEText(body, 'plain'))
        
        print(f"Testing email service connection...")
        print(f"SMTP Server: {settings.EMAIL_SMTP_SERVER}:{settings.EMAIL_SMTP_PORT}")
        print(f"Username: {settings.EMAIL_USERNAME}")
        
        # Send the email
        if settings.EMAIL_SMTP_PORT == 465:
            # Use SSL for port 465
            with smtplib.SMTP_SSL(settings.EMAIL_SMTP_SERVER, settings.EMAIL_SMTP_PORT) as server:
                server.login(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
                server.send_message(msg)
        else:
            # Use TLS for port 587
            with smtplib.SMTP(settings.EMAIL_SMTP_SERVER, settings.EMAIL_SMTP_PORT) as server:
                server.starttls()
                server.login(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
                server.send_message(msg)
        
        return {
            "success": True,
            "message": "Email service connection test successful",
            "sent_to": settings.EMAIL_USERNAME,
            "test_type": "connection_validation",
            "timestamp": datetime.now().isoformat(),
            "service_status": "operational"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__,
            "message": "Email service connection test failed",
            "test_type": "connection_validation",
            "timestamp": datetime.now().isoformat(),
            "service_status": "failed",
            "troubleshooting_tips": [
                "Check SMTP server and port configuration",
                "Verify email credentials",
                "Ensure 2FA is enabled and app password is used (for Gmail)",
                "Check firewall/network connectivity"
            ]
        }

@router.get("/status", summary="Get Email Service Status")
async def get_email_service_status():
    """
    Get the current status and configuration of the email notification service.
    
    **Purpose**: Provides system administrators with email service health and configuration information.
    
    **Use Cases**:
    - System monitoring
    - Configuration verification
    - Health check endpoints
    - Troubleshooting
    
    **Returns**: Email service configuration and status information
    """
    return {
        "service_name": "CRM Email Notification Service",
        "status": "active",
        "configuration": {
            "smtp_server": settings.EMAIL_SMTP_SERVER,
            "smtp_port": settings.EMAIL_SMTP_PORT,
            "username": settings.EMAIL_USERNAME,
            "authentication": "enabled",
            "tls_encryption": "enabled"
        },
        "capabilities": {
            "supported_templates": 5,
            "html_support": True,
            "text_support": True,
            "batch_notifications": True,
            "custom_notifications": True
        },
        "last_updated": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@router.post("/batch", summary="Send Batch Notifications")
async def send_batch_notifications(notifications: List[NotificationConfig]):
    """
    Send multiple email notifications in a single request.
    
    **Purpose**: Efficiently send multiple notifications for bulk operations or system events.
    
    **Parameters**:
    - `notifications`: List of notification configurations
    
    **Use Cases**:
    - Bulk contact operations
    - System-wide notifications
    - Batch processing results
    - Multi-user notifications
    
    **Returns**: Results for each notification in the batch
    """
    results = []
    
    for notification in notifications:
        try:
            response = email_agent.send_notification(
                EmailNotification(
                    to_email=notification.recipient_email,
                    email_type=notification.notification_type,
                    operation_data=notification.operation_data
                )
            )
            results.append({
                "recipient": notification.recipient_email,
                "type": notification.notification_type.value,
                "success": response.success,
                "message_id": response.message_id,
                "error": response.error
            })
        except Exception as e:
            results.append({
                "recipient": notification.recipient_email,
                "type": notification.notification_type.value,
                "success": False,
                "error": str(e)
            })
    
    return {
        "batch_id": f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "total_notifications": len(notifications),
        "successful": len([r for r in results if r["success"]]),
        "failed": len([r for r in results if not r["success"]]),
        "results": results,
        "timestamp": datetime.now().isoformat()
    } 