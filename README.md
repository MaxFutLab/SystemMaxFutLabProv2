# Android Emulator Automation (Python)

Estrutura inicial profissional para automação de jogo em múltiplas instâncias de emulador Android no Windows.

## Requisitos
- Python 3.12
- Dependências em `requirements.txt`

## Execução
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
python main.py --mode once
```

## Estrutura
- `app/automation`: orquestração e máquina de estados
- `app/emulator`: gerenciamento de instâncias
- `app/vision`: captura de tela e detecção por OpenCV
- `app/input`: ações de mouse/teclado
- `app/utils`: configuração e logging
- `config/settings.json`: configuração de exemplo
