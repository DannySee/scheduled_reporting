import data_centers as cnn


def send_message(to, subject, body, attachment):

    sql_server = cnn.sql_server()

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
        @blind_copy_recipients = 'daniel.clark@sysco.com',
        @subject = @Subject,
        @body = @Body,
        @file_attachments = @Attachment;
    """, subject, body, to, attachment)

    # Commit the transaction and close the connection
    sql_server.commit()
    sql_server.close()