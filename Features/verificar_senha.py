
from password_validator import PasswordValidator

def verifcar_senha(senha):
   schema = PasswordValidator()

   len_valido = schema.min(8).max(20).validate(senha)
   has_num = schema.has().digits().validate(senha)
   has_symbols = schema.has().symbols().validate(senha)
   spaces = schema.has().spaces().validate(senha)


   verificacao = {
       "len_valido": len_valido,
       "has_num": has_num,
       "has_symbols": has_symbols,
       "has_spaces": not spaces
   }

   mensagens_error = {
       "len_valido": "A senha deve ter 8 a 20 caracteres",
       "has_num": "A senha deve ter pelo menos 1 número",
       "has_symbols": "A senha deve ter pelo menos 1 símbolo",
       "has_spaces": "not spaces"
   }

   if False not in verificacao.values():
       return senha, True
   else:
       dados_errados = {mensagens_error[k]:v for k,v in verificacao.items() if v == False}

       return dados_errados, False