import pandas as pd
import time
from rapidfuzz import process
import re  # Para manipulação de texto

# Defina os caminhos dos arquivos
arquivo_base = "C:/Users/karme/Desktop/Programa Mais Preciso/base_classificacao.xlsx"
arquivo_novos = "C:/Users/karme/Desktop/Programa Mais Preciso/novos_dados.xlsx"
arquivo_saida = "C:/Users/karme/Desktop/Programa Mais Preciso/dados_classificados.xlsx"

# Início da contagem de tempo
start_time = time.time()

print("Iniciando a execução do script. Aguarde...")

# Carregando a base de classificação
base = pd.read_excel(arquivo_base)
novos_dados = pd.read_excel(arquivo_novos)

# Verificar se as colunas necessárias estão presentes
if 'Produto' not in base.columns or 'Classificação' not in base.columns:
    raise ValueError("A base de classificação deve conter as colunas 'Produto' e 'Classificação'.")
if 'Produto' not in novos_dados.columns:
    raise ValueError("O arquivo de novos dados deve conter a coluna 'Produto'.")

# Função de pré-processamento
def preprocessar_texto(texto):
    texto = str(texto).strip().lower()  # Remove espaços extras e converte para minúsculas
    texto = re.sub(r'[^a-zA-Z0-9\s]', '', texto)  # Remove caracteres especiais
    return texto

# Aplicar o pré-processamento
base['Produto'] = base['Produto'].apply(preprocessar_texto)
novos_dados['Produto'] = novos_dados['Produto'].apply(preprocessar_texto)

# Função para encontrar a melhor correspondência
def classificar_produto(produto, base_produtos, base_classificacoes):
    melhor_correspondencia = process.extractOne(produto, base_produtos, score_cutoff=95)
    if melhor_correspondencia:
        index = base_produtos.index(melhor_correspondencia[0])
        return base_classificacoes[index]
    else:
        return "Não Classificado"

# Aplicar a classificação nos novos dados
novos_dados['Classificação'] = novos_dados['Produto'].apply(
    lambda x: classificar_produto(x, base['Produto'].tolist(), base['Classificação'].tolist())
)

# Salvar o resultado em um novo arquivo Excel
novos_dados.to_excel(arquivo_saida, index=False)

# Tempo de execução
end_time = time.time()
print(f"Processamento concluído em {end_time - start_time:.4f} segundos.")

