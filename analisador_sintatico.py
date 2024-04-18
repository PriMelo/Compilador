import pickle
import json

arquivo_entrada = 'media.pkl'

token_resposta = []
token_saida = []

tabelaSimbolos ={}
nomeFuncao = None
contParam = 0 
tipoDado = {'VOID': -1, 'CHAR': 0, 'INT': 1, 'FLOAT': 2}

with open(arquivo_entrada, 'rb') as f:
    token_resposta = pickle.load(f)

i =0
token_atual = token_resposta[i][0]

def erro(*args):
    global token_atual, i
    
    token_esperado = args[1]
    token_saida.append(f'Erro sintatico - esperado: {token_esperado} na linha: {token_resposta[i][2]}')
    print('Erro sintático - esperado:', token_esperado, 'na linha:', token_resposta[i][2])
    
    if i < len(token_resposta)-1:
        i += 1
        token_atual = token_resposta[i][0]
    
    if args:
        args[0]()

def match(token_esperado):
    global token_atual, i
    
    token_saida.append(token_atual)
    print(token_atual)
        
    if token_esperado == token_atual:
        if i < len(token_resposta)-1:
            i += 1
            token_atual = token_resposta[i][0]
        
    else:
        erro()

def type_():
        
    if token_atual == 'INT':
        match('INT')

    elif token_atual == 'FLOAT':
        match('FLOAT')

    elif token_atual == 'CHAR':
        match('CHAR')
        
    else:
        erro(type_, 'INT | FLOAT | CHAR')
        
def tipoRetornoFuncao():
    
    if token_atual == 'ARROW':
        match('ARROW')
        type_()

    elif token_atual == 'simbolo invalido':
        erro(tipoRetornoFuncao, 'ARROW')   

    else:
        return
    
def atribuicaoOuChamada():
    
    if token_atual == 'ASSINGN':
        match('ASSINGN')
        expr()
        match('SEMICOLON')

    elif token_atual == 'LPAREN':
        match('LPAREN')
        listArgs()
        match('RPAREN')

    else:
        erro(atribuicaoOuChamada, 'ASSIGN | LPAREN')

def listArgs2():

    if token_atual == 'COMMA':
        match('COMMA')
        fator()
        listArgs2()

    elif token_atual == 'simbolo invalido':
        erro(listArgs2, 'COMMA')  

    else:
        return

def listArgs():
    
    if token_atual in ['ID', 'INT_CONST', 'FLOAT_CONST', 'CHAR_LITERAL', 'LPAREN']:
        fator()
        listArgs2()
    
    elif token_atual == 'simbolo invalido':
        erro(listArgs, 'ID | INT_CONST | FLOAT_CONST | CHAR_LITERAL | LPAREN' )  
    
    else:
        return
        
def chamadaFuncao():
    
    if token_atual == 'LPAREN':
        match('LPAREN')
        listArgs()
        match('RPAREN')

    elif token_atual == 'simbolo invalido':
        erro(chamadaFuncao, 'LPAREN')  

    else:
        return
        
def fator():
    
    if token_atual == 'ID':
        match('ID')
        chamadaFuncao()
    
    elif token_atual == 'INT_CONST':
        match('INT_CONST')

    elif token_atual == 'FLOAT_CONST':
        match('FLOAT_CONST')
        
    elif token_atual == 'CHAR_LITERAL':
        match('CHAR_LITERAL')
        
    elif token_atual == 'LPAREN':
        match('LPAREN')
        expr()
        match('RPAREN')

    else:
        erro(fator, 'LPAREN | ID | INT_CONST | FLOAT_CONST | CHAR_LITERAL')
        
def opMult():    
    
    if token_atual == 'MULT':
        match('MULT')
    
    elif token_atual == 'DIV':
        match('DIV')

    else:
        erro(opMult, 'MULT | DIV')    
        
def termoOpc():
    
    if token_atual in ['MULT', 'DIV']:
        opMult()
        fator()
        termoOpc()

    elif token_atual == 'simbolo invalido':
        erro(termoOpc, 'MULT | DIV')   

    else:
        return
    
def termo():
    
    fator()
    termoOpc()    
    
def opAdicao():
    
    if token_atual == 'PLUS':
        match('PLUS')
    
    elif token_atual == 'MINUS':
        match('MINUS')
    
    else:
        erro(opAdicao, 'PLUS | MINUS')

def adicaoOpc():
    
    if token_atual in ['PLUS', 'MINUS']:
        opAdicao()
        termo()
        adicaoOpc()

    elif token_atual == 'simbolo invalido':
        erro(adicaoOpc, 'PLUS | MINUS')  

    else:
        return

def adicao():
    
    termo()
    adicaoOpc()        

def opRel():
    if token_atual == 'LT':
        match('LT')
    
    elif token_atual == 'LTE':
        match('LTE')
    
    elif token_atual == 'GT':
        match('GT')
    
    elif token_atual == 'GTE':
        match('GTE')
    
    else:
        erro(opRel, 'LT | GT | LTE | GTE')

def relOpc():
    
    if token_atual in ['LT', 'GT', 'LTE', 'GTE']:
        opRel()
        adicao()
        relOpc()

    elif token_atual == 'simbolo invalido':
        erro(relOpc, 'LT | GT | LTE | GTE')  

    else:
        return
        
def rel():
    
    adicao()
    relOpc()

def opIgual():
    
    if token_atual == 'EQUAL':
        match('EQUAL')
    
    elif token_atual == 'NOTEQUAL':
        match('NOTEQUAL')
    
    else:
        erro(opIgual, 'EQUAL | NOTEQUAL')   

