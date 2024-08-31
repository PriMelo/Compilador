from analisador_lexico import AnalisadorLexico
from analisador_sintatico import AnalisadorSintatico
import csv


def export_tabelas(tabelas, nome_arq):
    
    with open(f'tabelas_simbolos_{nome_arq}.csv', mode='w', newline='') as arq:
        campos = ['chave','nome',
                'tipo_de_dado',
                'pos_param',
                'eh_chamada',
                'num_args',
                'args']
        
        escritor = csv.DictWriter(arq, fieldnames=campos)
        
        
        for chave, tabela in tabelas.items():
            arq.write(f'{chave}\n')
            escritor.writeheader()
            for lexema, atributos in tabela.elementos.items():
                
                linha = {'chave': atributos['chave'], 'nome': atributos['nome'],'tipo_de_dado': atributos['tipo_de_dado'],'pos_param': atributos['pos_param'], 'eh_chamada': atributos['eh_chamada'], 'num_args': atributos['num_args'], 'args': atributos['args']}
                escritor.writerow(linha)
            
        
    
    
    

an_lexico = AnalisadorLexico()
an_sintatico = AnalisadorSintatico()
arquivo = 'media.p'
saida_an_lexico = an_lexico.analisar(arquivo)
saida_an_sintatico = an_sintatico.analisar(saida_an_lexico,arquivo) 
an_sintatico.representacao_ASA(arquivo[:-2])
vec_ast = an_sintatico.vec_ast
tabelas = an_sintatico.tabelas

export_tabelas(tabelas, arquivo)

for arv in vec_ast:
    arv.verifica_tipos()

