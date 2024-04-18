import json
import pickle

arquivo_entrada = 'lexical_error.p'

reservada = ['fn', 'main', 'let', 'if', 'else', 'while', 'return', 'int', 'float', 'char', 'print', 'println']
lexema_token = {'main':'MAIN', 'fn': 'FUNCTION', 'if': 'IF', 'else': 'ELSE', 'while': 'WHILE', 'return': 'RETURN', 'let':'LET',
                'int':'INT', 'float':'FLOAT', 'char':'CHAR', 'print':'PRINT', 'println':'PRINTLN', '{': 'LBRACE', '}':'RBRACE',
                '(':'LPAREN', ')':'RPAREN', ':': 'COLON', ';': 'SEMICOLON', ',':'COMMA', '->':'ARROW', '=': 'ASSINGN',
                '==':'EQUAL', '!=':'NOTEQUAL', '<': 'LT', '>':'GT', '<=':'LTE', '>=':'GTE', '+':'PLUS', '-':'MINUS', '*':'MULT',
                '/':'DIV', '.':'POINT'}
linhas = []
tokens_resposta = []
linha_atual = 0
indice_caractere_atual = 0
caractere_atual =''
lexema_atual =""
estado_atual = 0

def prox_caractere():
    global indice_caractere_atual
    global linha_atual
    global caractere_atual

    if indice_caractere_atual < len(linhas[linha_atual])-1:
        indice_caractere_atual += 1
        caractere_atual = linhas[linha_atual][indice_caractere_atual]
          
    else:
        linha_atual += 1
        indice_caractere_atual = 0
        caractere_atual = linhas[linha_atual][indice_caractere_atual]
         
def define_token(lex):
    global lexema_atual
    global token_atual
    global tokens_resposta

    lexema_atual = lex
    token_atual = lexema_token[lexema_atual]
    tokens_resposta.append((token_atual,lexema_atual, linha_atual)) 

def af_0():   
   while caractere_atual != 'º':
        simbolos=['(',')','{','}',',',';',':','*','+','/']  
        invalidos = ['', '\n', "'", '"']

        if caractere_atual == ' ':
            prox_caractere()
        if caractere_atual in simbolos:
            define_token(caractere_atual)
            prox_caractere()
        elif caractere_atual == '=':
            af_1()
        elif caractere_atual == '!':
            af_2() 
        elif caractere_atual == '<':
            af_3()
        elif caractere_atual == '>':
            af_4()  
        elif caractere_atual == '-':
            af_5()  
        elif caractere_atual.isalpha() and caractere_atual not in invalidos:
            af_6() 
        elif caractere_atual.isnumeric() and caractere_atual not in invalidos:
            af_7() 
        elif caractere_atual == "'":
            af_9()
        elif caractere_atual == '"':
            af_10()                       
        else:
            if caractere_atual.strip() != '':
                tokens_resposta.append(('simbolo invalido',caractere_atual, linha_atual))
            prox_caractere()
                     

def af_1():  
   global caractere_atual  
   anterior = caractere_atual

   prox_caractere()
   if caractere_atual == '=':
        define_token (anterior + caractere_atual)     
        prox_caractere()   
   else:
        define_token(anterior)

def af_2():  
   global caractere_atual 
   anterior = caractere_atual

   prox_caractere()
   if caractere_atual == '=':
        define_token (anterior + caractere_atual)     
        prox_caractere()   
   else:
        raise Exception ('Ops! Erro léxico')   

def af_3():   
   global caractere_atual 
   anterior = caractere_atual

   prox_caractere()
   if caractere_atual == '=':
        define_token (anterior + caractere_atual)     
        prox_caractere()   
   else:
       define_token(anterior)        

def af_4():
    global caractere_atual 
    anterior = caractere_atual

    prox_caractere()
    if caractere_atual == '=':
            define_token (anterior + caractere_atual)     
            prox_caractere()   
    else:
       define_token(anterior)

