import win32com.client
from data_centers import sql_server

outlook = win32com.client.Dispatch('outlook.application')
mail = outlook.CreateItem(0)



def send_message(attachment):


    # Define the email parameters
    subject = 'test subject line'
    body = 'test Body'
    to = 'daniel.clark@sysco.com'

    # Execute the stored procedure to send the email
    sql_server.execute("""
    DECLARE @MailProfile VARCHAR(50) = 'Scheduled_Reporting';
    DECLARE @Subject NVARCHAR(255) = ?;
    DECLARE @Body NVARCHAR(MAX) = ?;
    DECLARE @Recipients NVARCHAR(MAX) = ?;
    DECLARE @Attachment NVARCHAR(MAX) = ?;

    EXEC msdb.dbo.sp_send_dbmail
        @profile_name = @MailProfile,
        @recipients = @Recipients,
        @subject = @Subject,
        @body = @Body;
        @file_attachments = @Attachment;
    """, subject, body, to, attachment)

    # Commit the transaction and close the connection
    sql_server.commit()
    sql_server.close()






    mail.To = to
    mail.Subject = subject
    mail.Body = body

    if attachment != '': mail.Attachments.Add(attachment)
    
    mail.Send()


