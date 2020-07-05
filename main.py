from cdprojlexer import Consts
import sys

# Tokenizer... This function converts the program string to token string
def tokenizer(program_string):
    tokens = Consts.tokens
    zero_count=0
    ip = 0
    program_string += '$'
    token_string = ""
    if program_string[49]== '0' :
            zero_count+=1
    while program_string[ip] != '$':
        current_token = ""
        if program_string[ip].isalpha() or program_string[ip] == '_':
            current_token += program_string[ip]
            ip += 1
            while program_string[ip].isalnum() or program_string[ip] == '_':
                current_token += program_string[ip]
                ip += 1
            if current_token in tokens.keys():
                token_string += tokens[current_token]
            else:
                token_string += tokens['var']
        elif program_string[ip].isnumeric():
            current_token += program_string[ip]
            ip += 1
            while program_string[ip].isnumeric() or program_string[ip] == '.':
                current_token += program_string[ip]
                ip += 1 
            token_string += tokens['num']
        else:
            if program_string[ip] in tokens:
                token_string += tokens[program_string[ip]]
                ip += 1
            else:
                nl_count = 1
                pointer_count = 0
                for _ in range(ip):
                    if program_string[_] == '\n':
                        nl_count += 1
                        pointer_count = 0
                    else:
                        pointer_count += 1
                print("Tokenizer: Error on line " + str(nl_count) + " on column " + str(pointer_count))

                exit()
    return token_string,zero_count



# Syntax Analyser... This function analyses the correctness of the program in terms of the syntax
def syntax_analyser(token_string, new_line,zero_count):
    # The rules
    rules = Consts.rules

    # Parse Table
    parse_table = Consts.parse_table

    token_string += "$"

    # Stack that is used for parsing

    stack = ['$', '0']

    # Parsing happens here

    ip = 0
    while True:
        pivot = parse_table[stack[-1]][token_string[ip]]

        if pivot[0] == 'S':
            stack.append(token_string[ip])
            ip += 1
            stack.append(pivot[1:])
            continue
        elif pivot[0] == 'R':
            rule = rules[int(pivot[1:])]
            for _ in range(2*len(rule[1])):
                stack.pop()
            stack.append(rule[0])
            new_pivot = parse_table[stack[-2]][stack[-1]]
            if new_pivot != 'E':
                stack.append(new_pivot)
                continue
            else:
                break
        elif pivot[0] == 'A' and zero_count == 0:
            print("Parsing Completed Successfully... No errors...")
            sys.exit()
        else:
            break
    line_count = 1
    for _ in range(ip):
        if token_string[_] == new_line:
            line_count += 1
        if zero_count > 0 :
            print ("Line 6 : Divide by zero error")
            sys.exit()
    print("Parser: Error in line " + str(line_count))


def print_key(val): 
    for key, value in Consts.tokens.items():
         if val == 's':
              continue
         elif val == 'n':
             continue
         elif val == value: 
             return key 
         
# Main function
def main():
    filename = "F:\\6th sem notes\\CD\\CLR-Parser-master\\change.txt"
    file = open(filename, "r")
    program_string = file.read()
    print("\nProgram\n")
    print(program_string)
    print("\nTokens\n")
    
    # Tokenizing
    token_string,zero_count = tokenizer(program_string)
    print("-------------",zero_count)
    for k in token_string:
       x=print_key(k)
       if(x!= None):
        print(x,"is a token") 
    print("\n")
    
    # Parsing
    syntax_analyser(token_string, Consts.tokens['\n'],zero_count)


main()


