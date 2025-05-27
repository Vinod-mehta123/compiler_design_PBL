def generate_target(opt_code):
    target = []
    reg_counter = 1  # Start register naming from R1

    for line in opt_code:
        if isinstance(line, str):
            line = line.strip()
            if line.startswith("int"):
                # Skip declarations like "int a;"
                continue
            line = line.replace(";", "")
            parts = line.split()

        elif isinstance(line, tuple):
            parts = list(line)
        else:
            continue

        if len(parts) == 3 and parts[1] == '=':
            # Simple assignment: a = 5 or b = t0
            dest, _, src = parts
            target.append(f"MOV R{reg_counter}, {src}")
            target.append(f"MOV {dest}, R{reg_counter}")

        elif len(parts) == 5 and parts[1] == '=':
            # Expression: t1 = a + b
            dest, _, op1, operator, op2 = parts
            target.append(f"MOV R{reg_counter}, {op1}")
            asm_op = {
                '+': 'ADD',
                '-': 'SUB',
                '*': 'MUL',
                '/': 'DIV'
            }.get(operator, '???')
            target.append(f"{asm_op} R{reg_counter}, {op2}")
            target.append(f"MOV {dest}, R{reg_counter}")

        else:
            # Unrecognized format
            target.append(f"# Cannot translate: {' '.join(parts)}")

    return target
