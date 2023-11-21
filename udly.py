import sys
import os
import tkinter as tk
import customtkinter as ctk
from CTkMenuBar import *
import subprocess
import threading
import re
import pyperclip


version = '- v1.1.0'

current_process = None

ascii_art_done= ascii_art = """                                                                                              


                                --------------Thanks-For-using-Udly----------------
                                                                                                                
"""



# Create a function to toggle full screen
def toggle_full_screen():
    if root.attributes("-fullscreen"):
        root.attributes("-fullscreen", False)
    else:
        root.attributes("-fullscreen", True)
        
# Create a function to run an external script and display its output
def run_external_script(course_link, selected_browser):
    global current_process
    # Check if the course link is empty
    if not course_link:
        print("Course link is empty. Please enter a valid Udemy course link.")
        return
    command = ["python", "main.py", "-c", course_link, "--browser", selected_browser, "--download-assets", "--download-captions", "--download-quizzes", "--id-as-course-name", "-n"]
    current_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, universal_newlines=True)


    # Remove the phrase "/course" from the course link if it's present
    course_link = course_link.replace('/course', '')

    def run_script():
        try:
            # Clear the old text in the output_text widget
            output_text.configure(state=tk.NORMAL)
            output_text.delete(1.0, tk.END)  # Clear all text from the widget
            output_text.configure(state=tk.DISABLED)

            # Create a new thread to read and display live output
            def read_output():
                for line in current_process.stdout:
                    # Remove escape sequences using regular expression
                    cleaned_line = re.sub(r'\x1B\[[0-?]*[ -/]*[@-~]', '', line)
                    output_text.configure(state=tk.NORMAL)
                    output_text.insert(tk.END, cleaned_line)
                    output_text.see(tk.END)  # Auto-scroll to the end
                    output_text.configure(state=tk.DISABLED)
                current_process.wait()

                # Display ASCII art when the process is finished
                output_text.configure(state=tk.NORMAL)
                output_text.insert(tk.END, ascii_art_done)
                output_text.see(tk.END)  # Auto-scroll to the end
                output_text.configure(state=tk.DISABLED)

            output_thread = threading.Thread(target=read_output)
            output_thread.start()
        except Exception as e:
            output_text.configure(state=tk.NORMAL)
            output_text.insert(tk.END, f"Error: {e}")
            output_text.configure(state=tk.DISABLED)

    # Create a new thread to run the script
    script_thread = threading.Thread(target=run_script)
    script_thread.start()

# Create a function to stop the running script
def stop_script():
    global current_process
    if current_process:
        current_process.terminate()
        current_process = None

#Comman Conditions to run
def final_cmd():
    cmd = [course_link_entry.get(), browser_var.get()]
    if check_sc.get():
        cmd.append(check_sc.get())
    if check_info.get():
        cmd.append(check_info.get())
    return " ".join(cmd)


# Restarts the Whole Window
def reload():
    root.destroy()
    os.startfile("udly.py")

# Create the main window
root = ctk.CTk()
root.title('Udly | Udemy Downloader GUI ' + version)
root.geometry('800x650')

# Top Menu
menu = CTkMenuBar(root)
button_1 = menu.add_cascade("Udly")
button_2 = menu.add_cascade("View")
button_3 = menu.add_cascade("Github Repo", command=lambda: print("Repo"))
button_4 = menu.add_cascade("Donate", command=lambda: print("Donate"))


# Create a frame to hold real-time output
output_frame = ctk.CTkFrame(root)
output_frame.pack(fill="both", expand=True)

# Create a label to provide instructions
instruction_label = ctk.CTkLabel(root, text="Enter the Udemy course link:", justify="right")
instruction_label.pack(side="top")
# Create an input field for the course link
course_link_entry = ctk.CTkEntry(root, width=400)
course_link_entry.pack(side="top")

# Create a StringVar for the selected browser and set the default browser
browser_var = ctk.StringVar(value="chrome")
#browser_var = tk.StringVar(root)
#browser_var.set("chrome")

# Create a Label for the browser selection
browser_label = ctk.CTkLabel(root, text="Choose a browser:")
browser_label.pack(side="left", padx = 5)

# Create a dropdown menu for choosing a browser
#browsers = 
browser_dropdown = ctk.CTkOptionMenu(root, values=["chrome", "firefox", "opera", "edge", "brave", "chromium", "vivaldi", "safari"],variable=browser_var)
#browser_dropdown = tk.OptionMenu(root, browser_var, *browsers)
browser_dropdown.pack(side="left")

#Create a checkbox for subscribed
check_sc = ctk.StringVar(value="")
sc_checkbox = ctk.CTkCheckBox(root, text="Subscribed?", variable=check_sc, onvalue="-sc", offvalue="", corner_radius=50)
sc_checkbox.pack(side="right", padx=10)

#Create a checkbox for info
check_info = ctk.StringVar(value="")
info_checkbox = ctk.CTkCheckBox(root, text="Want Info?", variable=check_info, onvalue="--info", offvalue="", corner_radius=50, command=lambda: print(check_info.get()))
info_checkbox.pack(side="right", padx=10)

#Create a checkbox for assets
#check_assets = ctk.StringVar(value="")
#assets_checkbox = ctk.CTkCheckBox(root, text="Want Assets?", variable=check_assets, onvalue="--download-assets", offvalue="", corner_radius=50)
#assets_checkbox.pack(side="right", padx=10)



# Create a button for "Run External Script" with the course link as an argument
run_script_button = ctk.CTkButton(root, text="Start Udlying", command=lambda: run_external_script(course_link_entry.get(), browser_var.get()), hover="true")
run_script_button.pack(side="right", pady=15)  # Adjust the placement as needed

# Create a button to stop the script
stop_button = ctk.CTkButton(root, text="Stop Udlying", command=stop_script)
stop_button.pack(side="right", pady=15, padx=3)

# Create a dropdown menu for "View"
dropdown2 = CustomDropdownMenu(widget=button_2)
dropdown2.add_option(option="Force Reload", command=lambda: reload())

# Create a dropdown menu for "Toggle Full Screen"
dropdown2.add_option(option="Toggle Full Screen", command=lambda: toggle_full_screen())

# Create a dropdown menu for "Udly"
dropdown1 = CustomDropdownMenu(widget=button_1)
dropdown1.add_option(option="Exit", command=lambda: sys.exit(0))


# Create a customtkinter text widget for displaying the output
output_text = ctk.CTkTextbox(output_frame, wrap=tk.WORD, state=tk.DISABLED)
output_text.pack(fill="both", expand=True)

# Run the application
root.mainloop()
