# Rufo_HID_Flood

Projeto em Python para simular teclado HID e enviar combinacoes de teclas via USB para outro computador.

## Estrutura

- `main.py`: ponto de entrada.
- `HidLoader.py`: carrega e valida combinacoes de teclado de um JSON.
- `KeyboardHidSender.py`: monta e envia relatorios HID de teclado (8 bytes).
- `data/keyboard_combinations.json`: lista de combinacoes prontas.

## Ambiente local

Foi criado um ambiente virtual em `localenv` e um arquivo `requirement.txt`.

Ative o ambiente:

```bash
source localenv/bin/activate
```

## Executar em modo simulacao (sem enviar na USB)

```bash
python main.py CTRL_ALT_DELETE --dry-run
```

## Executar enviando para USB HID Gadget

Por padrao o dispositivo eh `/dev/hidg0`:

```bash
python main.py CTRL_ALT_DELETE --device /dev/hidg0
```

## Exemplo de combinacao

`CTRL_ALT_DELETE` esta definida em `data/keyboard_combinations.json` como:

- modificadores: CTRL + ALT
- tecla: DELETE

## Todas as teclas e combinacoes

O arquivo `data/keyboard_combinations.json` agora eh gerado com combinacoes para todas as teclas disponiveis em `KeyboardHidSender.py`, incluindo exemplos como:

- F1
- ALT_TAB
- ALTGR_Q
- SHIFT_F1
- CTRL_ALT_DELETE

Padrao de nome:

- sem modificador: `TECLA` (ex.: `F1`)
- com modificadores: `MOD1_MOD2_TECLA` (ex.: `ALT_TAB`, `CTRL_SHIFT_ESC`)
- repeticao no JSON: `..._X2`, `..._X3`, `..._X4`, `..._X5`, `..._X10`, `..._X20`, `..._X50`, `..._X100`

Exemplos de repeticao:

```bash
python main.py SHIFT_X5 --dry-run
python main.py ALT_TAB_X5 --dry-run
python main.py SHIFT_X10 --dry-run
python main.py ALT_TAB_X20 --dry-run
python main.py SHIFT_X50 --dry-run --allow-high-repeat
python main.py ALT_TAB_X100 --dry-run --allow-high-repeat
```

Tambem eh possivel forcar repeticao por linha de comando:

```bash
python main.py SHIFT --repeat 5 --dry-run
```

Protecao contra envio acidental muito longo:

- limite padrao: 20 repeticoes
- para ultrapassar o limite, use `--allow-high-repeat`
- para desativar limite, use `--safe-max-repeat -1`

Para regenerar o JSON:

```bash
python tools/generate_keyboard_combinations.py
```

## Observacoes

- O host Linux precisa estar configurado como USB HID gadget para existir `/dev/hidg0`.
- Use somente em ambientes autorizados.
