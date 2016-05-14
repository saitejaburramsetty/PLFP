INTEGER, EOF, NULL = 'INTEGER', 'EOF', 'NULL'
PLUS, MINUS, TIMES, DIVIDE, EXP = 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EXP'


class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, or EOF
        self.type = type
        # token value: 0, 1, 2. 3, 4, 5, 6, 7, 8, 9, '+', or None
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Interpreter(object):
    def __init__(self, text):
        # client string input, e.g. "3+5"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        # current token instance
        self.current_token = None

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        text = self.text
        if self.pos > len(text) - 1:
            return Token(EOF, None)

        # get a character at the position self.pos and decide
        # what token to create based on the single character
        current_char = text[self.pos]
        if current_char.isdigit():
            token = Token(INTEGER, int(current_char))
            self.pos += 1
            return token

        if current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token

        if current_char == '-':
            token = Token(MINUS, current_char)
            self.pos += 1
            return token

        if current_char == '*':
            token = Token(TIMES, current_char)
            self.pos += 1
            return token

        if current_char == '/':
            token = Token(DIVIDE, current_char)
            self.pos += 1
            return token

        if current_char == '^':
            token = Token(EXP, current_char)
            self.pos += 1
            return token

        print "Could not recognize character: " + current_char
        self.error()

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            print "Eating failed"
            self.error()

    def expr(self):
        #expr -> INTEGER OPERATOR INTEGER

        # set current token to the first token taken from the input
        self.current_token = self.get_next_token()

        # get value of left side digits
        left = self.current_token
        self.eat(INTEGER)

        while self.current_token.type == "INTEGER":
            left.value *= 10
            left.value += self.current_token.value
            self.eat(INTEGER)
        op = self.current_token
        self.eat(self.current_token.type)

        right = self.current_token
        self.eat(INTEGER)

        while self.current_token.type == "INTEGER":
            right.value *= 10
            right.value += self.current_token.value
            self.eat(INTEGER)

        if op.type == "PLUS": 
            result = left.value + right.value
        elif op.type == "MINUS": 
            result = left.value - right.value
        elif op.type == "TIMES": 
            result = left.value * right.value
        elif op.type == "DIVIDE": 
            result = left.value / right.value
        elif op.type == "EXP": 
            result = left.value ** right.value

        return result


def main():
    while True:
        try:
            text = raw_input('Calc >> ')
        except EOFError:
            break
        if not text:
            continue
        elif text == "quit":
            break

        #remove all white spaces
        text = text.replace(" ", "")

        #process string
        interpreter = Interpreter(text)
        result = interpreter.expr()

        print result

if __name__ == '__main__':
    main()