def exprOpc():
    
    if token_atual in ['EQUAL', 'NOTEQUAL']:
        opIgual()
        rel()
        exprOpc()

    elif token_atual == 'simbolo invalido':
        erro(exprOpc, 'EQUAL | NOTEQUAL')  

    else:
        return
        
def expr():
    
    rel()
    exprOpc()
      
def comandoSenao():
    
    if token_atual == 'ELSE':
        match('ELSE')
        comandoIf()

    elif token_atual == 'simbolo invalido':
        erro(comandoSenao, 'ELSE')  

    else:
        return
  
def comandoIf():
    
    if token_atual == 'IF':
        match('IF')
        expr()
        bloco()
        comandoSenao()
    
    elif token_atual == 'LBRACE':
        bloco()
    
    else:
        erro(comandoIf, 'IF | LBRACE')
    
    
def comando():
    
    if token_atual == 'ID':
        match('ID')
        atribuicaoOuChamada()
    
    elif token_atual == 'IF':
        comandoIf()
    
    elif token_atual == 'WHILE':
        match('WHILE')
        expr()
        bloco()
    
    elif token_atual == 'PRINT':
        match('PRINT')
        match('LPAREN')
        match("FORMATTER_STRING")
        match('COMMA')
        listArgs()
        match('RPAREN')
        match('SEMICOLON')
    
    elif token_atual == 'PRINTLN':
        match('PRINTLN')
        match('LPAREN')
        match("FORMATTER_STRING")
        match('COMMA')
        listArgs()
        match('RPAREN')
        match('SEMICOLON') 
    
    elif token_atual == 'RETURN':
        match('RETURN')
        expr()
        match('SEMICOLON')
    
    else:
        erro(comando, 'RETURN')
        
def varList2():

    if token_atual == 'COMMA':
        match('COMMA')
        match('ID')
        varList2()

    elif token_atual == 'simbolo invalido':
        erro(varList2, 'COMMA')      

    else:
        return

def varList():

    match('ID')
    varList2()  
    
def declaracao():

    match('LET')
    varList()
    match('COLON')
    type_()
    match('SEMICOLON')
        
def sequencia():

    if token_atual == 'LET':
        declaracao()
        sequencia()
    
    elif token_atual in ['ID','IF', 'WHILE', 'PRINT', 'PRINTLN', 'RETURN']:
        comando()
        sequencia()
    
    elif token_atual == 'simbolo invalido':
        erro(sequencia, 'LET | ID | IF | WHILE | PRINT | PRINTLN | RETURN ')    
    
    else:
        return    
        
def bloco():
    
    match('LBRACE')
    sequencia()
    match('RBRACE')
        
def listaParams2():
    global contParam
    
    if token_atual == 'COMMA':
        match('COMMA')
        match('ID')
        match('COLON')
        type_()
        tabelaSimbolos[nomeFuncao]['chave'].append(token_resposta[i-2][1])
        tabelaSimbolos[nomeFuncao]['nome'].append(token_resposta[i-2][1])
        tabelaSimbolos[nomeFuncao]['tipoDados'].append(tipoDado[token_resposta[i-1][0]])
        tabelaSimbolos[nomeFuncao]['posicaoParam'].append(contParam)        
        contParam += 1
        tabelaSimbolos[nomeFuncao]['chamada'].append(False)
        tabelaSimbolos[nomeFuncao]['nArgs'].append(None)
        tabelaSimbolos[nomeFuncao]['args'].append([None])
        listaParams2()

    elif token_atual == 'simbolo invalido':
        erro(listaParams2, 'COMMA')  

    else:
        return

def listaParams():
    global contParam
    
    if token_atual == 'ID':
        match('ID')
        match('COLON')
        type_()
        tabelaSimbolos[nomeFuncao]['chave'].append(token_resposta[i-2][1])
        tabelaSimbolos[nomeFuncao]['nome'].append(token_resposta[i-2][1])
        tabelaSimbolos[nomeFuncao]['tipoDados'].append(tipoDado[token_resposta[i-1][0]])
        tabelaSimbolos[nomeFuncao]['posicaoParam'].append(0)        
        contParam += 1
        tabelaSimbolos[nomeFuncao]['chamada'].append(False)
        tabelaSimbolos[nomeFuncao]['nArgs'].append(None)
        tabelaSimbolos[nomeFuncao]['args'].append([None])
        listaParams2()
        contParam = 0
    
    elif token_atual == 'simbolo invalido':
        erro(listaParams, 'ID')      
      
    else:
        return
       
def funcaoSeq():
    
    if token_atual == 'FUNCTION':        
        funcao()
        funcaoSeq()

    elif token_atual == 'simbolo invalido':
        erro(funcaoSeq, 'FUNCTION')      
        
    else:
        return    
        
def funcao():
    global nomeFuncao
    
    match('FUNCTION')
    tabela = {'chave': [], 'nome': [], 'tipoDados': [], 'posicaoParam': [], 'chamada': [], 'nArgs': [], 'args': []}
    tabelaSimbolos[token_resposta[i][1]] = tabela
    nomeFuncao = token_resposta[i][1]
    
    if token_atual == 'MAIN':
        match('MAIN')
    
    else:
        match('ID')
    
    match('LPAREN')
    listaParams()
    match('RPAREN')
    tipoRetornoFuncao()
    bloco()
         
def programa():
    
    if token_atual == 'FUNCTION':
        funcao()
        funcaoSeq()
    
    else:
        erro(programa, 'FUNCTION')
    

programa()

saida = {'saida':[]}   

for r in token_saida:    
    
        saida['saida'].append(
            {
                'token': r
            }
        )
        
with open(f"{arquivo_entrada[:-3]}_sintatico.json", "w") as arquivo:     
    json.dump(saida, arquivo, indent=4)