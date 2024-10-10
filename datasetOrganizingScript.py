import os
import shutil

handsign_names = {
    1: "Opaco",
    2: "Rojo",
    3: "Verde",
    4: "Amarillo",
    5: "Brillante",
    6: "Celeste",
    7: "Colores",
    8: "Rosa",
    9: "Mujeres",
    10: "Enemigo",
    11: "Hijo",
    12: "Hombre",
    13: "Lejos",
    14: "Cajón",
    15: "Nacer",
    16: "Aprender",
    17: "Llamar",
    18: "Espumadera",
    19: "Amargo",
    20: "Leche condensada",
    21: "Leche",
    22: "Agua",
    23: "Comida",
    24: "Argentina",
    25: "Uruguay",
    26: "País",
    27: "Apellido",
    28: "Dónde",
    29: "Burlarse",
    30: "Cumpleaños",
    31: "Desayuno",
    32: "Foto",
    33: "Hambre",
    34: "Mapa",
    35: "Moneda",
    36: "Música",
    37: "Barco",
    38: "Ninguno",
    39: "Nombre",
    40: "Paciencia",
    41: "Perfume",
    42: "Sordo",
    43: "Trampa",
    44: "Arroz",
    45: "Asado",
    46: "Caramelo",
    47: "Chicle",
    48: "Fideos",
    49: "Yogur",
    50: "Aceptar",
    51: "Gracias",
    52: "Apagar",
    53: "Aparecer",
    54: "Aterrizar",
    55: "Atrapar",
    56: "Ayuda",
    57: "Bailar",
    58: "Bañarse",
    59: "Comprar",
    60: "Copiar",
    61: "Correr",
    62: "Darse cuenta",
    63: "Dar",
    64: "Encontrar"
}


def organize_videos(input_folder):
    # Create a list of all files in the input folder
    files = os.listdir(input_folder)

    # Loop through all files in the input folder
    for file_name in files:
        # Ensure it's a video file (mp4 in this case)
        if file_name.endswith(".mp4"):
            # Extract the first three digits and subtract 1
            try:
                first_three_numbers = int(file_name[:3])
                folder_index = first_three_numbers
                
                # Get the corresponding handsign name, lowercase the folder name
                folder_name = handsign_names.get(folder_index, f"handsign_{folder_index}").lower()
                
                # Create the destination folder if it doesn't exist
                destination_folder = os.path.join(input_folder, folder_name)
                os.makedirs(destination_folder, exist_ok=True)
                
                # Move the file to the destination folder
                src_path = os.path.join(input_folder, file_name)
                dest_path = os.path.join(destination_folder, file_name)
                shutil.move(src_path, dest_path)
                print(f'Moved {file_name} to {folder_name}')
            
            except ValueError:
                print(f"Skipping {file_name}, not starting with a number.")

# Define your input folder path
input_folder = "all"

# Call the functions
organize_videos(input_folder)
