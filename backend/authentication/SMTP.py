import mailersend

mailer = mailersend.NewApiClient()

subject = "Subject"
text = "Greetings from the team, you got this message through MailerSend."
html = "Greetings from the team, you got this message through MailerSend."

my_mail = "info@domain.com"
subscriber_list = ['recipient1@email.com',
                   'recipient2@email.com', 'recipient3@email.com']

mailer.send(my_mail, subscriber_list, subject, html, text)
