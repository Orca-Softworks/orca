package main

const (
	START          = "["
	END            = "]"
	TEMPLATE_START = "{"
	TEMPLATE_END   = "}"
	SEPARATOR      = "-"

	DECLARATION = "DECLARATION"
	FUNCTION    = "FUNCTION"
	MACRO       = "MACRO"
	ARGUMENT    = "ARGUMENT"

	INTEGER      = "INTEGER"
	FLOAT        = "FLOAT"
	STRING_QUOTE = "'"

	ILLEGAL = "ILLEGAL"
	EOF     = "EOF"
)

type TokenType string

type Token struct {
	Type    TokenType
	Literal string
	Line    uint16
	Column  uint16
}

type Lexer struct {
	input        string
	position     int
	readPosition int
	ch           byte
}

func New(input string) *Lexer {
	l := &Lexer{input: input}
	l.readChar()
	return l
}

func (l *Lexer) readChar() {
	if l.readPosition > len(l.input) {
		l.ch = 0
	} else {
		l.ch = l.input[l.readPosition]
	}
	l.position = l.readPosition
	l.readPosition += 1
}

func main() {
	lexer := New("hi!")
	print(lexer.input)
}
