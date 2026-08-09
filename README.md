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

## Observacoes

- O host Linux precisa estar configurado como USB HID gadget para existir `/dev/hidg0`.
- Use somente em ambientes autorizados.
