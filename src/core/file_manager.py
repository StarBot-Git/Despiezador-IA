import os
import json

from pathlib import Path

class OpenAIFileManager:
    def __init__(self, openai_client):
        self.client = openai_client

        base_dir = Path(__file__).resolve().parents[2]

        self.id_register = base_dir / "assets" / "file_ids.json"

    """
        Upload_File():
    """
    def Upload_File(self, local_FileName: str, path: str, purpose:str = "user_data"):
        data = self.Load_Register()

        with open(path, "rb") as f:
            file_id = self.client.files.create(file=f, purpose=purpose).id

        data[local_FileName] = file_id
        self.Save_Register(data)

        print(f"[OpenAI] Registrado {local_FileName}: {file_id}")

        return file_id

    """
        Load_File():
    """
    def Load_File(self, local_FileName: str, path: str = None, purpose: str = "user_data"):
        """
        Devuelve el ID del archivo almacenado en el registro. Si no existe y se
        proporciona una ruta, lo sube a OpenAI y registra su ID.
        """
        data = self.Load_Register()
        file_id = data.get(local_FileName)

        if file_id:
            print(f"[OpenAI] Se cargó {local_FileName}: {file_id}")
            return file_id

        print(f"[OpenAI] {local_FileName} no existe en el registro.")

        if path and os.path.exists(path):
            print(f"[OpenAI] Subiendo {local_FileName} desde {path}...")
            return self.Upload_File(local_FileName, path, purpose)

        return None

    """
        Load_Register():
    """
    def Load_Register(self):
        if not os.path.exists(self.id_register):
            return {}
        
        with open(self.id_register, "r", encoding="utf-8") as file:
            return json.load(file)

    """
        Save_Register():
    """
    def Save_Register(self, data: dict):
        with open(self.id_register, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
