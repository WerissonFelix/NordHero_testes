import smtplib

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login("seu_email@gmail.com", "senha_gerada_topico_anterior")
server.sendmail(
  "remetente@gmail.com",
  "destinatario@gmail.com",
  "Conteúdo da mensagem")
server.quit()