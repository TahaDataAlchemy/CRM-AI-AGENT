import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict, Any, Optional, List
from app.domain.AiAgent.EmailAgent.data.EmailDataModel import EmailType, EmailNotification, EmailResponse
from app.domain.AiAgent.EmailAgent.data.EmailTemplates import EmailTemplates
from app.infra.config import settings
from app.domain.AiAgent.OrchestratorAgent.data.DataModel import AgentResponse
from app.shared.utils.common_functions import CommonFuntions

class EmailAgent:
    def __init__(self):
        self.smtp_server = settings.EMAIL_SMTP_SERVER
        self.smtp_port = settings.EMAIL_SMTP_PORT
        self.username = settings.EMAIL_USERNAME
        self.password = settings.EMAIL_PASSWORD
        
    def send_notification(self, notification: EmailNotification) -> EmailResponse:
        """
        Send email notification
        """
        try:
            CommonFuntions.write_log(f"Attempting to send email to: {notification.to_email}")
            CommonFuntions.write_log(f"Email type: {notification.email_type}")
            CommonFuntions.write_log(f"SMTP Server: {self.smtp_server}:{self.smtp_port}")
            
            # Get email template
            template = EmailTemplates.get_template(notification.email_type, notification.operation_data)
            CommonFuntions.write_log(f"Email subject: {template.subject}")
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.username
            msg['To'] = notification.to_email
            msg['Subject'] = template.subject
            
            # Add text and HTML parts
            text_part = MIMEText(template.body, 'plain')
            msg.attach(text_part)
            
            if template.html_body:
                html_part = MIMEText(template.html_body, 'html')
                msg.attach(html_part)
            
            CommonFuntions.write_log("Connecting to SMTP server with SSL...")
            # Send email with SSL (for port 465)
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                CommonFuntions.write_log("Logging in to SMTP with SSL...")
                server.login(self.username, self.password)
                CommonFuntions.write_log("Sending message...")
                server.send_message(msg)
                CommonFuntions.write_log("Message sent successfully!")
            
            message_id = f"email_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            CommonFuntions.write_log(f"Email sent successfully with ID: {message_id}")
            
            return EmailResponse(
                success=True,
                sent_to=notification.to_email,
                message_id=message_id
            )
            
        except Exception as e:
            CommonFuntions.write_error_log(f"Email error: {str(e)}")
            CommonFuntions.write_error_log(f"Error type: {type(e).__name__}")
            return EmailResponse(
                success=False,
                error=str(e),
                sent_to=notification.to_email
            )
    
    def notify_contact_created(self, contact_data: Dict[str, Any], to_email: str) -> EmailResponse:
        """
        Send notification for contact creation
        """
        notification = EmailNotification(
            to_email=to_email,
            email_type=EmailType.CONTACT_CREATED,
            operation_data=contact_data
        )
        return self.send_notification(notification)
    
    def notify_contact_updated(self, contact_data: Dict[str, Any], to_email: str) -> EmailResponse:
        """
        Send notification for contact update
        """
        notification = EmailNotification(
            to_email=to_email,
            email_type=EmailType.CONTACT_UPDATED,
            operation_data=contact_data
        )
        return self.send_notification(notification)
    
    def notify_contact_deleted(self, contact_data: Dict[str, Any], to_email: str) -> EmailResponse:
        """
        Send notification for contact deletion
        """
        notification = EmailNotification(
            to_email=to_email,
            email_type=EmailType.CONTACT_DELETED,
            operation_data=contact_data
        )
        return self.send_notification(notification)
    
    def notify_operation_success(self, operation: str, details: str, to_email: str) -> EmailResponse:
        """
        Send notification for successful operation
        """
        operation_data = {
            "operation": operation,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        
        notification = EmailNotification(
            to_email=to_email,
            email_type=EmailType.OPERATION_SUCCESS,
            operation_data=operation_data
        )
        return self.send_notification(notification)
    
    def notify_operation_failed(self, operation: str, error: str, to_email: str) -> EmailResponse:
        """
        Send notification for failed operation
        """
        operation_data = {
            "operation": operation,
            "error": error,
            "timestamp": datetime.now().isoformat()
        }
        
        notification = EmailNotification(
            to_email=to_email,
            email_type=EmailType.OPERATION_FAILED,
            operation_data=operation_data
        )
        return self.send_notification(notification)
    
    def notify_multiple_operations(self, operations: List[Dict[str, Any]], to_email: str) -> List[EmailResponse]:
        """
        Send notifications for multiple operations
        """
        responses = []
        for operation in operations:
            if operation.get('success'):
                response = self.notify_operation_success(
                    operation.get('task', 'Unknown'),
                    operation.get('message', 'Operation completed'),
                    to_email
                )
            else:
                response = self.notify_operation_failed(
                    operation.get('task', 'Unknown'),
                    operation.get('error', 'Unknown error'),
                    to_email
                )
            responses.append(response)
        return responses

# Global email agent instance
email_agent = EmailAgent()