def af_5():
    global caractere_atual 
    anterior = caractere_atual

    prox_caractere()
    if caractere_atual == '>':
        define_token (anterior + caractere_atual)     
        prox_caractere()   
    else:
       define_token(anterior)

def af_6():
    global lexema_atual
    global token_atual
    global caractere_atual
    global tokens_resposta

    palavra = caractere_atual
    prox_caractere()
    while caractere_atual.isalnum():
        palavra += caractere_atual    
        prox_caractere()
    palavra = palavra.strip()
    if palavra in reservada:
        define_token(palavra)  
    elif len(palavra) > 0: 
        lexema_atual = palavra
        token_atual = "ID"
        tokens_resposta.append((token_atual,lexema_atual, linha_atual))   

def af_7():
    global lexema_atual
    global token_atual
    global caractere_atual
    global tokens_resposta

    numero = caractere_atual
    prox_caractere()
    while caractere_atual.isnumeric():
        numero += caractere_atual
        prox_caractere()
    if (caractere_atual == '.'):
        af_8(numero)
    else:
        lexema_atual = numero
        token_atual = "INT_CONST"
        tokens_resposta.append((token_atual,lexema_atual, linha_atual))    

def af_8(numero):
    global lexema_atual
    global token_atual
    global caractere_atual
    global tokens_resposta

    numero+=caractere_atual
    prox_caractere()
    while caractere_atual.isnumeric():
        numero += caractere_atual
        prox_caractere()    
    lexema_atual = numero
    token_atual = "FLOAT_CONST"
    tokens_resposta.append((token_atual,lexema_atual, linha_atual))  

def af_9():
    global lexema_atual
    global token_atual
    global caractere_atual
    global tokens_resposta

    simbolos=['(',')','{','}',',',';',':','*','+','/','-'] 

    prox_caractere()
    simbolo = caractere_atual
    if simbolo in simbolos or simbolo.isalnum():
        prox_caractere()
        if caractere_atual == "'":
            lexema_atual = simbolo
            token_atual = "CHAR_LITERAL"
            tokens_resposta.append((token_atual,lexema_atual, linha_atual))
            prox_caractere() 
        else:
            raise Exception ('Ops! Erro léxico')    
    else:
        raise Exception ('Ops! Erro léxico')
#incompleto e ainda não verificou o fecha "    
def af_10():
    global lexema_atual
    global token_atual
    global caractere_atual
    global tokens_resposta

    prox_caractere()
    simbolo = caractere_atual
    if simbolo == '{':
        prox_caractere()
        if caractere_atual == '}':
            lexema_atual = simbolo + caractere_atual
            prox_caractere()
            if caractere_atual == '"':
                token_atual = "FORMATTER_STRING"
                tokens_resposta.append((token_atual,lexema_atual, linha_atual)) 
                prox_caractere()
        else:
            raise Exception ('Ops! Erro léxico')    
    else:
        raise Exception ('Ops! Erro léxico')


with open (arquivo_entrada) as arq:
   linhas = arq.readlines()
   linhas[len(linhas)-1] += 'º'

caractere_atual = linhas[linha_atual][indice_caractere_atual]
af_0()

print(tokens_resposta)   

saida = {'saida':[]}   

for r in tokens_resposta:
    
    if 'simbolo invalido' not in r[0]:
        saida['saida'].append(
            {
                'token': r[0],
                'lexema': r[1],
                'linha': r[2] 
            }
        )
    else:
        
        saida['saida'].append(
            {
                'Erro': r[0],
                'simbolo': r[1],
                'linha': r[2] 
            }
        )
        
       
with open(f"{arquivo_entrada[:-2]}_tokens.json", "w") as arquivo:     
    json.dump(saida, arquivo, indent=4)

with open(f"{arquivo_entrada[:-2]}.pkl","wb") as f:
          pickle.dump(tokens_resposta, f) 
      
    
