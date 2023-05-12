import pyodbc

def send_message(attachment):

    # sql server connection properties
    sql_server = pyodbc.connect(
        driver='{SQL Server}',
        server='MS248CSSQL01.SYSCO.NET',
        database='Pricing_Agreements')


    # Define the email parameters
    subject = 'test subject line'
    body = 'test Body'
    recipients = 'daniel.clark@sysco.com'
    #attachment = r'C:\path\to\your\report\file.ext'

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
        @body = @Body,
        @file_attachments = @Attachment;
    """, subject, body, recipients, attachment)

    # Commit the transaction and close the connection
    sql_server.commit()
    sql_server.close()


