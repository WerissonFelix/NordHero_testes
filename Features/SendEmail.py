import smtplib
from email.message import EmailMessage
import mimetypes


class EmailSender:
    def __init__(self):
        self.remetente = 'nordherosupport@gmail.com'
        self.destinatario = 'caua.araujo@ufrpe.br'
        self.assunto = 'Testando envio de email'
        self.mensagem = """
        Esta é uma mensagem de teste.

        Att,
        """
    def send_email(self):
        senha = 'ihlg vbxt neli trlb'
        anexo = './Images/TesteDeEnvio.png'

        # Cria um email
        msg = EmailMessage()
        msg['From'] = self.remetente
        msg['To'] = self.destinatario
        msg['Subject'] = self.assunto
        msg.set_content(self.mensagem)


        # Anexa um arquivo
        mimetype, _ = mimetypes.guess_type(anexo)
        mime_type, mime_subtype = mimetype.split('/')

        with open(anexo,'rb') as arquivo:
            msg.add_attachment(arquivo.read(),maintype=mime_type, subtype=mime_subtype, filename=anexo)

        # Realiza o envio do email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as email:
            email.login(self.remetente, senha)
            email.send_message(msg)


print("Email enviado com sucesso!")


Teste = EmailSender()
Teste.send_email()