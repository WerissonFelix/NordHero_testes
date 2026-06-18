import smtplib
from email.message import EmailMessage
import mimetypes
import random

class EmailSender:
    def __init__(self, destinatario: str, assunto: str, mensagem: str):
        self.remetente = 'nordherosupport@gmail.com'
        self.destinatario = destinatario
        self.assunto = assunto
        self.mensagem = mensagem
        self.senha = 'gthh kpvb pgcy gipe'
    def gerar_codigo(self):
            return str(random.randint(100000, 999999))

    def enviar_codigo(self):
        codigo = self.gerar_codigo()

        msg = EmailMessage()
        msg["From"] = self.remetente
        msg["To"] = self.destinatario
        msg["Subject"] = "Código de Verificação"

        msg.set_content(
            f"Seu código de verificação é: {codigo}\n\n"
            "Este código expira em alguns minutos."
        )

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as email:
            email.login(self.remetente, self.senha)
            email.send_message(msg)

        return codigo

    def send_email(self):
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
            email.login(self.remetente, self.senha)
            email.send_message(msg)

