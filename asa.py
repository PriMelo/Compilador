class AstNode:
    
    def __init__(self):
        self.node_type = None
        self.children = []
        self.node_type = None
        self.data_type = None
        self.op = None

class Bloco_node(AstNode):
    def __init__(self,children:list):
        super().__init__()
        self.children = children[::]
        self.node_type = 'BLOCO'
        self.children = children[::]
        
class Function_node(AstNode):
    def __init__(self, node_type, filho:Bloco_node, data_type, op):
        super().__init__()
        self.children.append(filho)
        self.node_type = node_type
        self.data_type = data_type
        self.op = op
        
        
class RelOp_node(AstNode):
    def __init__(self,filho_esq, filho_dir,op):
        super().__init__()
        self.children.append(filho_esq)
        self.children.append(filho_dir)
        self.node_type = 'RELOP'
        self.data_type = None
        self.op = op
        self.esq = filho_esq
        self.dir = filho_dir
        
   

class ArithOp_node(AstNode):
    def __init__(self,filho_esq, filho_dir,op):
        super().__init__()
        self.children.append(filho_esq)
        self.children.append(filho_dir)
        self.node_type = 'ARITHOP'
        self.data_type = None
        self.op = op
        self.esq = filho_esq
        self.dir = filho_dir
            
class Assign_node(AstNode):
    def __init__(self,  filho_esq, filho_dir):
        super().__init__()
        self.children.append(filho_esq)
        self.children.append(filho_dir)
        self.node_type = 'ASSIGN'
        self.data_type = None
        self.op = '='
        self.esq = filho_esq
        self.dir = filho_dir
        
        
class If_node(AstNode):
    def __init__(self,  condicao, parte_verdadeira, parte_falsa:None):
        super().__init__()
        self.children.append(condicao)
        self.children.append(parte_verdadeira)
        self.children.append(parte_falsa)
        self.node_type = 'IF'
        self.data_type = None
        self.op = None
        self.condicao = condicao
        self.parte_verdadeira = parte_verdadeira
        self.parte_falsa = parte_falsa

class While_node(AstNode):
    def __init__(self,  condicao, comando):
        super().__init__()
        self.children.append(condicao)
        self.children.append(comando)
        self.node_type = 'WHILE'
        self.data_type = None
        self.op = None
        self.condicao = condicao
        self.comando = comando
        
class Print_node(AstNode):
    def __init__(self, argumento, quebra_linha:False):
        super().__init__()
        self.children.append(argumento)
        self.node_type = 'PRINT'
        self.data_type = None
        self.op = None
        self.argumento = argumento
        self.quebra_linha = quebra_linha
        
class Return_node(AstNode):
    def __init__(self, expressao):
        super().__init__()
        self.children.append(expressao)
        self.node_type = 'RETURN'
        self.data_type = None
        self.op = None
        self.expressao = expressao
        
class AssignNode(AstNode):
    def __init__(self, node_type, children, data_type, op):
        super().__init__(node_type, children, data_type, op)
        
        
class Call_node(AstNode):
    def __init__(self,argumentos:list):
        super().__init__()
        self.children = argumentos[::]
        self.node_type = 'CALL'
        self.argumentos = argumentos[::]

        
class Id_node(AstNode):
    def __init__(self):
        super().__init__()
        self.node_type = 'ID'
        

class Int_const_node(AstNode):
    def __init__(self):
        super().__init__()
        self.node_type = 'INT_CONST'
        self.data_type = 'int'
       
class Float_const_node(AstNode):
    def __init__(self):
        super().__init__()
        self.node_type = 'FLOAT_CONST'
        self.data_type = 'float'
        
class Char_const_node(AstNode):
    def __init__(self):
        super().__init__()
        self.node_type = 'CHAR_CONST'
        self.data_type = 'char'