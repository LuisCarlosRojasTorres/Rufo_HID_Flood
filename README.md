# Rufo_HID_Flood

Projeto em Python para simular teclado HID e enviar combinacoes de teclas via USB para outro computador.

## Estrutura

- `main.py`: ponto de entrada.
- `HidLoader.py`: carrega e valida combinacoes de teclado de um JSON.
- `KeyboardHidSender.py`: monta e envia relatorios HID de teclado (8 bytes).
- `data/keyboard_combinations.json`: lista de combinacoes prontas.
- `mouse_main.py`: ponto de entrada para mouse HID.
- `MouseLoader.py`: carrega e valida acoes de mouse de um JSON.
- `MouseHidSender.py`: monta e envia relatorios HID de mouse (4 bytes).
- `data/mouse_combinations.json`: lista de acoes de mouse prontas.

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

Escolher por menu interativo entre teclado e mouse (envio em lote):

```bash
python main.py --menu --dry-run --between-ms 5
```

Enviar todas as combinacoes em sequencia (simulacao):

```bash
python main.py --all --dry-run --between-ms 5
```

Enviar todas do teclado ou todas do mouse sem menu:

```bash
python main.py --all --target keyboard --dry-run --between-ms 5
python main.py --all --target mouse --dry-run --between-ms 5
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
- com `--all`, entradas acima do limite sao puladas (skipped) quando `--allow-high-repeat` nao eh usado

Envio em lote:

- use `--all` para enviar todas as entradas do JSON em sequencia
- use `--between-ms` para pausar entre combinacoes
- o sistema mostra tempo por item e tempo total do lote (`total_time`)

Tempo no envio individual:

- no envio de um unico item, a saida inclui `[TIMER] NOME: XX.XX ms`

Para regenerar o JSON:

```bash
python tools/generate_keyboard_combinations.py
```

## Mouse HID

Executar uma acao de mouse em simulacao:

```bash
python mouse_main.py LEFT_CLICK --dry-run
```

Executar todas as acoes de mouse em sequencia:

```bash
python mouse_main.py --all --dry-run --between-ms 5
```

Exemplos de acoes de mouse:

- `LEFT_CLICK`
- `RIGHT_CLICK`
- `MIDDLE_CLICK`
- `MOVE_UP_10`
- `MOVE_RIGHT_50`
- `SCROLL_UP_3`

Exemplos com repeticao:

```bash
python mouse_main.py LEFT_CLICK_X5 --dry-run
python mouse_main.py SCROLL_UP_3_X10 --dry-run
python mouse_main.py LEFT_CLICK_X50 --dry-run --allow-high-repeat
python mouse_main.py LEFT_CLICK --repeat 100 --dry-run --allow-high-repeat
```

Padrao de repeticao no JSON de mouse:

- `..._X2`, `..._X3`, `..._X4`, `..._X5`, `..._X10`, `..._X20`, `..._X50`, `..._X100`

Regra de seguranca no envio em lote de mouse:

- com `--all`, acoes acima do limite sao puladas (skipped) quando `--allow-high-repeat` nao eh usado
- o lote de mouse tambem exibe tempo por item e tempo total (`total_time`)

Regenerar o JSON de mouse:

```bash
python tools/generate_mouse_combinations.py
```

## Observacoes

- O host Linux precisa estar configurado como USB HID gadget para existir `/dev/hidg0`.
- Use somente em ambientes autorizados.
