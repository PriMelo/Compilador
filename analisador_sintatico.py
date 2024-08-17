from first_follow import first, follow
import sys

class TabelaDeSimbolos:
    
    def __init__(self, nome_tab):
        self.nome = nome_tab
        self.tipo_retorno = None
        self.elementos = {}

           
        
    def novo_elemento(self,chave, lexema, tipo, pos_param, eh_chamada=False, num_args=0, args=[]):
        
        if lexema not in self.elementos:
        
            self.elementos[chave] ={
                'nome': lexema,
                'tipo_de_dado': tipo,
                'pos_param':pos_param,
                'eh_chamada': eh_chamada,
                'num_args': num_args,
                'args':args,
                'chave': chave
            }
            
        # elif -> se tiver duas chamadas de função iguais?
        
        else:
            print('Erro semântico: redeclaração de identificador')
    
    def get_elemento(self,lexema):
        
        if self.elementos[lexema]:
            
            return self.elementos[lexema]
        
        else:
            print('Erro: elemento não existe na tabela')
            
    def print_tab(self):
        print(f"Tabela {self.nome}")
        for e in self.elementos.values():
            print(f"chave:{e['chave']} nome: {e['nome']} tipo_de_dado: {e['tipo_de_dado']} pos_param: {e['pos_param']} eh_chamada: {e['eh_chamada']} num_args: {e['num_args']} args: {e['args']}")
        
        
        
    

