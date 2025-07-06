from typing import Dict, Any
from .EmailDataModel import EmailTemplate, EmailType

class EmailTemplates:
    @staticmethod
    def get_template(email_type: EmailType, data: Dict[str, Any]) -> EmailTemplate:
        """Get email template based on type and data"""
        
        if email_type == EmailType.CONTACT_CREATED:
            return EmailTemplate(
                subject=f"Contact Created Successfully - {data.get('firstname', 'New Contact')}",
                body=f"""
Hello,

A new contact has been successfully created in your CRM system.

Contact Details:
- Name: {data.get('firstname', 'N/A')} {data.get('lastname', '')}
- Email: {data.get('email', 'N/A')}
- Company: {data.get('company', 'N/A')}
- Phone: {data.get('phone', 'N/A')}

Contact ID: {data.get('id', 'N/A')}
Created At: {data.get('createdAt', 'N/A')}

Best regards,
Your CRM System
                """.strip(),
                html_body=f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .success {{ color: #28a745; font-weight: bold; }}
        .details {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 15px 0; }}
        .field {{ margin: 5px 0; }}
    </style>
</head>
<body>
    <h2 class="success">Contact Created Successfully</h2>
    <p>A new contact has been successfully created in your CRM system.</p>
    
    <div class="details">
        <h3>Contact Details:</h3>
        <div class="field"><strong>Name:</strong> {data.get('firstname', 'N/A')} {data.get('lastname', '')}</div>
        <div class="field"><strong>Email:</strong> {data.get('email', 'N/A')}</div>
        <div class="field"><strong>Company:</strong> {data.get('company', 'N/A')}</div>
        <div class="field"><strong>Phone:</strong> {data.get('phone', 'N/A')}</div>
        <div class="field"><strong>Contact ID:</strong> {data.get('id', 'N/A')}</div>
        <div class="field"><strong>Created At:</strong> {data.get('createdAt', 'N/A')}</div>
    </div>
    
    <p>Best regards,<br>Your CRM System</p>
</body>
</html>
                """
            )
        
        elif email_type == EmailType.CONTACT_UPDATED:
            return EmailTemplate(
                subject=f"Contact Updated Successfully - {data.get('firstname', 'Contact')}",
                body=f"""
Hello,

A contact has been successfully updated in your CRM system.

Contact Details:
- Name: {data.get('firstname', 'N/A')} {data.get('lastname', '')}
- Email: {data.get('email', 'N/A')}
- Company: {data.get('company', 'N/A')}
- Phone: {data.get('phone', 'N/A')}

Contact ID: {data.get('id', 'N/A')}
Updated At: {data.get('updatedAt', 'N/A')}

Best regards,
Your CRM System
                """.strip(),
                html_body=f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .update {{ color: #ffc107; font-weight: bold; }}
        .details {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 15px 0; }}
        .field {{ margin: 5px 0; }}
    </style>
</head>
<body>
    <h2 class="update">Contact Updated Successfully</h2>
    <p>A contact has been successfully updated in your CRM system.</p>
    
    <div class="details">
        <h3>Contact Details:</h3>
        <div class="field"><strong>Name:</strong> {data.get('firstname', 'N/A')} {data.get('lastname', '')}</div>
        <div class="field"><strong>Email:</strong> {data.get('email', 'N/A')}</div>
        <div class="field"><strong>Company:</strong> {data.get('company', 'N/A')}</div>
        <div class="field"><strong>Phone:</strong> {data.get('phone', 'N/A')}</div>
        <div class="field"><strong>Contact ID:</strong> {data.get('id', 'N/A')}</div>
        <div class="field"><strong>Updated At:</strong> {data.get('updatedAt', 'N/A')}</div>
    </div>
    
    <p>Best regards,<br>Your CRM System</p>
</body>
</html>
                """
            )
        
        elif email_type == EmailType.CONTACT_DELETED:
            return EmailTemplate(
                subject=f"Contact Deleted Successfully - {data.get('firstname', 'Contact')}",
                body=f"""
Hello,

A contact has been successfully deleted from your CRM system.

Deleted Contact Details:
- Name: {data.get('firstname', 'N/A')} {data.get('lastname', '')}
- Email: {data.get('email', 'N/A')}
- Company: {data.get('company', 'N/A')}

Contact ID: {data.get('id', 'N/A')}
Deleted At: {data.get('deletedAt', 'N/A')}

Best regards,
Your CRM System
                """.strip(),
                html_body=f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .delete {{ color: #dc3545; font-weight: bold; }}
        .details {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 15px 0; }}
        .field {{ margin: 5px 0; }}
    </style>
</head>
<body>
    <h2 class="delete">Contact Deleted Successfully</h2>
    <p>A contact has been successfully deleted from your CRM system.</p>
    
    <div class="details">
        <h3>Deleted Contact Details:</h3>
        <div class="field"><strong>Name:</strong> {data.get('firstname', 'N/A')} {data.get('lastname', '')}</div>
        <div class="field"><strong>Email:</strong> {data.get('email', 'N/A')}</div>
        <div class="field"><strong>Company:</strong> {data.get('company', 'N/A')}</div>
        <div class="field"><strong>Contact ID:</strong> {data.get('id', 'N/A')}</div>
        <div class="field"><strong>Deleted At:</strong> {data.get('deletedAt', 'N/A')}</div>
    </div>
    
    <p>Best regards,<br>Your CRM System</p>
</body>
</html>
                """
            )
        
        elif email_type == EmailType.OPERATION_SUCCESS:
            return EmailTemplate(
                subject=f"Operation Completed Successfully",
                body=f"""
Hello,

The following operation has been completed successfully:

Operation: {data.get('operation', 'N/A')}
Details: {data.get('details', 'N/A')}
Timestamp: {data.get('timestamp', 'N/A')}

Best regards,
Your CRM System
                """.strip(),
                html_body=f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .success {{ color: #28a745; font-weight: bold; }}
        .details {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 15px 0; }}
        .field {{ margin: 5px 0; }}
    </style>
</head>
<body>
    <h2 class="success">Operation Completed Successfully</h2>
    <p>The following operation has been completed successfully:</p>
    
    <div class="details">
        <div class="field"><strong>Operation:</strong> {data.get('operation', 'N/A')}</div>
        <div class="field"><strong>Details:</strong> {data.get('details', 'N/A')}</div>
        <div class="field"><strong>Timestamp:</strong> {data.get('timestamp', 'N/A')}</div>
    </div>
    
    <p>Best regards,<br>Your CRM System</p>
</body>
</html>
                """
            )
        
        elif email_type == EmailType.OPERATION_FAILED:
            return EmailTemplate(
                subject=f"❌ Operation Failed",
                body=f"""
Hello,

The following operation has failed:

Operation: {data.get('operation', 'N/A')}
Error: {data.get('error', 'N/A')}
Timestamp: {data.get('timestamp', 'N/A')}

Please check the system logs for more details.

Best regards,
Your CRM System
                """.strip(),
                html_body=f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .error {{ color: #dc3545; font-weight: bold; }}
        .details {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 15px 0; }}
        .field {{ margin: 5px 0; }}
    </style>
</head>
<body>
    <h2 class="error">❌ Operation Failed</h2>
    <p>The following operation has failed:</p>
    
    <div class="details">
        <div class="field"><strong>Operation:</strong> {data.get('operation', 'N/A')}</div>
        <div class="field"><strong>Error:</strong> {data.get('error', 'N/A')}</div>
        <div class="field"><strong>Timestamp:</strong> {data.get('timestamp', 'N/A')}</div>
    </div>
    
    <p>Please check the system logs for more details.</p>
    <p>Best regards,<br>Your CRM System</p>
</body>
</html>
                """
            )
        
        else:
            # Default template
            return EmailTemplate(
                subject="CRM System Notification",
                body=f"""
Hello,

A CRM operation has been performed.

Operation Type: {email_type.value}
Data: {data}

Best regards,
Your CRM System
                """.strip()
            ) 