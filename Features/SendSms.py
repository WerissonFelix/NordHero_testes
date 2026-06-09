from twilio.rest import Client
import random

class SmsSender:
    def __init__(self, destinatario: str):
        self.destinatario = destinatario
        self.account_sid = ""
        self.auth_token = ""
        self.remetente = ""

        self.client = Client(self.account_sid, self.auth_token)

    def gerar_codigo(self):
        return str(random.randint(100000, 999999))

    def enviar_codigo(self):
        codigo = self.gerar_codigo()

        mensagem = self.client.messages.create(
            body=f"Seu código de verificação é: {codigo}\n\nEste código expira em alguns minutos.",
            from_=self.remetente,
            to=self.destinatario
        )

        print(f"SMS enviado. SID: {mensagem.sid}")

        return codigo

    def enviar_sms(self, texto):
        mensagem = self.client.messages.create(
            body=texto,
            from_=self.remetente,
            to=self.destinatario
        )

        print(f"SMS enviado. SID: {mensagem.sid}")