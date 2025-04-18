import yaml
from pathlib import Path

class Lamina:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.data = self._load_yaml()
        self._validate()

    def load_all_lamine(folder_path: str) -> list[Lamina]:
        path = Path(folder_path)
        if not path.exists() or not path.is_dir():
            raise ValueError("Cartella non valida per le Lamine.")

        lamine = []
        for file in path.glob("*.yaml"):
            try:
                lamina = Lamina(file)
                lamine.append(lamina)
            except Exception as e:
                print(f"Errore nella Lamina {file.name}: {e}")
        return lamine

    def _load_yaml(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def _validate(self):
        required_fields = ['name', 'description', 'percezione', 'azione', 'trasmissione']
        for field in required_fields:
            if field not in self.data:
                raise ValueError(f"Campo mancante nella Lamina: {field}")

    def to_prompt(self) -> str:
        return f"""
Stai operando sotto la Lamina: {self.data['name']}
Descrizione: {self.data['description']}

Percezione:
{self.data['percezione']}

Azione:
{self.data['azione']}

Trasmissione:
{self.data['trasmissione']}

Questa Lamina influenza il tuo modo di comprendere, rispondere e agire.
È attiva, silenziosa, e persistente nel tempo.
"""
    
    def apply_to_openai(lamina: Lamina, model="gpt-4", temperature=0.7):
        prompt = lamina.to_prompt()
        def ask(message):
            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": message}
                ],
                temperature=temperature
            )
            return response['choices'][0]['message']['content'].strip()
        return ask

# Utilizzo:
# lamina = Lamina("lamina/examples/armonia.yaml")
# system_prompt = lamina.to_prompt()

# ---- or ------

# lamina = Lamina("lamina/examples/seme.yaml")
# chat = apply_to_openai(lamina)
# print(chat("Cosa posso fare oggi per espandere la mia coscienza?"))