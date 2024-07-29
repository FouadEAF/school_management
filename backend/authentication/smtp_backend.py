import smtplib
from django.core.mail.backends.smtp import EmailBackend
import certifi
from ssl import create_default_context, _create_unverified_context


class SSLUnverifiedEmailBackend(EmailBackend):
    def _get_connection(self):
        if self.connection:
            return self.connection
        self.connection = smtplib.SMTP(self.host, self.port)
        self.connection.ehlo()
        if self.use_tls:
            # Create SSL context with certifi CA bundle
            context = create_default_context(cafile=certifi.where())
            self.connection.starttls(context=context)
            self.connection.ehlo()
        if self.username and self.password:
            self.connection.login(self.username, self.password)
        return self.connection
