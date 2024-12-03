import re 

tokens = [
    #tipos
    ('INT', r'\.\. -\. -'),
    ('FLOAT', r'\.\.-\. \.-\.\. --- \.- -'),
    ('DOUBLE', r'-\.\. --- \.\.- -\.\.\. \.-\.\. \.'),
    ('CHAR', r'\.\.\. - \.-\. \.\. -\. --\.'),
    ('BOOLEAN', r'-\.\.\. --- --- \.-\.\. \. \.- -\.'),
    ('NULL', r'-\. \.\.- \.-\.\. \.-\.\.'),
    ('TRUE', r'- \.-\. \.\.- \.'),
    ('FALSE', r'\.\.-\. \.- \.-\.\. \.\.\. \.'),

    #reservadas
    ('IF', r'\.\. \.\.-\.'),
    ('ELSE', r'\. \.-\.\. \.\.\. \.'),
    ('FOR', r'\.\.-\. --- \.-\.'),
    ('WHILE', r'\.-- \.\.\.\. \.\. \.-\.\. \.'),
    ('FUNCAO', r'\.\.-\. \.\.- -\. -\.-\. - \.\. --- -\.'),
    ('RETURN', r'\.-\. \. - \.\.- \.-\. -\.'),
    ('BREAK', r'-\.\.\. \.-\. \. \.- -\.-'),
    ('PRINT', r'\.--\. \.-\. \.\. -\. -'), 

    #
    ('STRING', r'"([-.a-zA-Z0-9 ]+)"'),
    ('ID', r'[a-zA-Z_][a-zA-Z_0-9]*'),
    ('IDMORSE', r'`([-.a-zA-Z0-9 ]+)`'),
    ('NUMERO', r'\d+(\.\d*)?'),
    ('BRANCO', r'\s+'),
    ('COMENT', r'\/\/(.*?)\/\/'),

    #controle
    ('START', r'-\.-\. --- -- \. ---'),
    ('END', r'\.\.-\. \.\. --'),

    #simbolos
    ('INCR', r'\+\+'),
    ('DECR', r'--'),
    ('MAIS', r'\+'),
    ('MENOS', r'\-'),
    ('ASTERISCOS', r'\*'),
    ('BARRA', r'\/'),
    ('DIRPAREN', r'\)'),
    ('ESQPAREM', r'\('),
    ('BARRAINVERT', r'\\'),
    ('ASPASDUP', r'\"'),
    ('ASPASSIMP', r'\''),
    ('ATRIBUICAO', r'\='),
    ('MAIOR', r'\>'),
    ('MENOR', r'\<'),
    ('DIRCHAVE', r'\}'),
    ('ESQCHAVE', r'\{'),
    ('DIRCOLCHETE', r'\]'),
    ('ESQCOLCHETE', r'\['),
    ('NEGAÇÃO', r'\!'),
    ('PVIRG', r'\;'),
    ('AND', r'\&&'),
    ('ECOMERC', r'\&'),
    ('OR', r'\|\|'),
    ('MAIOR', r'\>'),
    ('MENOR', r'\<'),
]


def lexer(text):
    pos = 0
    linha = 1
    coluna = 1
    tokens_identificados = []  # Lista para armazenar os tokens identificados

    header = f"{'Token':<15} {'Lexema':<55} {'Linha':<10} {'Coluna':<10}\n"
    with open("tokens.txt", "w") as output_file:
        output_file.write(header)
        output_file.write("="*90 + "\n")
        
        # Loop que passa pelos tokens
        while pos < len(text):
            match = None
            for token_type, regex in tokens:
                regex_obj = re.compile(regex)
                match = regex_obj.match(text, pos)
                if match:
                    lexema = match.group(0)
                    token_len = len(lexema)

                    if token_type == 'BRANCO':
                        if '\n' in lexema:
                            linha += lexema.count('\n')
                            coluna = 1
                        else:
                            coluna += token_len
                        pos = match.end(0)
                        break

                    tokens_identificados.append((token_type, lexema, linha, coluna))  # Armazena o token
                    output_linha = f"{token_type:<15} {lexema:<55} {linha:<10} {coluna:<10}\n"
                    output_file.write(output_linha)

                    pos = match.end(0)
                    coluna += token_len
                    break

            if not match:
                print(f"Erro Léxico: Caractere inesperado '{text[pos]}' - Linha: {linha}, Coluna: {coluna}")
                pos += 1
                coluna += 1

    return tokens_identificados  # Retorna a lista de tokens
