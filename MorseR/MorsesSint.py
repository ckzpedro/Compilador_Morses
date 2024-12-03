from MorsesLex import lexer

class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.output = open("sintatico_output.txt", "w")

    #PRINTA A MENSAGEM NO CONSOLE (apenas para melhor visualização)
    def log(self, message):
        self.output.write(message + "\n")
        print(message)

    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def match(self, token_type):
        current = self.current_token()
        if current and current[0] == token_type:
            self.pos += 1
            return True
        return False

    def check_optional_semicolon(self):
        next_token_type = self.current_token()[0] if self.current_token() else None
        if next_token_type not in {'ESQCOLCHETE', 'ESQPAREM', 'ESQCHAVE'}:
            if self.match('PVIRG'):
                self.log("Ponto e virgula opcional detectado e consumido")

    #VERIFICA OS TOKENS DE INICIO E FINAL DO PROGRAMA
    def parse_program(self):
        if not self.match('START'):
            raise SyntaxError("Esperado token START no inicio do programa")
        
        self.log("Programa iniciado com token START \n")

        while self.current_token() is not None and self.current_token()[0] != 'END':
            self.parse_statement()

        if self.current_token() is None or not self.match('END'):
            raise SyntaxError("Esperado token END no final do programa")

        self.log("Programa finalizado com token END")

    def parse_variable(self):
        token_type = self.current_token()[0]
        if token_type in {'INT', 'FLOAT', 'DOUBLE', 'CHAR', 'BOOLEAN'}:
            self.match(token_type)
            self.log(f"Declaração de variável do tipo {token_type} ")

            if not self.match('ID'):
                raise SyntaxError(f"Esperado um identificador após o tipo {token_type}")

            if self.match('ATRIBUICAO'):
                self.log("Atribuição detectada após a declaração da variável")
                self.parse_expression() 
        else:
            raise SyntaxError("Esperado um tipo de variável (INT, FLOAT, etc.)")

    #ONDE OCORRE A LEITURA DOS TOKENS E CHAMAMENTO DOS RESPECTIVOS AUTOMATOS
    def parse_statement(self):
        token_type = self.current_token()[0]
        if token_type == 'IF':
            self.parse_if()
        elif token_type == 'FOR':
            self.parse_for()
        elif token_type == 'PRINT':
            self.parse_print()
        elif token_type == 'FUNCAO':
            self.parse_function()
        elif token_type == 'BOOLEAN':
            self.parse_boolean()
        elif token_type == 'CHAR':
            self.parse_char()
        elif token_type == 'DOUBLE':
            self.parse_double()
        elif token_type == 'INT':
            self.parse_int()
        elif token_type == 'FLOAT':
            self.parse_float()
        elif token_type == 'WHILE':
            self.parse_while()
        else:
            raise SyntaxError(f"Token inesperado {token_type} na posição {self.pos}")
        
        self.check_optional_semicolon()

    #VERIFICA SE HÁ UMA ESTRUTURA DE DECLARAÇÃO DE VARIAVÉIS (int, float, bool, char e double)
    def parse_int(self):
        self.match('INT')
        self.log("Declaracao de variavel tipo INTEIRO")

        if not self.match('ID' or 'IDMORSE'):
            raise SyntaxError('Esperado um IDENTIFICADOR apos INT')

        if not self.match('ATRIBUICAO'):
            raise SyntaxError("Esperado '=' apos ID")
        self.parse_expression()
        self.log("Variavel tipo INTEIRO validada \n")

    def parse_float(self):
        self.match('FLOAT')
        self.log("Declaracao de variavel tipo FLOAT")

        if not self.match('ID' or 'IDMORSE'):
            raise SyntaxError('Esperado um IDENTIFICADOR apos FLOAT')


        if not self.match('ATRIBUICAO'):
            raise SyntaxError("Esperado '=' apos ID")
        
        self.parse_expression()
        self.log("Variavel tipo FLOAT validada \n")

    def parse_boolean(self):
        self.match('BOOLEAN')
        self.log("Declaração de variavel tipo BOOLEAN")

        if not self.match('ID' or 'IDMORSE'):
            raise SyntaxError('Esperado um IDENTIFICADOR apos BOOLEAN')

        if not self.match('ATRIBUICAO'):
            raise SyntaxError("Esperado '=' apos ID")
        
        self.parse_expression()
        self.log("Variavel tipo BOOLEAN validada\n")

    def parse_char(self):
        self.match('CHAR')
        self.log("Declaracaoo de variavel tipo CHAR")

        if not self.match('ID' or 'IDMORSE'):
            raise SyntaxError('Esperado um IDENTIFICADOR apos CHAR')

        if not self.match('ATRIBUICAO'):
            raise SyntaxError("Esperado '=' apos ID")
        
        self.parse_expression()
        self.log("Variavel tipo CHAR validada\n")

    def parse_double(self):
        self.match('DOUBLE')
        self.log("Declaração de variavel tipo DOUBLE")

        if not self.match('ID' or 'IDMORSE'):
            raise SyntaxError('Esperado um IDENTIFICADOR apos DOUBLE')

        if not self.match('ATRIBUICAO'):
            raise SyntaxError("Esperado '=' apos ID")
        
        self.parse_expression()
        self.log("Variavel tipo DOUBLE validada\n")

    #VERIFICA SE HÁ UMA ESTRUTURA IF
    def parse_if(self):
        self.match('IF')
        self.log("Inicio da estrutura IF")

        if not self.match('ESQPAREM'):
            raise SyntaxError("Esperado '(' apos IF")
        
        # Reconhece expressões mais complexas dentro do IF
        self.parse_expression()

        if not self.match('DIRPAREN'):
            raise SyntaxError("Esperado ')' ao fechamento da condição IF")

        self.log("Condicional IF validado\n")
        self.parse_block()

        if self.match('ELSE'):
            self.log("Estrutura ELSE detectada e validada")
            self.parse_block()
            self.log("Condicional ELSE validada\n")
    
    #VERIFICA SE HÁ UMA ESTRUTURA FOR
    def parse_for(self):
        self.match('FOR')
        self.log("Inicio da estrutura FOR")

        if not self.match('ESQPAREM'):
            raise SyntaxError("Esperado '(' apos FOR")
        
        # 1. Inicialização (declaração de variável ou expressão de atribuição)
        if self.current_token()[0] in {'INT', 'FLOAT', 'DOUBLE', 'CHAR', 'BOOLEAN'}:
            self.parse_variable()  # Declaração de variável
        else:
            self.parse_expression()  # Expressão de inicialização sem declaração
        
        if not self.match('PVIRG'):
            raise SyntaxError("Esperado ';' apos inicialização do FOR")
        
        # 2. Condição
        self.parse_expression()
        
        if not self.match('PVIRG'):
            raise SyntaxError("Esperado ';' apos condição do FOR")
        
        # 3. Incremento
        self.parse_expression()
        
        if not self.match('DIRPAREN'):
            raise SyntaxError("Esperado ')' apos incremento do FOR")
        
        self.log("Estrutura FOR validada\n")
        self.parse_block()

    #VERIFICA SE HÁ UMA ESTRUTURA WHILE
    def parse_while(self):
        self.match('WHILE')
        self.log("Inicio da estrutura WHILE")

        if not self.match('ESQPAREM'):
            raise SyntaxError("Esperado '(' apos WHILE")
        
        self.parse_expression()

        if not self.match('DIRPAREN'):
            raise SyntaxError("Esperado ')' ao fechamento da condição WHILE")

        self.parse_block()
        self.log("Condicional WHILE validado\n")

    #VERIFICA SE HÁ UMA ESTRUTURA PRINT
    def parse_print(self):
        self.match('PRINT')
        self.log("Inicio da estrutura PRINT")

        if not self.match('ESQPAREM'):
            raise SyntaxError("Esperado '(' apos PRINT")

        self.parse_expression()

        if not self.match('DIRPAREN'):
            raise SyntaxError("Esperado ')' ao fechamento do print")

        self.log("Estrutura PRINT validada\n")

    #VERIFICA SE HÁ UMA ESTRUTURA DE FUNÇÃO  
    def parse_function(self):
        self.match('FUNCAO')
        self.log("Declaracaoo de funcao detectada")

        if not self.match('ESQPAREM'):
            raise SyntaxError("Esperado '(' apos FUNCAO")

        while not self.match('DIRPAREN'):
            if not self.match('ID'):
                raise SyntaxError("Esperado nome de parametro")
            if self.current_token()[0] != 'DIRPAREN' and not self.match('VIRG'):
                raise SyntaxError("Esperado ',' entre parametros")

        self.log("Declaração de funcao validada\n")
        self.parse_block()

    #ANALISA O BLOCO DE CODIGO QUE SE ENCONTRA ENTRE { } 
    def parse_block(self):
        if not self.match('ESQCHAVE'):
            raise SyntaxError("Esperado '{' ao inicio do bloco de codigo")
        
        self.log("Inicio do bloco de codigo")

        while not self.match('DIRCHAVE'):
            self.parse_statement()

        self.log("Fim do bloco de codigo\n")

    #CONSOME TOKENS QUE DIZEM RESPEITO A EXPRESSÕES MAIS SIMPLES 
    def parse_expression(self):
        token_type = self.current_token()[0]
        if token_type in ('NUMERO', 'ID', 'TRUE', 'FALSE', 'NULL', 'STRING'):
            self.log(f"Expressão valida detectada: {self.current_token()[1]}")
            self.pos += 1
        else:
            raise SyntaxError("Esperado uma expressão")
        
        while self.current_token() and self.current_token()[0] in {'MAIS', 'MENOS', 'MAIOR', 'MENOR', 'AND', 'OR', 'INCR', 'DECR', 'ATRIBUICAO'}:
            operator = self.current_token()[0]
            self.pos += 1 
            self.log(f"Operador '{operator}' detectado")

            if operator in {'INCR', 'DECR'}:
                break
            
            if self.current_token()[0] not in ('NUMERO', 'ID', 'TRUE', 'FALSE', 'NULL', 'BREAK'):
                raise SyntaxError("Esperado uma expressao apos o operador")

            self.log(f"Expressão valida detectada: {self.current_token()[1]}")
            self.pos += 1  

    def close(self):
        self.output.close()

def parse_code(text):
    tokens = lexer(text)
    tokens = [(t, l, ln, col) for t, l, ln, col in tokens if t != 'BRANCO']
    
    parser = Parser(tokens)
    try:
        parser.parse_program()
        print("Codigo validado com sucesso.")
    except SyntaxError as e:
        parser.log(f"Erro de sintaxe: {e}")
    finally:
        parser.close()