class AnalisadorSintatico:
        
    token_resposta = []
    token_saida = []

    i =0
    token_atual = None
    tabelas = {}
    
    tipo_de_dado = None
    tabela_atual = None
    posicao_param = 0
    
    tipo_de_dado = {
            'VOID': -1,
            'CHAR': 0,
            'INT': 1,
            'FLOAT': 2       
        }
    
    def r_cria_tabela(cls, lexema):
        
        
        if lexema not in cls.tabelas:
            
            nova_tabela = TabelaDeSimbolos(lexema)
            cls.tabelas[lexema] = nova_tabela
            cls.tabela_atual = nova_tabela
            
        else:
            print('Erro: Função redeclarada')
    
   
    
    def nova_tabela(cls,nome_tab):
        cls.tabelas[nome_tab] = None
    
    def analisar(cls, saida_an_lexico):
        cls.token_resposta = saida_an_lexico.copy()
        cls.token_atual = cls.token_resposta[cls.i][0]
        cls.programa()
        
        saida = {'saida':[]}   

        for r in cls.token_saida:    
            
                saida['saida'].append(
                    {
                        'token': r
                    }
                )
                
        for k in cls.tabelas:
            print(cls.tabelas[k].print_tab())
        
        return saida
                
        

    def erro(cls,*args):       
        
        token_esperado = args[1]
        cls.token_saida.append(f'Erro sintatico - encontrado: {cls.token_resposta[cls.i][1]} esperado: {token_esperado} na linha: {cls.token_resposta[cls.i][2]}')
       # print('Erro sintático - esperado:', token_esperado, 'na linha:', cls.token_resposta[cls.i][2])
        if cls.i < len(cls.token_resposta)-1:
                       
            if args[0] and  not cls.token_atual in follow[args[0].__name__]:
              
                cls.i += 1
            
            cls.token_atual = cls.token_resposta[cls.i][0]
        
        if args[0] != None:
            args[0]()

    def match(cls,token_esperado):
                
        cls.token_saida.append(cls.token_atual)
            
        if token_esperado == cls.token_atual:
            if cls.i < len(cls.token_resposta)-1:
                cls.i += 1
                cls.token_atual = cls.token_resposta[cls.i][0]
            
        else:
            cls.erro(None,token_esperado)

    def type_(cls):
            
        if cls.token_atual == 'INT':
            cls.match('INT')
            return cls.tipo_de_dado[cls.token_resposta[cls.i-1][0]] 

        elif cls.token_atual == 'FLOAT':
            cls.match('FLOAT')
            return cls.tipo_de_dado[cls.token_resposta[cls.i-1][0]] 

        elif cls.token_atual == 'CHAR':
            cls.match('CHAR')
            return cls.tipo_de_dado[cls.token_resposta[cls.i-1][0]]
            
        else:
            cls.erro(cls.type_, 'INT | FLOAT | CHAR')
            return None
            
    def tipoRetornoFuncao(cls):
        
        if cls.token_atual == 'ARROW':
            cls.match('ARROW')
            tipo_retorno = cls.type_()
            return tipo_retorno

        elif cls.token_atual == 'simbolo invalido':
            cls.erro(cls.tipoRetornoFuncao, 'ARROW')   

        else:
            return
        
    def atribuicaoOuChamada(cls):
        
        if cls.token_atual == 'ASSINGN':
            cls.match('ASSINGN')
            cls.expr()
            cls.match('SEMICOLON')

        elif cls.token_atual == 'LPAREN':
            cls.match('LPAREN')
            cls.listArgs()
            cls.match('RPAREN')

        else:
            cls.erro(cls.atribuicaoOuChamada, 'ASSIGN | LPAREN')

    def listArgs2(cls,argumentos):

        if cls.token_atual == 'COMMA':
            cls.match('COMMA')
            arg = cls.fator()
            argumentos.append(arg) 
            cls.listArgs2(argumentos)
        

        elif cls.token_atual == 'simbolo invalido':
            cls.erro(cls.listArgs2, 'COMMA')  

        else:
            return

    def listArgs(cls):

        argumentos = []
        
        if cls.token_atual in ['ID', 'INT_CONST', 'FLOAT_CONST', 'CHAR_LITERAL', 'LPAREN']:
            f = cls.fator()
            argumentos.append(f)
    
            cls.listArgs2(argumentos)
            return argumentos
            
        
        elif cls.token_atual == 'simbolo invalido':
            cls.erro(cls.listArgs, 'ID | INT_CONST | FLOAT_CONST | CHAR_LITERAL | LPAREN' )  
        
        else:
            return
        
            
    def chamadaFuncao(cls):
        
        if cls.token_atual == 'LPAREN':
            cls.match('LPAREN')
            args = cls.listArgs()
            cls.match('RPAREN')
            return args

        elif cls.token_atual == 'simbolo invalido':
            cls.erro(cls.chamadaFuncao, 'LPAREN')  

        else:
            return -1
            
    def fator(cls):

        if cls.token_atual == 'ID':
            cls.match('ID')
            lexema = cls.token_resposta[cls.i-1][1]
            argumentos = cls.chamadaFuncao()
            if not argumentos == -1:
                tipo_tab_chamada = cls.tabelas[lexema].tipo_retorno
                cls.tabela_atual.novo_elemento(chave=lexema, lexema=lexema,tipo=tipo_tab_chamada, pos_param=-1, eh_chamada=True,num_args=len(argumentos),args=argumentos)
            
            return lexema
        
        elif cls.token_atual == 'INT_CONST':
            cls.match('INT_CONST')
            return cls.token_resposta[cls.i-1][1]

        elif cls.token_atual == 'FLOAT_CONST':
            cls.match('FLOAT_CONST')
            return cls.token_resposta[cls.i-1][1]
            
        elif cls.token_atual == 'CHAR_LITERAL':
            cls.match('CHAR_LITERAL')
            return cls.token_resposta[cls.i-1][1]
            
        elif cls.token_atual == 'LPAREN':
            cls.match('LPAREN')
            cls.expr()
            cls.match('RPAREN')
            return cls.token_resposta[cls.i-2][1]

        else:
            cls.erro(cls.fator, 'LPAREN | ID | INT_CONST | FLOAT_CONST | CHAR_LITERAL')
            return None
            
    def opMult(cls):    
        
        if cls.token_atual == 'MULT':
            cls.match('MULT')
        
        elif cls.token_atual == 'DIV':
            cls.match('DIV')

        else:
            cls.erro(cls.opMult, 'MULT | DIV')    
            
    def termoOpc(cls):
        
        if cls.token_atual in ['MULT', 'DIV']:
            cls.opMult()
            cls.fator()
            cls.termoOpc()

        elif cls.token_atual == 'simbolo invalido':
            cls.erro(cls.termoOpc, 'MULT | DIV')   

        else:
            return
        
    def termo(cls):
        
        cls.fator()
        cls.termoOpc()    
        
    def opAdicao(cls):
        
        if cls.token_atual == 'PLUS':
            cls.match('PLUS')
        
        elif cls.token_atual == 'MINUS':
            cls.match('MINUS')
        
        else:
            cls.erro(cls.opAdicao, 'PLUS | MINUS')

    def adicaoOpc(cls):
        
        if cls.token_atual in ['PLUS', 'MINUS']:
            cls.opAdicao()
            cls.termo()
            cls.adicaoOpc()

        elif cls.token_atual == 'simbolo invalido':
            cls.erro(cls.adicaoOpc, 'PLUS | MINUS')  

        else:
            return

    def adicao(cls):
        
        cls.termo()
        cls.adicaoOpc()        

    def opRel(cls):
        if cls.token_atual == 'LT':
            cls.match('LT')
        
        elif cls.token_atual == 'LTE':
            cls.match('LTE')
        
        elif cls.token_atual == 'GT':
            cls.match('GT')
        
        elif cls.token_atual == 'GTE':
            cls.match('GTE')
        
        else:
            cls.erro(cls.opRel, 'LT | GT | LTE | GTE')

    def relOpc(cls):
        
        if cls.token_atual in ['LT', 'GT', 'LTE', 'GTE']:
            cls.opRel()
            cls.adicao()
            cls.relOpc()

        elif cls.token_atual == 'simbolo invalido':
            cls.erro(cls.relOpc, 'LT | GT | LTE | GTE')  

        else:
            return
            
    def rel(cls):
        
        cls.adicao()
        cls.relOpc()

    def opIgual(cls):
        
        if cls.token_atual == 'EQUAL':
            cls.match('EQUAL')
        
        elif cls.token_atual == 'NOTEQUAL':
            cls.match('NOTEQUAL')
        
        else:
            cls.erro(cls.opIgual, 'EQUAL | NOTEQUAL')   

    def exprOpc(cls):
        
        if cls.token_atual in ['EQUAL', 'NOTEQUAL']:
            cls.opIgual()
            cls.rel()
            cls.exprOpc()

        elif cls.token_atual == 'simbolo invalido':
            cls.erro(cls.exprOpc, 'EQUAL | NOTEQUAL')  

        else:
            return
            
    def expr(cls):
        
        cls.rel()
        cls.exprOpc()
        
    def comandoSenao(cls):
        
        if cls.token_atual == 'ELSE':
            cls.match('ELSE')
            cls.comandoIf()

        elif cls.token_atual == 'simbolo invalido':
            cls.erro(cls.comandoSenao, 'ELSE')  

        else:
            return
    
    def comandoIf(cls):
        
        if cls.token_atual == 'IF':
            cls.match('IF')
            cls.expr()
            cls.bloco()
            cls.comandoSenao()
        
        elif cls.token_atual == 'LBRACE':
            cls.bloco()
        
        else:
            cls.erro(cls.comandoIf, 'IF | LBRACE')
        
        
    def comando(cls):

        if cls.token_atual == 'ID':
            cls.match('ID')
            cls.atribuicaoOuChamada()
        
        elif cls.token_atual == 'IF':
            cls.comandoIf()
        
        elif cls.token_atual == 'WHILE':
            cls.match('WHILE')
            cls.expr()
            cls.bloco()
        
        elif cls.token_atual == 'PRINT':
            
            cls.match('PRINT')
            lexema = cls.token_resposta[cls.i-1][1]
            cls.match('LPAREN')
            cls.match("FORMATTER_STRING")
            cls.match('COMMA')
            args = cls.listArgs()
            if args == None:
                args = []
            argumentos = ["sys_call(print)"] + args
            cls.match('RPAREN')
            cls.tabela_atual.novo_elemento(chave=lexema, lexema=lexema,tipo=-1, pos_param=-1, eh_chamada=True,num_args=len(argumentos),args=argumentos)

            cls.match('SEMICOLON')
        
        elif cls.token_atual == 'PRINTLN':
            cls.match('PRINTLN')
            lexema = cls.token_resposta[cls.i-1][1]
            cls.match('LPAREN')
            cls.match("FORMATTER_STRING")
            cls.match('COMMA')
            args = cls.listArgs()
            argumentos = ["sys_call(print)"] + args
            cls.match('RPAREN')
            cls.tabela_atual.novo_elemento(chave=lexema, lexema=lexema,tipo=-1, pos_param=-1, eh_chamada=True,num_args=len(argumentos),args=argumentos)
            cls.match('SEMICOLON') 
        
        elif cls.token_atual == 'RETURN':
            cls.match('RETURN')
            cls.expr()
            cls.match('SEMICOLON')
        
        else:
            cls.erro(cls.comando, 'RETURN')
            
    def varList2(cls,variaveis):

        if cls.token_atual == 'COMMA':
            cls.match('COMMA')
            cls.match('ID')
            variaveis.append(cls.token_resposta[cls.i-1][1])
            cls.varList2(variaveis)

        elif cls.token_atual == 'simbolo invalido':
            cls.erro(cls.varList2, 'COMMA')      

        elif cls.token_atual in follow[sys._getframe().f_code.co_name]:
            return
        else:
            cls.erro(getattr(cls, sys._getframe().f_code.co_name), 'COMMA | ' + ' | '.join(follow[sys._getframe().f_code.co_name]))
        

    def varList(cls):
        
        variaveis = []
        cls.match('ID')
        variaveis.append(cls.token_resposta[cls.i-1][1])
        cls.varList2(variaveis)  
        return variaveis
        
    def declaracao(cls):

        cls.match('LET')
        variaveis = cls.varList()
        cls.match('COLON')
        tipo = cls.type_()
        for v in variaveis:
            
            cls.tabela_atual.novo_elemento(chave=v, lexema=v,tipo=tipo, pos_param=-1)
        
        cls.match('SEMICOLON')
            
    def sequencia(cls):
        if cls.token_atual == 'LET':
            cls.declaracao()
            cls.sequencia()
        
        elif cls.token_atual in ['ID','IF', 'WHILE', 'PRINT', 'PRINTLN', 'RETURN']:
            cls.comando()
            cls.sequencia()
        
        elif cls.token_atual == 'simbolo invalido':
            cls.erro(cls.sequencia, 'LET | ID | IF | WHILE | PRINT | PRINTLN | RETURN ')    
        
        else:
            return    
            
    def bloco(cls):
        cls.match('LBRACE')
        cls.sequencia()
        cls.match('RBRACE')
            
    def listaParams2(cls):


        if cls.token_atual == 'COMMA':
            cls.match('COMMA')
            cls.posicao_param += 1
            cls.match('ID')
            lexema = cls.token_resposta[cls.i-1][1]
            cls.match('COLON')
            tipo = cls.type_() 
            cls.tabela_atual.novo_elemento(chave=lexema, lexema=lexema,tipo=tipo, pos_param=cls.posicao_param)
            cls.listaParams2()

        elif cls.token_atual == 'simbolo invalido':
            cls.erro(cls.listaParams2, 'COMMA')  

        else:
            return

    def listaParams(cls):
        cls.posicao_param = 0

        if cls.token_atual == 'ID':
            cls.match('ID')
            lexema = cls.token_resposta[cls.i-1][1]
            cls.match('COLON')
            tipo = cls.type_()
            cls.tabela_atual.novo_elemento(chave=lexema, lexema=lexema,tipo=tipo, pos_param=cls.posicao_param)
            cls.listaParams2()
        
        elif cls.token_atual in follow[sys._getframe().f_code.co_name]:
            return
        else:
            cls.erro(getattr(cls, sys._getframe().f_code.co_name), 'ID | ' + ' | '.join(follow[sys._getframe().f_code.co_name]) )

        
        
    def funcaoSeq(cls):
        
        if cls.token_atual == 'FUNCTION':        
            cls.funcao()
            cls.funcaoSeq()

        elif cls.token_atual == 'simbolo invalido':
            cls.erro(cls.funcaoSeq, 'FUNCTION')      
            
        else:
            return    
            
    def funcao(cls):

        cls.match('FUNCTION')
        
        if cls.token_atual == 'MAIN':
            cls.r_cria_tabela(cls.token_resposta[cls.i][1])
            cls.match('MAIN')
        
        elif cls.token_atual == 'ID':
            cls.r_cria_tabela(cls.token_resposta[cls.i][1])
            cls.match('ID')
        
        elif cls.token_atual == 'simbolo invalido':
            cls.erro(None, 'ID | MAIN')  
        
        else:
            cls.erro(None, 'ID| MAIN')
        
        cls.match('LPAREN')
        cls.listaParams()
        cls.match('RPAREN')
        tipo_retorno = cls.tipoRetornoFuncao()
        cls.tabela_atual.tipo_retorno = tipo_retorno
        
        cls.bloco()
            
    def programa(cls):
        
        if cls.token_atual == 'FUNCTION':
            cls.funcao()
            cls.funcaoSeq()
        
        else:
            cls.erro(cls.programa, 'FUNCTION')
            
        
        

    

    