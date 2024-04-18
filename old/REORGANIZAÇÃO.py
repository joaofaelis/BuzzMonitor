import os

# Diretório base
diretorio_base = r"C:\Users\João Faelis\Desktop\BuzzMonitor\database_original"

# Listando todos os arquivos no diretório
arquivos = os.listdir(diretorio_base)

# Iterando sobre a lista de arquivos
for nome_arquivo in arquivos:
    # Construindo o caminho completo para cada arquivo
    caminho_completo = os.path.join(diretorio_base, nome_arquivo)

    # Imprimindo o caminho completo de cada arquivo
    print("Caminho completo:", caminho_completo)