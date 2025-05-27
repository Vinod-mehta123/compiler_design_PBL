import tkinter as tk
from lexer import tokenize
from parser import parse
from semantic import semantic_check
from intermediate import generate_code
from optimizer import optimize
from codegen import generate_target
from utils import build_tree

from PIL import Image, ImageTk
import os

def update_output(text_widget, lines):
    text_widget.delete(1.0, tk.END)
    for line in lines:
        text_widget.insert(tk.END, str(line) + "\n")

def visualize():
    code = input_text.get("1.0", tk.END)

    tokens = tokenize(code)
    update_output(output_lexer, tokens)

    ast = parse(code)
    if ast is None:
        update_output(output_semantic, ["Syntax Error in input."])
        return  # ❗Stop further processing if AST couldn't be built

    tree = build_tree(ast)
    tree.render("ast", format="png", cleanup=True)
    image = Image.open("ast.png")
    image = image.resize((300, 300))
    img = ImageTk.PhotoImage(image)
    image_label.config(image=img)
    image_label.image = img

    sem_errors = semantic_check(ast)
    update_output(output_semantic, sem_errors if sem_errors else ["No semantic errors."])

    ic = generate_code(ast)
    update_output(output_intermediate, ic)

    opt = optimize(ic)
    update_output(output_optimized, opt)

    target = generate_target(opt)
    update_output(output_target, target)


root = tk.Tk()
root.title("Compiler Phase Visualizer")

input_text = tk.Text(root, height=5)
input_text.pack()

tk.Button(root, text="Run Compiler", command=visualize).pack()

output_lexer = tk.Text(root, height=5, bg="lightyellow")
output_lexer.pack()
tk.Label(root, text="Lexical Tokens").pack()

output_semantic = tk.Text(root, height=3, bg="lightblue")
output_semantic.pack()
tk.Label(root, text="Semantic Analysis").pack()

output_intermediate = tk.Text(root, height=5, bg="lightgreen")
output_intermediate.pack()
tk.Label(root, text="Intermediate Code").pack()

output_optimized = tk.Text(root, height=5, bg="lightgrey")
output_optimized.pack()
tk.Label(root, text="Optimized Code").pack()

output_target = tk.Text(root, height=5, bg="lightpink")
output_target.pack()
tk.Label(root, text="Target Code").pack()

image_label = tk.Label(root)
image_label.pack()
tk.Label(root, text="Parse Tree").pack()

root.mainloop()
