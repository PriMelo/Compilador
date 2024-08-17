from analisador_lexico import AnalisadorLexico
from analisador_sintatico import AnalisadorSintatico

an_lexico = AnalisadorLexico()
an_sintatico = AnalisadorSintatico()
arquivo = 'code1.p'
saida_an_lexico = an_lexico.analisar(arquivo)
saida_an_sintatico = an_sintatico.analisar(saida_an_lexico) 

#print(saida_an_sintatico)

"""
with open(f"{arquivo_entrada[:-3]}_sintatico.json", "w") as arquivo:     
            json.dump(saida, arquivo, indent=4)
"""
