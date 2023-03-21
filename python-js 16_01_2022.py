functionDictionary = {
    "print": "print",
    "pow": "Math.pow"
}

state = "L"
filename = "./Transp_test.py" #pēdiņās ierakstiet faila ar Python kodu nosaukumu
token = ""
tab_counter = 0
bracket_counter = 0

output = open("./sample/result.js", "w+") #Šī failā varēsiet apskatīt rezultātu

# print(functionDictionary[token])

helper_functions = '''
function range(count) {
    const arr = [];
    for (let i = 0; i < count; i++) {
        arr.push(i);
    }
    return arr;
}

function print(...data) {
    document.writeln(data.join(", ") + "<br />");
}

// ---------------------

'''


def write_str(data):
    output.write(data)
    print(data, end="")


write_str(helper_functions)

with open(filename) as f:
    while True:
        c = f.read(1)

        if c == "\t":
            write_str("   ")
            tab_counter += 1

        if c == "\n":
            if tab_counter == 0:
                for i in range(bracket_counter):
                    write_str("}\n\n")
                bracket_counter = 0
            tab_counter = 0

        if state == "L":
            if c == "=":
                state = "A"
            elif c == "+" or c == "-":
                token = token + " " + c
                state = "A_MATH"
            elif c == "(":
                state = "F"
            elif c == "(":
                state = "Dic"
            elif c == "}":
                state = "Close_Bracket"
            elif token == "if":
                state = "IF"
            elif token == "while":
                state = "WHILE"
            elif token == "for":
                state = "FOR"
            elif c != "\n" and c != "\t" and c != " " and c != "{":
                token = token + c

        elif state == "Close_Bracket":
            write_str("\n}")
            c = ""
            token = ""
            state = "L"

        elif state == "A":
            write_str(token + " = ")
            if c != " " and c != "=":
                write_str(c)
            token = ""
            state = "A2"

        elif state == "A_MATH":
            if c == "=":
                write_str(token + "= ")
                token = ""
                state = "A2"

        elif state == "A2":
            if c == "\n":
                write_str(";")
                state = "L"
            write_str(c)

        elif state == "F":
            write_str(functionDictionary[token] + "(" + c)
            token = ""
            state = "A2"

        elif state == "2IF":
            if c != ":":
                write_str(c)
            else:
                tab_counter += 1
                bracket_counter += 1
                write_str(") {\n")
                token = ""
                state = "L"

        elif state == "IF":
            write_str("\nif (" + c)
            token = ""
            state = "2IF"

        elif state == "WHILE":
            write_str("\nwhile (" + c)
            token = ""
            state = "2IF"

        elif state == "FOR":
            write_str("\nfor (" + c)
            token = ""
            state = "2IF"

        elif state == "2FOR":
            tab_counter += 1
            bracket_counter += 1
            write_str(") {\n")
            token = ""
            state = "L"

        elif state == "A3":
            if c == "\n":
                write_str(";")
                state = "L"
            write_str(c)

        elif state == "Dic":
            write_str("var " + token + " = ")
            if c != " " and c != "=":
                write_str(c)
            token = ""
            state = "A2"

        if not c:
            for i in range(bracket_counter):
                write_str("}\n\n")
            write_str("\n // End of file")
            break

output.close()
