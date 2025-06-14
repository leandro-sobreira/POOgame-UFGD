import os
from PIL import Image

def get_new_card_name(old_filename_jpg):
    """
    Determina o novo nome base para o arquivo de carta UNO, sem extensão.
    Exemplos de transformação:
    "Blue_1.jpg" -> "blue_1"
    "Red_Skip.jpg" -> "red_block"
    "Wild_Draw_4.jpg" -> "+4"
    "Wild.jpg" -> "wild"
    "Yellow_Draw_2.jpg" -> "yellow_+2"
    """
    # Remove a extensão .jpg e converte para minúsculas
    name = os.path.splitext(old_filename_jpg)[0].lower()

    # Casos especiais (mais específicos devem vir primeiro)
    if name == "wild_draw_4":
        return "+4"
    if name == "wild":
        return "wild"

    # Substituições gerais para partes do nome
    # A ordem pode ser importante se houver sobreposição de padrões
    name = name.replace("_skip", "_block")
    name = name.replace("_draw_2", "_+2")
    # Nomes como "color_reverse" (ex: "blue_reverse") ou "color_number" (ex: "green_0")
    # já estarão no formato correto após a conversão para minúsculas e as substituições acima.

    return name

def rename_and_convert_uno_cards(directory_path):
    """
    Renomeia arquivos de cartas UNO JPG para um novo padrão e os converte para PNG.
    Os arquivos JPG originais não são excluídos.
    """
    if not os.path.isdir(directory_path):
        print(f"Erro: O diretório '{directory_path}' não foi encontrado.")
        return

    print(f"Iniciando processamento de arquivos em: {directory_path}")
    processed_count = 0
    error_count = 0

    for filename_jpg in os.listdir(directory_path):
        if not filename_jpg.lower().endswith(".jpg"):
            continue

        old_file_path_jpg = os.path.join(directory_path, filename_jpg)
        new_base_name_png = get_new_card_name(filename_jpg)
        new_file_path_png = os.path.join(directory_path, f"{new_base_name_png}.png")

        try:
            with Image.open(old_file_path_jpg) as img:
                img.save(new_file_path_png, "PNG")
            print(f"Convertido e renomeado: '{filename_jpg}' -> '{new_base_name_png}.png'")
            processed_count += 1
        except Exception as e:
            print(f"Erro ao processar '{filename_jpg}': {e}")
            error_count += 1
    
    print(f"\nProcessamento concluído. {processed_count} arquivos processados com sucesso, {error_count} erros.")

if __name__ == "__main__":
    # Caminho para o diretório das cartas.
    # Assumindo que o script 'renamecards.py' é executado da raiz do projeto,
    # onde 'src' é um subdiretório.
    cards_dir = "src/img/games/uno/cards"
    rename_and_convert_uno_cards(cards_dir)
