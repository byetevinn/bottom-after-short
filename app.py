import os
import pandas as pd


# Caminho da pasta de entrada
input_folder = "./data"

# Caminho da pasta de saída
output_folder = "./output"

# Lista de nomes de arquivos na pasta de entrada
file_names = os.listdir(input_folder)

# Iterar sobre cada arquivo na lista
for file_name in file_names:
    # Caminho completo do arquivo de entrada
    input_file_path = os.path.join(input_folder, file_name)

    # Criar uma lista para armazenar as linhas divididas
    split_lines = []

    # Abrir o arquivo e ler linha por linha
    with open(input_file_path, "r") as file:
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
                        concatenated_parts.append(
                            substrings[i] + "," + substrings[i + 1]
                        )

                # Adicionar as partes concatenadas à lista de linhas divididas
                split_lines.append(concatenated_parts)

    # Criar DataFrame a partir da lista de linhas divididas
    df = pd.DataFrame(split_lines)

    # Iterar sobre cada coluna do DataFrame
    for column in df.columns:
        # Acessar os valores da coluna usando o nome do cabeçalho
        values = df[column]

        # Contagem de pontos de inflação
        inflation_point = 0

        # Verificar se está descendo
        going_down = True

        # Armazenar o último valor percorrido da linha
        previous_point = None

        # Menor valor encontrado na linha
        lower_value = None

        # Iterar sobre cada valor da coluna
        for index, value in values.items():
            # Verificar se o index é maior que 0 e o valor é uma string
            if index > 0 and isinstance(value, str):
                # Dividir o valor por vírgula e armazenar em uma variável
                splitted_value = value.split(",")

                # Armazenar os valores de Tempo e Pontuação da Linha em variáveis separadas
                time = float(splitted_value[0])
                line_score = float(splitted_value[1])

                # Verificar se o tempo é maior que 0.9
                if time > 0.9:
                    # Verificar se o valor anterior é menor que o valor atual
                    if (
                        previous_point is not None
                        and previous_point < line_score
                        and going_down
                    ):
                        inflation_point += 1
                        going_down = False

                        # Verificar se a contagem de pontos de inflação é igual a 1
                        if inflation_point == 1:
                            # Substituir o valor na linha 1
                            df.loc[1, column] = previous_point

                        if inflation_point > 1:

                            if lower_value is None:
                                lower_value = previous_point
                            elif previous_point < lower_value:
                                lower_value = previous_point

                            # Substituir o valor na linha 2
                            df.loc[2, column] = lower_value

                    else:
                        if previous_point is not None and previous_point > line_score:
                            going_down = True

                        previous_point = line_score

        # Limpar a coluna (exceto as linhas 1 à 3)
        df.loc[3:, column] = None

    # Caminho completo do arquivo de saída
    output_file_path = os.path.join(output_folder, f"{file_name}.xlsx")

    # Salvar o DataFrame em um arquivo Excel
    df.to_excel(output_file_path, index=False)
