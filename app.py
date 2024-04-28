import pandas as pd
from datetime import datetime


# Caminho do arquivo
file_path = "./data/P01_12ARE-GBD 08.txt"


split_lines = []


# Abrir o arquivo e ler linha por linha
with open(file_path, "r") as file:
    for index, line in enumerate(file):
        # Remover espaços em branco, quebras de linha e dividir em substrings
        substrings = line.strip().split(",")

        # Verificar se é a primeira linha
        if index == 0:
            # Adicionar as substrings à lista de linhas divididas
            split_lines.append(substrings)

        else:
            # Adicionar as partes das substrings a cada duas vírgulas em uma única entrada na lista
            concatenated_parts = []

            for i in range(0, len(substrings), 2):
                # Verificar se o índice é válido
                if i + 1 < len(substrings):
                    # Concatenar as duas partes separadas por vírgula e adicionar à lista
                    concatenated_parts.append(substrings[i] + "," + substrings[i + 1])

            # Adicionar as partes concatenadas à lista de linhas divididas
            split_lines.append(concatenated_parts)


# Criar DataFrame a partir da lista de linhas divididas
df = pd.DataFrame(split_lines)


# Percorrer cada coluna do DataFrame usando o nome do cabeçalho
for column in df.columns:
    print("Inicio -----------------------")

    # Acessar os valores da coluna usando o nome do cabeçalho
    values = df[column]

    # Contagem de pontos de inflação
    inflation_point = 0

    # Verificar se está descendo
    going_down = True

    # Armazenar o último valor percorrido da linha
    previous_point = None

    for index, value in values.items():

        # Verificar se o index é maior que 0 e o valor é uma string
        if index > 0 and isinstance(value, str):
            # Dividir o valor por vírgula e armazenar em uma variável
            splitted_value = value.split(",")

            # Armazenar os valores de Tempo e Pontuação da Linha em variáveis separadas
            time = float(splitted_value[0])
            line_score = float(splitted_value[1])

            # Verificar se o tempo é maior que 1
            if time > 1:
                # Verificar se o valor anterior é menor que o valor atual
                if (
                    previous_point is not None
                    and previous_point < line_score
                    and going_down
                ):

                    inflation_point += 1

                    going_down = False

                    # Verificar se a contagem de pontos de inflação é igual a 2
                    if inflation_point == 2:
                        print("previous_point", previous_point)
                        print("line_score", line_score)
                        print("time", time)
                        print("-----------------------")

                        df.loc[1:, column] = previous_point

                        # Limpar a coluna (exceto as linhas 0 à 3)
                        df[column].iloc[2:] = None
                        break

                else:
                    if previous_point is not None and previous_point > line_score:
                        going_down = True

                    previous_point = line_score


# Obter a data e hora atuais
data_hora_atual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Caminho do arquivo Excel de saída
excel_file_path = f"./data/{data_hora_atual}.xlsx"

# Salvar o DataFrame em um arquivo Excel
df.to_excel(excel_file_path, index=False)
