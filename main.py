from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess

compiler = Tk()
compiler.title('My PYTHON IDE')
file_path = ''
external_libraries = []
user_input = None


def set_file_path(path):
    global file_path
    file_path = path


def open_file():
    path = askopenfilename(filetypes=[('Python Files', '*.py')])
    with open(path, 'r') as file:
        code = file.read()
        editor.delete('1.0', END)
        editor.insert('1.0', code)
        set_file_path(path)


def save_as():
    if file_path == '':
        path = asksaveasfilename(filetypes=[('Python Files', '*.py')])
    else:
        path = file_path
    with open(path, 'w') as file:
        code = editor.get('1.0', END)
        file.write(code)
        set_file_path(path)


def add_library():
    lib_path = askopenfilename(filetypes=[('Python Files', '*.py')])
    if lib_path:
        external_libraries.append(lib_path)


def get_user_input():
    global user_input
    user_input = input_box.get('1.0', END)


def run():
    if file_path == '':
        save_prompt = Toplevel()
        text = Label(save_prompt, text='Please save your code')
        text.pack()
        return

    command = f'python {file_path}'
    if external_libraries:
        command += ' ' + ' '.join(external_libraries)

    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               shell=True)

    # Pass user input to the process
    if user_input:
        process.stdin.write(user_input.encode())
        process.stdin.flush()

    output, error = process.communicate()
    code_output.insert('1.0', output.decode())
    code_output.insert('1.0', error.decode())


menu_bar = Menu(compiler)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save', command=save_as)
file_menu.add_command(label='Save As', command=save_as)
file_menu.add_command(label='Exit', command=exit)
menu_bar.add_cascade(label='File', menu=file_menu)

run_menu = Menu(menu_bar, tearoff=0)
run_menu.add_command(label='Run', command=run)
menu_bar.add_cascade(label='Run', menu=run_menu)

library_menu = Menu(menu_bar, tearoff=0)
library_menu.add_command(label='Add library', command=add_library)
menu_bar.add_cascade(label='External Libraries', menu=library_menu)

compiler.config(menu=menu_bar)

editor = Text()
editor.pack()

input_box = Text(height=5)
input_box.pack()

run_button = Button(text='Run', command=lambda: [get_user_input(), run()])
run_button.pack()

code_output = Text(height=10)
code_output.pack()

compiler.mainloop()
