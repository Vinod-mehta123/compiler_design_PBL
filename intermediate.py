temp_counter = 0

def new_temp():
    global temp_counter
    temp = f't{temp_counter}'
    temp_counter += 1
    return temp

def generate_code(ast_list):
    code = []

    def walk(node):
        if node[0] == 'assign':
            rhs = walk(node[2])
            code.append(f"{node[1]} = {rhs}")
        elif node[0] in ('+', '-', '*', '/'):
            left = walk(node[1])
            right = walk(node[2])
            temp = new_temp()
            code.append(f"{temp} = {left} {node[0]} {right}")
            return temp
        elif node[0] == 'num':
            return str(node[1])
        elif node[0] == 'id':
            return node[1]
        elif node[0] == 'declare':
            code.append(f"int {node[1]};")

    # Process each statement in the list
    for stmt in ast_list:
        walk(stmt)

    return code
