
class AnalisadorLexico:
    

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
    
    def analisar(cls, arquivo_entrada ):
        with open (arquivo_entrada) as arq:
            cls.linhas = arq.readlines()
            cls.linhas[len(cls.linhas)-1] += 'º'
        
        cls.caractere_atual = cls.linhas[cls.linha_atual][cls.indice_caractere_atual]
        cls.af_0()
        
        """
        saida = {'saida':[]}   

        for r in cls.tokens_resposta:
            
            saida['saida'].append(
                    {
                        'token': r[0],
                        'lexema': r[1],
                        'linha': r[2] 
                    }
                )
                
                """
           
        return cls.tokens_resposta
            

    def prox_caractere(cls):

        if cls.indice_caractere_atual < len(cls.linhas[cls.linha_atual])-1:
            cls.indice_caractere_atual += 1
            cls.caractere_atual = cls.linhas[cls.linha_atual][cls.indice_caractere_atual]
            
        else:
            cls.linha_atual += 1
            cls.indice_caractere_atual = 0
            cls.caractere_atual = cls.linhas[cls.linha_atual][cls.indice_caractere_atual]
         
    def define_token(cls,lex):

        cls.lexema_atual = lex
        cls.token_atual = cls.lexema_token[cls.lexema_atual]
        cls.tokens_resposta.append((cls.token_atual,cls.lexema_atual, cls.linha_atual)) 

    def af_0(cls):   
        while cls.caractere_atual != 'º':
            simbolos=['(',')','{','}',',',';',':','*','+','/']  
            invalidos = ['', '\n', "'", '"']

            if cls.caractere_atual == ' ':
                cls.prox_caractere()
            if cls.caractere_atual in simbolos:
                cls.define_token(cls.caractere_atual)
                cls.prox_caractere()
            elif cls.caractere_atual == '=':
                cls.af_1()
            elif cls.caractere_atual == '!':
                cls.af_2() 
            elif cls.caractere_atual == '<':
                cls.af_3()
            elif cls.caractere_atual == '>':
                cls.af_4()  
            elif cls.caractere_atual == '-':
                cls.af_5()  
            elif cls.caractere_atual.isalpha() and cls.caractere_atual not in invalidos:
                cls.af_6() 
            elif cls.caractere_atual.isnumeric() and cls.caractere_atual not in invalidos:
                cls.af_7() 
            elif cls.caractere_atual == "'":
                cls.af_9()
            elif cls.caractere_atual == '"':
                cls.af_10()                       
            else:
                if cls.caractere_atual.strip() != '':
                    cls.tokens_resposta.append(('simbolo invalido',cls.caractere_atual, cls.linha_atual))
                cls.prox_caractere()

    def af_1(cls):  
        anterior = cls.caractere_atual

        cls.prox_caractere()
        if cls.caractere_atual == '=':
                cls.define_token(anterior + cls.caractere_atual)     
                cls.prox_caractere()   
        else:
                cls.define_token(anterior)

    def af_2(cls):  
        anterior = cls.caractere_atual

        cls.prox_caractere()
        if cls.caractere_atual == '=':
                cls.define_token(anterior + cls.caractere_atual)     
                cls.prox_caractere()   
        else:
                raise Exception ('Ops! Erro léxico')   

    def af_3(cls):   
        anterior = cls.caractere_atual

        cls.prox_caractere()
        if cls.caractere_atual == '=':
                cls.define_token(anterior + cls.caractere_atual)     
                cls.prox_caractere()   
        else:
            cls.define_token(anterior)        

    def af_4(cls):
        anterior = cls.caractere_atual

        cls.prox_caractere()
        if cls.caractere_atual == '=':
            cls.define_token(anterior + cls.caractere_atual)     
            cls.prox_caractere()   
        else:
            cls.define_token(anterior)

    def af_5(cls):
        anterior = cls.caractere_atual

        cls.prox_caractere()
        if cls.caractere_atual == '>':
            cls.define_token(anterior + cls.caractere_atual)     
            cls.prox_caractere()   
        else:
            cls.define_token(anterior)

    def af_6(cls):

        palavra = cls.caractere_atual
        cls.prox_caractere()
        while cls.caractere_atual.isalnum():
            palavra += cls.caractere_atual    
            cls.prox_caractere()
        palavra = palavra.strip()
        if palavra in cls.reservada:
            cls.define_token(palavra)  
        elif len(palavra) > 0: 
            cls.lexema_atual = palavra
            cls.token_atual = "ID"
            cls.tokens_resposta.append((cls.token_atual,cls.lexema_atual, cls.linha_atual))   

    def af_7(cls):
        
        numero = cls.caractere_atual
        cls.prox_caractere()
        while cls.caractere_atual.isnumeric():
            numero += cls.caractere_atual
            cls.prox_caractere()
        if (cls.caractere_atual == '.'):
            cls.af_8(numero)
        else:
            cls.lexema_atual = numero
            cls.token_atual = "INT_CONST"
            cls.tokens_resposta.append((cls.token_atual,cls.lexema_atual, cls.linha_atual))    

    def af_8(cls, numero):
        
        numero+=cls.caractere_atual
        cls.prox_caractere()
        while cls.caractere_atual.isnumeric():
            numero += cls.caractere_atual
            cls.prox_caractere()    
        cls.lexema_atual = numero
        cls.token_atual = "FLOAT_CONST"
        cls.tokens_resposta.append((cls.token_atual,cls.lexema_atual, cls.linha_atual))  

    def af_9(cls):
    
        simbolos=['(',')','{','}',',',';',':','*','+','/','-'] 

        cls.prox_caractere()
        simbolo = cls.caractere_atual
        if simbolo in simbolos or simbolo.isalnum():
            cls.prox_caractere()
            if cls.caractere_atual == "'":
                cls.lexema_atual = simbolo
                cls.token_atual = "CHAR_LITERAL"
                cls.tokens_resposta.append((cls.token_atual,cls.lexema_atual, cls.linha_atual))
                cls.prox_caractere() 
            else:
                raise Exception ('Ops! Erro léxico')    
        else:
            raise Exception ('Ops! Erro léxico')
    
    def af_10(cls):

        cls.prox_caractere()
        simbolo = cls.caractere_atual
        if simbolo == '{':
            cls.prox_caractere()
            if cls.caractere_atual == '}':
                cls.lexema_atual = simbolo + cls.caractere_atual
                cls.prox_caractere()
                if cls.caractere_atual == '"':
                    cls.token_atual = "FORMATTER_STRING"
                    cls.tokens_resposta.append((cls.token_atual,cls.lexema_atual, cls.linha_atual)) 
                    cls.prox_caractere()
            else:
                raise Exception ('Ops! Erro léxico')    
        else:
            raise Exception ('Ops! Erro léxico')








"""
with open(f"{arquivo_entrada[:-2]}_tokens.json", "w") as arquivo:     
    json.dump(saida, arquivo, indent=4)

with open(f"{arquivo_entrada[:-2]}.pkl","wb") as f:
          pickle.dump(cls.tokens_resposta, f) 
"""
      
    
