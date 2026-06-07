import smtplib
from email.message import EmailMessage
import mimetypes

# Dados de Envio
remetente = 'nordherosupport@gmail.com'
destinatario = 'caua.araujo@ufrpe.br'
assunto = 'Testando envio de email'
mensagem = """
Esta é uma mensagem de teste.

Att,
"""

senha = 'ihlg vbxt neli trlb'
anexo = './Features/emailteste.png'

# Cria um email
msg = EmailMessage()
msg['From'] = remetente
msg['To'] = destinatario
msg['Subject'] = assunto
msg.set_content(mensagem)

# Anexa um arquivo
mimetype, _ = mimetypes.guess_type(anexo)
mime_type, mime_subtype = mimetype.split('/')

with open(anexo,'rb') as arquivo:
    msg.add_attachment(arquivo.read(),maintype=mime_type, subtype=mime_subtype, filename=anexo)

# Realiza o envio do email
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as email:
    email.login(remetente, senha)
    email.send_message(msg)


print("Email enviado com sucesso!")
