### Universal Save Tool by Hazeblade###
version = "ver. 1.2.7"
#Library Imports.
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askdirectory
from tkinter import simpledialog
from tkinter import messagebox
from functools import partial
from pynput.keyboard import Listener
import keyboard, shutil, winsound, json, webbrowser, os, logging, base64, tempfile, threading, time, copy
import tkinter as tk
import pygetwindow as gw
import base64
from tkinter import PhotoImage
from tkinter import ttk
from os.path import basename

#Default Configuration Dictionary
default_config = {
    "disclaimer": 1,
    "saveHotkey": "F7",
    "loadHotkey": "F9",
    "renameHotkey": "F2",
    "deleteHotkey": "DELETE",
    "sound": 1,
    "last_used_profile": "Default Profile",
    "profiles": {
        "Default Profile": {
            "inputfile": "Saves/",
            "outputfile": "Not Assigned",
            "outputfilesecondary": "Not Assigned",
            "secondarystate": "disabled",
            "dynamicsaves": 0
        }
    },
    "window_size": {
        "width": 350,
        "height": 440
    }
}

#Initialize Base64 Icon
icon_base64 = "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"
icon_data = base64.b64decode(icon_base64)

#Create Default Directories
if not os.path.exists("Saves/"):
    os.makedirs("Saves/")
if not os.path.exists("data/"):
    os.makedirs("data/")

#Initalize Error Logging
logging.basicConfig(filename='data\logs.txt', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

#Preload Functions
def write_data():
    try:         
        with open('data/config.json', 'w') as f:
            json.dump(config, f, indent=4)
            
    except PermissionError:
        logging.error("Permission denied while trying to write to config.json")
        messagebox.showerror("Permission Error", "You don't have permission to write to this directory.")
    except Exception as e:
        logging.error(f"An error occurred in write_data: {e}")
        messagebox.showerror("Error", f"An error occurred while saving config: {e}")

        
def confirm_opt(): #Toggles the Dead Space Remake Impossible Disclaimer on launch.
    if cb.get() == 1:
        config['disclaimer'] = 0
    elif cb.get() == 0:
        config['disclaimer'] = 1

    
def close_opt(): #Closes the Dead Space Remake Impossible Disclaimer.
    write_data()
    root0.destroy()


def create_profile():
    global selected_profile
    profile_name = simpledialog.askstring("Create Profile", "Enter a name for the profile (max 20 characters):")
    if profile_name is not None:
        # Truncate the input to the first 20 characters
        profile_name = profile_name[:20]

        if profile_name.strip():  # Check if the name is not blank
            if profile_name not in config['profiles']:

                new_profile = {
                    'inputfile': 'Saves/',
                    'outputfile': 'Not Assigned',
                    'outputfilesecondary': 'Not Assigned',
                    'secondarystate': 'disabled',
                    'dynamicsaves': 0
                }

                if 'profiles' not in config:
                    config['profiles'] = {}

                config['profiles'][profile_name] = new_profile
                update_profile_dropdown()
                write_data()

                selected_profile = profile_name
                profile_var.set(profile_name)
                select_profile(None)
            else:
                messagebox.showwarning("Profile Already Exists", "Profile with this name already exists.")
        else:
            messagebox.showwarning("Invalid Profile Name", "Please enter a valid profile name.")


def edit_profile():
    global selected_profile
    selected_profile = profile_var.get()
    new_profile_name = simpledialog.askstring("Edit Profile", "Enter a new name for the profile:")
    if new_profile_name is not None:
        if new_profile_name.strip():  # Check if the new name is not blank
            if new_profile_name != selected_profile and new_profile_name not in config['profiles']:
                if selected_profile in config['profiles']:
                    # Create a copy of the profile data
                    profile_data = config['profiles'][selected_profile]

                    # Remove the old profile entry
                    del config['profiles'][selected_profile]

                    # Add the profile data with the new name
                    config['profiles'][new_profile_name] = profile_data

                    # Update the profile dropdown menu
                    update_profile_dropdown()

                    # Save the changes to the JSON file
                    write_data()

                    profile_var.set(new_profile_name)
                    select_profile(None)
                else:
                    messagebox.showwarning("Profile Not Found", "Selected profile not found in configuration.")
            else:
                messagebox.showwarning("Invalid Profile Name", "Please enter a valid and unique profile name.")
        else:
            messagebox.showwarning("Invalid Profile Name", "Please enter a valid profile name.")


def duplicate_profile():
    global selected_profile
    selected_profile = profile_var.get()
    copied_profile_name = simpledialog.askstring("Edit Profile", "Enter a new name for the profile:")
    if copied_profile_name is not None:
        if copied_profile_name.strip():  # Check if the new name is not blank
            if copied_profile_name not in config['profiles']:
                if selected_profile in config['profiles']:
                    # Create a deep copy of the profile data
                    profile_data = copy.deepcopy(config['profiles'][selected_profile])

                    # Add the profile data with the new name
                    config['profiles'][copied_profile_name] = profile_data

                    # Update the profile dropdown menu
                    update_profile_dropdown()

                    # Save the changes to the JSON file
                    write_data()

                    # Set the newly created profile as the selected profile
                    selected_profile = copied_profile_name
                    profile_var.set(selected_profile)

                    # Refresh the UI for the selected profile
                    select_profile(None)
                else:
                    messagebox.showwarning("Profile Not Found", "Selected profile not found in configuration.")
            else:
                messagebox.showwarning("Profile Already Exists", "Profile with this name already exists.")
        else:
            messagebox.showwarning("Invalid Profile Name", "Please enter a valid profile name.")


def delete_profile():
    global selected_profile, stop_scan, dynamic_filename_var, dynamicSaveCheckbutton

    if not selected_profile:
        messagebox.showinfo("Delete Profile", "Please select a profile to delete.")
        return

    confirm = messagebox.askyesno("Delete Profile", f"Do you want to delete the '{selected_profile}' profile? This action cannot be undone.")
    if confirm:
        del config['profiles'][selected_profile]
        update_profile_dropdown()

        # Set the selected profile to the first key in the updated profiles
        profiles = list(config['profiles'].keys())
        if profiles:
            selected_profile = profiles[0]
            profile_var.set(selected_profile)
        else:
            selected_profile = None
            profile_var.set("")

        write_data()
        

def load_profiles():
    # Load the list of profiles from the config
    profiles = list(config['profiles'].keys())
    return profiles


def load_last_used_profile():
    last_used_profile = config['last_used_profile']
    if last_used_profile in config['profiles']:
        selected_profile = last_used_profile
    else:
        selected_profile = "Default Profile"  # Set a default profile if necessary


def select_profile(event):
    global selected_profile, dynamic_filename_var, scan_thread, profile_changed_flag
    selected_profile = profile_var.get()
    config['last_used_profile'] = selected_profile

    # Stop the current scanner (if running)
    stop_scan.set()

    # Clear the current selection in the listbox
    savefileListbox.selection_clear(0, 'end')

    if selected_profile in config['profiles']:
        profile_data = config['profiles'][selected_profile]
        profile_changed_flag = True

        # Handle Dynamic Save Slots
        if profile_data['dynamicsaves'] == 0:
            dynamic_filename_var.set(0)
        elif profile_data['dynamicsaves'] == 1:
            dynamic_filename_var.set(1)
            # Recreate and start the scanner thread
            stop_scan.clear()
            scan_thread = threading.Thread(target=scan_folder, args=(selected_profile,))
            scan_thread.daemon = True
            scan_thread.start()

        # Handle Secondary Save Slot
        if profile_data['secondarystate'] == "normal":
            # Check the checkbox, turn on browse button and label
            saveSlot2Checkbutton.select()
            saveSlot2Button['state'] = NORMAL
            saveSlot2DirLabel['state'] = NORMAL
        else:
            # Disable the browse button and label
            saveSlot2Checkbutton.deselect()
            saveSlot2Button['state'] = DISABLED
            saveSlot2DirLabel['state'] = DISABLED

        # Update other UI elements
        loadSaveDirectory = profile_data['inputfile']
        closest_folder = get_closest_folder(loadSaveDirectory)
        loadSaveDir.set(closest_folder)
        full_file_path = profile_data['outputfile']
        file_name = basename(full_file_path)
        saveSlotDir.set(file_name)
        full_file_path_secondary = profile_data['outputfilesecondary']
        file_name_secondary = basename(full_file_path_secondary)
        saveSlot2Dir.set(file_name_secondary)

        # Update the input directory for the selected profile
        input_dir_load(profile_data['inputfile'], selected_profile, [])

        # Refresh the listbox
        write_data()
        refresh_listbox()

    
def listbox_populate(filepath, input_dir): #Get a list of all save files in the chosen directory.
    try:
        if not os.path.exists(config['profiles'][selected_profile]['inputfile']):
            loadSaveDir.set("Not Assigned")
            messagebox.showwarning("WARNING", "The specified directory for Save Files does not exist. Please choose a different directory.")
            return
        
        for path in os.listdir(filepath):
            if os.path.isfile(os.path.join(filepath, path)):
                if path.endswith('.sav'): #Only include valid file types.
                    input_dir.append(path)
                    
        savefileListboxItems.set(input_dir) #update the GUI list.
        closest_folder = get_closest_folder(filepath)
        loadSaveDir.set(closest_folder)#update the GUI text.
        
    except Exception as e:
        logging.error("Failed to load listbox: {e}")
        messagebox.showerror("Error", f"An error occurred while populating the listbox: {e}")

    
def refresh_listbox(new_save_name=None):
    global selected_input, profile_changed_flag
    try:
        if not os.path.exists(config['profiles'][selected_profile]['inputfile']):
            messagebox.showwarning("Filepath Not Found", "The specified filepath does not exist.")
            return

        listbox_populate(filepath=config['profiles'][selected_profile]['inputfile'], input_dir=[])

        if new_save_name and not profile_changed_flag:
            # Find the index of the newly created save
            new_save_index = savefileListbox.get(0, END).index(new_save_name)
            savefileListbox.selection_clear(0, END)  # Clear the current selection
            savefileListbox.selection_set(new_save_index)  # Select the new save
            savefileListbox.see(new_save_index)  # Scroll to make the new save visible
        elif selected_input and not profile_changed_flag:
            new_save_index = savefileListbox.get(0, END).index(selected_input)
            savefileListbox.selection_clear(0, END)  # Clear the current selection
            savefileListbox.selection_set(new_save_index)  # Select the new save
            
        profile_changed_flag = False
    except Exception as e:
        logging.error(f"Failed to refresh listbox: {e}")
        messagebox.showerror("Error", f"An error occurred while refreshing the listbox: {e}")
        

def auto_refresh_listbox():
    selected_items = savefileListbox.curselection()
    if selected_items:
        selected_item = selected_items[0]
        refresh_listbox()
        savefileListbox.selection_set(selected_item)
    root.after(5000, auto_refresh_listbox)  # Schedule the refresh every 60 seconds (adjust as needed)


def update_config(config, default_config):
    # Update existing configuration with new keys from default configuration
    for key, value in default_config.items():
        config.setdefault(key, value)

    # Update user's profile data with new keys from the default profile
    for profile, profile_data in config["profiles"].items():
        for key, value in default_config["profiles"]["Default Profile"].items():
            profile_data.setdefault(key, value)

    # Save the updated configuration to the file
    with open('data\\config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)


# Load the existing configuration or create a new one with defaults
try:
    with open('data\\config.json', 'r') as f:
        config = json.load(f)

except (FileNotFoundError, json.JSONDecodeError):
    # Create a new configuration with defaults if the file is not found or cannot be decoded
    config = default_config
    with open('data\\config.json', 'w') as f:
        json.dump(config, f, indent=4)

# Update the configuration
update_config(config, default_config)
        
if config['disclaimer'] == 1 or config['disclaimer']!= 0: #Executes a TKinter prompt window if the user is opted in.
    root0=Tk()
    root0.geometry("300x160")
    root0.title("NOTICE")
    root0.resizable(False, False)
    icon_image = PhotoImage(data=icon_data)
    root0.iconphoto(True,icon_image)
    cb = IntVar()
    line0 = Label(root0, text="If you are using this tool for Dead Space Remake Impossible Mode, the Save Slot you choose must also be on Impossible, otherwise the difficulty will be set to Hard.", font='Arial 10 bold', wraplength=250).pack(pady=2)
    Checkbutton(root0,text="Do not show this message again.", font=('Arial 10'), variable=cb, onvalue=1, offvalue=0, command=confirm_opt).pack(pady=5)
    button0 = Button(root0, text="OK", command=close_opt)
    button0.pack(pady=5)
    root0.mainloop()


#Primary Functions
is_setting_hotkey = False #Global flag variable. Will be used to prevent accidental hotkey activations.
is_in_prompt = False #Global flag variable. Will be used to prevent accidentally saving/loading during renaming.

def input_dir_load(filepath, selected_profile, input_dir):
    try:
        if filepath == "":
            pass
        else:
            listbox_populate(filepath=filepath, input_dir=input_dir)
            
    except:
        filepath = "Saves/"
        config['profiles'][selected_profile]['inputfile'] = filepath
        write_data()
        listbox_populate(filepath=filepath, input_dir=input_dir)
        messagebox.showwarning("Directory Not Found", "Save File Directory not found. Directory reset to Default...") #Prompt user reset completed.

    
def open_file_input(selected_profile): #Requests the user choose a directory where save files are.
    filepath = askdirectory(title="Select a Folder") + '/' #Ask for the file.
    if filepath == "/": #Change nothing if the user hits Cancel.
        return
    
    else: #Write the provided file to saved application data. This allows users to only have to set up their save files on initial launch.
         # Update the inputfile for the selected profile
        if selected_profile in config['profiles']:
            config['profiles'][selected_profile]['inputfile'] = filepath
            write_data()
            input_dir_load(filepath=filepath, selected_profile=selected_profile, input_dir=[])
        else:
            messagebox.showwarning("Profile Not Found", "Selected profile not found in configuration.")

        
def open_file_output(selected_profile): #Requests the user to choose save slot for loading and creating save files.
    filepath = filedialog.askopenfilename(title="Select a Save File", filetype=[("SAV Files", "*.sav"), ("All Files", "*.*")]) #Ask for the file.
    if filepath == "": #Change nothing if the user hits Cancel.
        return
        
    else: #Write the provided file to saved application data. This allows users to only have to set up their save files on initial launch.
        # Update the outputfile for the selected profile
        if selected_profile in config['profiles']:
            config['profiles'][selected_profile]['outputfile'] = filepath
            write_data()
            file_name = basename(filepath)
            saveSlotDir.set(file_name)  # update the GUI text.
        else:
            messagebox.showwarning("Profile Not Found", "Selected profile not found in configuration.")


def open_file_output_secondary(): #Requests the user to choose save slot for loading and creating save files.
    filepath = filedialog.askopenfilename(title="Select a Save File", filetype=[("SAV Files","*.sav"), ("All Files", "*.*")]) #Ask for the file.
    if filepath == "": #Change nothing if the user hits Cancel.
        return
        
    else: #Write the provided file to saved application data. This allows users to only have to set up their save files on initial launch.
        # Update the outputfile for the selected profile
        if selected_profile in config['profiles']:
            config['profiles'][selected_profile]['outputfilesecondary'] = filepath
            write_data()
            file_name = basename(filepath)
            saveSlot2Dir.set(file_name)  # update the GUI text.
        else:
            messagebox.showwarning("Profile Not Found", "Selected profile not found in configuration.")

        
def input_selected(event):
    global selected_input
    try:
        selected_indice_input = savefileListbox.curselection()[0]
        selected_input = savefileListbox.get(selected_indice_input)
    except:
        selected_input = ""

            
def on_press(origin, key):  # Binds a process to a hotkey and writes the new keybind to user settings.
    global is_setting_hotkey, hotkey_success, new_hotkey
    is_setting_hotkey = True
    new_hotkey = str(key).replace("'", "").replace("Key.", "").upper()
    
    if config['saveHotkey'] == new_hotkey or config['loadHotkey'] == new_hotkey or config['renameHotkey'] == new_hotkey or config['deleteHotkey'] == new_hotkey:
        hotkey_success = False
        return False
    
    if origin == 'save':
        keyboard.remove_hotkey(config['saveHotkey'])  # remove old hotkey
        keyboard.add_hotkey(new_hotkey, lambda: createSave())
        config['saveHotkey'] = new_hotkey
        
    elif origin == 'load':
        keyboard.remove_hotkey(config['loadHotkey'])  # remove old hotkey
        keyboard.add_hotkey(new_hotkey, lambda: loadSave())
        config['loadHotkey'] = new_hotkey
        
    elif origin == 'rename':
        keyboard.remove_hotkey(config['renameHotkey'],) #remove old hotkey
        keyboard.add_hotkey(new_hotkey, lambda: check_window_and_rename())
        config['renameHotkey'] = new_hotkey

    elif origin == 'delete':
        keyboard.remove_hotkey(config['deleteHotkey'],) #remove old hotkey
        keyboard.add_hotkey(new_hotkey, lambda: check_window_and_delete())
        config['deleteHotkey'] = new_hotkey
        
    write_data()
    is_setting_hotkey = False
    hotkey_success = True
    return False


def set_hotkey_save(): #Activates the listener to accept the new keybind. Also updates the GUI to show the new keybind.
    global is_setting_hotkey, hotkey_success, new_hotkey
    is_setting_hotkey = True
    try:
        with Listener(on_press=partial(on_press, 'save')) as listener:
            listener.join()
        
        if hotkey_success:
            saveHotkey_label.set(f"Save: {config['saveHotkey']}")
        
        else:
            messagebox.showwarning("WARNING", "Hotkey is already bound.")

    except ValueError as e:
        keyboard.add_hotkey(config['saveHotkey'], lambda: createSave())
        logging.error(f"Hotkey selection is not supported by keyboard library: {e}")
        messagebox.showwarning("WARNING", f"Hotkey {new_hotkey} not supported. Please bind a different key.")
        
    is_setting_hotkey = False


def set_hotkey_load(): #Activates the listener to accept the new keybind. Also updates the GUI to show the new keybind.
    global is_setting_hotkey, hotkey_success
    is_setting_hotkey = True
    try:
        with Listener(on_press=partial(on_press, 'load')) as listener:
            listener.join()
        
        if hotkey_success:
            loadHotkey_label.set(f"Load: {config['loadHotkey']}")
        
        else:
            messagebox.showwarning("WARNING", "Hotkey is already bound.")
            
    except ValueError as e:
        keyboard.add_hotkey(config['loadHotkey'], lambda: loadSave())
        logging.error(f"Hotkey selection is not supported by keyboard library: {e}")
        messagebox.showwarning("Error", f"Hotkey {new_hotkey} not supported. Please bind a different key.")
        
    is_setting_hotkey = False


def set_hotkey_rename(): #Activates the listener to accept the new keybind. Also updates the GUI to show the new keybind.
    global is_setting_hotkey, hotkey_success
    is_setting_hotkey = True
    try:
        with Listener(on_press=partial(on_press, 'rename')) as listener:
            listener.join()
        
        if hotkey_success:
            renameHotkey_label.set(f"Rename: {config['renameHotkey']}")
        
        else:
            messagebox.showwarning("WARNING", "Hotkey is already bound!")
    except ValueError as e:
        keyboard.add_hotkey(config['renameHotkey'], lambda: check_window_and_rename())
        logging.error(f"Hotkey selection is not supported by keyboard library: {e}")
        messagebox.showwarning("WARNING", f"Hotkey {new_hotkey} not supported. Please bind a different key.")
        
    is_setting_hotkey = False


def set_hotkey_delete(): #Activates the listener to accept the new keybind. Also updates the GUI to show the new keybind.
    global is_setting_hotkey, hotkey_success
    is_setting_hotkey = True
    try:
        with Listener(on_press=partial(on_press, 'delete')) as listener:
            listener.join()
        
        if hotkey_success:
            deleteHotkey_label.set(f"Delete: {config['deleteHotkey']}")
        
        else:
            messagebox.showwarning("WARNING", "Hotkey is already bound!")
    except ValueError as e:
        keyboard.add_hotkey(config['deleteHotkey'], lambda: check_window_and_delete())
        logging.error(f"Hotkey selection is not supported by keyboard library: {e}")
        messagebox.showwarning("WARNING", f"Hotkey {new_hotkey} not supported. Please bind a different key.")
        
    is_setting_hotkey = False


def check_window_and_rename():
    active_window = gw.getActiveWindow()
    if active_window is not None and "Universal Save Tool" in active_window.title:
        rename_file_scheduler()


def check_window_and_delete():
    active_window = gw.getActiveWindow()
    if active_window is not None and "Universal Save Tool" in active_window.title:
        deleteSave_scheduler()


def confirm_sound(): #Toggles the audio cue when saves are injected.
    if sound_var.get() == 1:
        config['sound'] = 1
        write_data()
    elif sound_var.get() == 0:
        config['sound'] = 0
        write_data()

    
def reset_config():
    # Ask for confirmation
    confirmation = messagebox.askyesno("Reset Confirmation", "Are you sure you want to reset? All data will be wiped!")

    if confirmation:
        global config
        config = default_config
        write_data()
        messagebox.showinfo("Reset Complete", "Reset complete! The software will close.")
        root.destroy()  # Close the tool
    else:
        # User chose not to reset, do nothing
        pass

    
def hyperlink(url):
    webbrowser.open_new(url)

    
def createSave():
    global selected_input

    if is_setting_hotkey:
        return
    if is_in_prompt:
        return

    try:
        dst_path = config['profiles'][selected_profile]['outputfile']
        if dst_path == "Not Assigned":
            messagebox.showwarning("Save Slot Not Selected", "You must select a Save Slot to continue.")
            return False
        
        saveName = f"UST.sav" #Be careful using a fixed file extension. Some games may not use .sav - Could add a separate module to detect other extensions.
        base_name, file_extension = os.path.splitext(saveName)
        counter = 0
        counter_str = str(counter).zfill(3)
        new_save_name = f"{base_name}_{counter_str}{file_extension}"
        src_path = config['profiles'][selected_profile]['inputfile'] + new_save_name
        if src_path == dst_path:
            messagebox.showwarning("WARNING", "Input and Output Files must be different.")
            return False
        
        while os.path.exists(src_path):
            counter_str = str(counter).zfill(3)
            new_save_name = f"{base_name}_{counter_str}{file_extension}"
            src_path = config['profiles'][selected_profile]['inputfile'] + new_save_name
            counter += 1

        shutil.copy(dst_path, src_path)
        sound_var = config['sound']
        if sound_var == 1:
            try:
                winsound.Beep(500,100)
            except Exception as e:
                logging.error(f"An error occurred while playing the sound: {e}")
                
        selected_input = new_save_name
        refresh_listbox(new_save_name)
        
    except Exception as e:
        logging.error(f"An error occurred while creating the save: {e}")
        messagebox.showwarning ("ERROR", "An Error occurred while creating the save.") #Prompt user file or directory not there.

        
def loadSave():
    global selected_input

    if is_setting_hotkey:
        return
    if is_in_prompt:
        return
    try:
        if selected_input == "":
            messagebox.showwarning("Save File Missing", "You must select a Save File to load.")
            return False
        
        dst_path = config['profiles'][selected_profile]['outputfile']
        if dst_path == "Not Assigned":
            messagebox.showwarning("Not Assigned", "You must select a Save Slot to write to.")
            return False
        
        src_path = config['profiles'][selected_profile]['inputfile'] + selected_input
        if src_path == "":
            messagebox.showwarning("Directory Not Assigned", "Load a directory to continue.")
            return False
        
        if src_path == dst_path:
            messagebox.showwarning("WARNING", "Save Slot cannot be the same file as your backup save file.")
            return False
        
        shutil.copy(src_path, dst_path)

        if secondary_save_enabled.get() == 1:
            dst_path_secondary = config['profiles'][selected_profile]['outputfilesecondary']
            if dst_path_secondary == "Not Assigned":
                messagebox.showwarning("Not Assigned", "You must select a Save Slot to write to.")
                return False
            shutil.copy (src_path, dst_path_secondary)

        sound_var = config['sound']
        if sound_var == 1:
            try:
                winsound.Beep(1000,100)
            except Exception as e:
                logging.error(f"An error occurred while playing the sound: {e}")
    except:
        logging.error(f"An error occurred while loading the save: {e}")
        messagebox.showwarning ("ERROR", "An Error occurred while loading the save.") #Prompt user file no longer there.


def rename_file_scheduler():
    if is_setting_hotkey:
        return
    if is_in_prompt:
        return
    root.after(0,rename_file)


def rename_file():
    global is_in_prompt
    global selected_input
    is_in_prompt = True
    
    try:
        selected_indices = savefileListbox.curselection()
        if not selected_indices:
            messagebox.showwarning("No Selection", "Please select a save file from the list.")
            is_in_prompt = False
            return
        
        selected_index = selected_indices[0]
        old_name = config['profiles'][selected_profile]['inputfile'] + savefileListbox.get(selected_index)
        new_save_name = simpledialog.askstring("Input", "Enter a new name: ")
        if new_save_name is None:
            is_in_prompt = False
            return
        
        if new_save_name == "":
            messagebox.showwarning("Blank File Name", "File name cannot be blank!")
            is_in_prompt = False
            return
        
        new_name = config['profiles'][selected_profile]['inputfile'] + new_save_name + ".sav"
        if os.path.exists(new_name):
            messagebox.showwarning("File Already Exists", "File name already exists!")
            is_in_prompt = False
            return
        
        os.rename(old_name, new_name)
        new_save_name = new_save_name + ".sav"
        selected_input = new_save_name
        refresh_listbox(new_save_name)
        
    except Exception as e:
        logging.error(f"An error occurred in rename_file: {e}")
        messagebox.showerror("Error", f"An error occurred while renaming the file: {e}")
        
    is_in_prompt = False


def deleteSave_scheduler():
    if is_setting_hotkey:
        return
    if is_in_prompt:
        return
    root.after(0,deleteSave())


def deleteSave():
    global is_in_prompt
    global selected_input
    is_in_prompt = True
    
    try:
        selected_indices = savefileListbox.curselection()
        if not selected_indices:
            messagebox.showwarning("No Selection", "Please select a save file from the list.")
            is_in_prompt = False
            return
        
        selected_index = selected_indices[0]
        save_to_delete = savefileListbox.get(selected_index)
        file_path = os.path.join(config['profiles'][selected_profile]['inputfile'], save_to_delete)

        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this save?")

        if confirm:
            os.remove(file_path)
            next_index = selected_index + 1 if selected_index + 1 < savefileListbox.size() else selected_index - 1
            selected_input = savefileListbox.get(next_index)

        is_in_prompt = False
        refresh_listbox()

    except IndexError:
        is_in_prompt = False
        messagebox.showwarning("No Save Selected", "No save file selected. Please select a save file to delete.")
    except Exception as e:
        is_in_prompt = False
        logging.error(f"An error occurred in deleteSave: {e}")
        messagebox.showerror("Error", f"An error occurred while deleting a save: {e}")
        

# Init scan variables
scan_thread = None
stop_scan = threading.Event()

def scan_folder(selected_profile):
    global stop_scan, dynamic_filename_var
    while not stop_scan.is_set():
        try:
            # Check if the folder exists for the main save slot
            output_file_path = config['profiles'][selected_profile]['outputfile']
            folder_path, file_name = os.path.split(output_file_path)

            if not os.path.exists(folder_path):
                messagebox.showinfo("Reminder", "Please configure your main save slot before enabling Dynamic Save Slots.")
                stop_scan.set()  # Shut down the scanner
                dynamic_filename_var.set(0)  # Turn off the checkbox
                config['profiles'][selected_profile]['dynamicsaves'] = 0
                write_data()
                continue

            files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
            found_file = find_file_with_numbers(files)

            if found_file:
                # Update the saveSlotDir and configuration for the main save slot
                file_name = basename(os.path.join(folder_path, found_file))
                saveSlotDir.set(file_name)
                config['profiles'][selected_profile]['outputfile'] = os.path.join(folder_path, found_file)
                write_data()

            if config['profiles'][selected_profile]['secondarystate'] == "normal":
                    output_file_path_secondary = config['profiles'][selected_profile]['outputfilesecondary']
                    folder_path_secondary, file_name_secondary = os.path.split(output_file_path_secondary)
                    if config['profiles'][selected_profile]['outputfilesecondary'] == "Not Assigned" or not os.path.exists(folder_path_secondary):
                        messagebox.showinfo("Reminder", "Please configure your secondary save slot before enabling Dynamic Save Slots.")
                        stop_scan.set()  # Shut down the scanner
                        dynamic_filename_var.set(0)  # Turn off the checkbox
                        config['profiles'][selected_profile]['dynamicsaves'] = 0
                        write_data()
                        continue

                    files_secondary = [f for f in os.listdir(folder_path_secondary) if os.path.isfile(os.path.join(folder_path_secondary, f))]
                    found_file_secondary = find_file_with_numbers(files_secondary)

                    if found_file_secondary:
                        # Update the saveSlotDirSecondary and configuration for the secondary save slot
                        file_name_secondary = basename(os.path.join(folder_path_secondary, found_file_secondary))
                        saveSlot2Dir.set(file_name_secondary)
                        config['profiles'][selected_profile]['outputfilesecondary'] = os.path.join(folder_path_secondary, found_file_secondary)
                        write_data()
                        

        except FileNotFoundError as e:
            logging.error(f"Error in scanning folder: {e}")
            messagebox.showerror("File Not Found", f"Error in scanning folder: {e}")
        
        time.sleep(5)  # Adjust the interval as needed


def find_file_with_numbers(files):
    # Exclude files containing the word "container" or numbers in the extension
    filtered_files = [file for file in files if 'container' not in file.lower() and not any(char.isdigit() for char in os.path.splitext(file)[1])]

    # Find the first file with numbers in its name from the filtered list
    for file in filtered_files:
        if any(char.isdigit() for char in file):
            return file
    return None


def toggle_dynamic_filename():
    global scan_thread, stop_scan
    if dynamic_filename_var.get() == 1:
        confirmation = messagebox.askyesno("Confirm", "Dynamic Filename only works for games with saves that are renamed when overwritten. Are you sure you want to enable this feature?")
        if confirmation:
            # Enable dynamic filename logic
            config['profiles'][selected_profile]['dynamicsaves'] = 1
            stop_scan.clear()
            scan_thread = threading.Thread(target=scan_folder, args=(selected_profile,))
            scan_thread.daemon = True
            scan_thread.start()
        else:
            # User chose not to enable dynamic filename detection
            dynamic_filename_var.set(0)  # Uncheck the check button
    elif dynamic_filename_var.get() == 0:
        config['profiles'][selected_profile]['dynamicsaves'] = 0
        if scan_thread:
            dynamic_filename_var.set(0)
            message_box = messagebox.showinfo("Dynamic Filename Disabled", "Dynamic filename detection is disabled. There will be one final scan after you click OK. After that you will be able to resume using the software.")
            # Disable dynamic filename logic
            stop_scan.set()  # Set the stop_scan flag
            scan_thread.join()  # Wait for the scanning thread to finish with a timeout           
    write_data()
        

# Create a function to handle the checkbox state change
def on_checkbox_change():
    # Assuming selected_profile is the current profile
    if secondary_save_enabled.get() == 1:
        config['profiles'][selected_profile]['secondarystate'] = "normal"
        # Enable secondary save slot selection
        saveSlot2DirLabel.config(state=NORMAL)
        saveSlot2Button.config(state=NORMAL)
    else:
        # Disable secondary save slot selection
        config['profiles'][selected_profile]['secondarystate'] = "disabled"
        saveSlot2DirLabel.config(state=DISABLED)
        saveSlot2Button.config(state=DISABLED)

    # Save the data to the configuration file
    write_data()


def update_profile_dropdown():
    profiles = list(config['profiles'].keys())
    profileDropdown['values'] = profiles

    
def adjust_wraplength(event, *labels):
    new_width = event.width
    new_wraplength = min(new_width - 10, 1000)  # Adjust the value as needed
    for label in labels:
        label.config(wraplength=new_wraplength)


def get_closest_folder(directory):
    # Get the last part of the path, which is the closest folder
    closest_folder = '/' + os.path.basename(os.path.normpath(directory)) + '/'
    return closest_folder
    

def on_close():
    global stop_scan
    stop_scan.set()  # Set the stop_scan event to signal the scan_folder thread to stop
    width = root.winfo_width()
    height = root.winfo_height()
    config['window_size'] = {"width": width, "height": height}
    update_config(config, default_config)
    root.destroy()


#Main Tkinter Window Settings.
root=Tk()
icon_image = PhotoImage(data=icon_data)
root.iconphoto(True,icon_image)
width = config['window_size']['width']
height = config['window_size']['height']
root.geometry(f"{width}x{height}")
root.title("Universal Save Tool")
root.minsize(300,440)
root.rowconfigure(7, weight=1)
root.columnconfigure(2, weight=1)
#Define Label Variables.
loadSaveDir = StringVar()
saveSlotDir = StringVar()
saveSlot2Dir = StringVar()
saveHotkey_var = StringVar()
saveHotkey_label = StringVar()
loadHotkey_var = StringVar()
loadHotkey_label = StringVar()
renameHotkey_var = StringVar()
renameHotkey_label = StringVar()
deleteHotkey_var = StringVar()
deleteHotkey_label = StringVar()
profile_var = tk.StringVar()
sound_var = IntVar()
secondary_save_enabled = IntVar()
dynamic_filename_var = IntVar()
#Import Hotkey and Directory Settings From Last Session and Initialize Variables.
saveHotkey_var.set (config['saveHotkey'])
saveHotkey_label.set(f"Save: {saveHotkey_var.get()}")
loadHotkey_var.set(config['loadHotkey'])
loadHotkey_label.set(f"Load: {loadHotkey_var.get()}")
renameHotkey_var.set(config['renameHotkey'])
renameHotkey_label.set(f"Rename: {renameHotkey_var.get()}")
deleteHotkey_var.set(config['deleteHotkey'])
deleteHotkey_label.set(f"Delete: {deleteHotkey_var.get()}")
profiles = load_profiles()
profile_var.set(config['last_used_profile'])
loadSaveDirectory = config['profiles'][profile_var.get()]['inputfile']
closest_folder = get_closest_folder(loadSaveDirectory)
loadSaveDir.set(closest_folder)
sound_var.set(config['sound'])
if config['profiles'][profile_var.get()]['secondarystate'] == 'normal':
    secondary_save_enabled.set(1)
dynamic_filename_var.set(config['profiles'][profile_var.get()]['dynamicsaves'])
input_dir = []
selected_input = ""

#Hotkeys for creating and loading saves.
try:
    keyboard.add_hotkey(config['saveHotkey'], lambda: createSave())
except ValueError as e:
    keyboard.add_hotkey(default_config['saveHotkey'], lambda: createSave())
    saveHotkey_label.set(f"Save: {default_config['saveHotkey']}")
    config['saveHotkey'] = default_config['saveHotkey']
    write_data()
    messagebox.showerror("Error", "Save hotkey not supported. Resetting the key to default.")
    
try:
    keyboard.add_hotkey(config['loadHotkey'], lambda: loadSave())
except ValueError as e:
    keyboard.add_hotkey(default_config['loadHotkey'], lambda: loadSave())
    loadHotkey_label.set(f"Load: {default_config['loadHotkey']}")
    config['loadHotkey'] = default_config['loadHotkey']
    write_data()
    messagebox.showerror("Error", "Load hotkey not supported. Resetting the key to default.")
    
try:
    keyboard.add_hotkey(config['renameHotkey'], lambda: check_window_and_rename())
except ValueError as e:
    keyboard.add_hotkey(default_config['renameHotkey'], lambda: check_window_and_rename())
    saveHotkey_label.set(f"Rename: {default_config['renameHotkey']}")
    config['renameHotkey'] = default_config['renameHotkey']
    write_data()
    messagebox.showerror("Error", "Rename hotkey not supported. Resetting the key to default.")
try:
    keyboard.add_hotkey(config['deleteHotkey'], lambda: check_window_and_delete())
except ValueError as e:
    keyboard.add_hotkey(default_config['deleteHotkey'], lambda: check_window_and_delete())
    saveHotkey_label.set(f"Delete: {default_config['deleteHotkey']}")
    config['deleteHotkey'] = default_config['deleteHotkey']
    write_data()
    messagebox.showerror("Error", "Delete hotkey not supported. Resetting the key to default.")

# Call the load_last_used_profile function when your application starts
load_last_used_profile()

# Make sure config['profiles'] is not empty
if 'profiles' in config and config['profiles']:
    selected_profile = next(iter(config['profiles']))
else:
    selected_profile = "Default Profile"  # Set a default profile name in case there are no profiles defined

#GUI Windows - Tabs for Profiles, Keybinds, About - Main
notebook = ttk.Notebook(root)
notebook.pack(anchor="nw", side="top", fill="x")
profileFrame = ttk.Frame(notebook)
keybindFrame = ttk.Frame(notebook)
aboutFrame = ttk.Frame(notebook)
notebook.add(profileFrame, text="Profiles")
notebook.add(keybindFrame, text="Keybinds")
notebook.add(aboutFrame, text="About")
for frame in [profileFrame, keybindFrame, aboutFrame]:
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)
main_frame = ttk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)
main_frame.bind("<Configure>", lambda event: adjust_wraplength(event, loadSaveDirLabel, saveSlotDirLabel, saveSlot2DirLabel))
main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(2, weight=1)
#Profiles Widgets
profileDropdown = ttk.Combobox(profileFrame, textvariable=profile_var, values=list(config['profiles'].keys()), state="readonly", width=8000)
profileDropdown.bind("<<ComboboxSelected>>", select_profile)
profileDropdown.grid(row=0, column=0, sticky=W, pady=5, padx=5)
newProfileButton = Button(profileFrame, text="New", command=create_profile)
newProfileButton.grid(row=0, column=1, sticky=W, padx=5)
editProfileButton = Button(profileFrame, text="Edit", command=edit_profile)
editProfileButton.grid(row=0, column=2, sticky=E, padx=5)
duplicateProfileButton = Button(profileFrame, text="Duplicate", command=duplicate_profile)
duplicateProfileButton.grid(row=0, column=3, sticky=E, padx=5)
deleteProfileButton = Button(profileFrame, text="Delete", command=delete_profile)
deleteProfileButton.grid(row=0, column=4, sticky=E, padx=5)
#Keybind Widgets.
saveHotkeyLabel = Label(keybindFrame, textvariable=saveHotkey_label, font='Arial 10')
saveHotkeyLabel.grid(row=0, column=0, sticky=W, padx=2)
saveHotkeyButton = Button(keybindFrame, text="Bind Key", command=set_hotkey_save).grid(row=0, column=3, sticky=E, padx=5, pady=5)
loadHotkeyLabel = Label(keybindFrame, textvariable=loadHotkey_label, font='Arial 10')
loadHotkeyLabel.grid(row=1, column=0, sticky=W, padx=2)
loadHotkeyButton = Button(keybindFrame, text="Bind Key", command=set_hotkey_load).grid(row=1, column=3, sticky=E, padx=5, pady=5)
renameHotkeyText = Label(keybindFrame, textvariable=renameHotkey_label, font='Arial 10')
renameHotkeyText.grid(row=2, column=0, sticky=W, padx=2)
renameHotkeyButton = Button(keybindFrame, text="Bind Key", command=set_hotkey_rename).grid(row=2, column=3, sticky=E, padx=5, pady=5)
deleteHotkeyText = Label(keybindFrame, textvariable=deleteHotkey_label, font='Arial 10')
deleteHotkeyText.grid(row=3, column=0, sticky=W, padx=2)
deleteHotkeyButton = Button(keybindFrame, text="Bind Key", command=set_hotkey_delete).grid(row=3, column=3, sticky=E, padx=5, pady=5)
#About Frame Widgets
programNameLabel = Label(aboutFrame, text="Universal Save Tool")
programNameLabel.grid(row=0, column = 0, padx=2)
versionLabel = Label(aboutFrame, text=version + " by Hazeblade")
versionLabel.grid(row=1, column=0, padx=2)
hyperlinkLabel = Label(aboutFrame, text="Support me on Patreon!", fg="blue", cursor="hand2")
hyperlinkLabel.grid(row=2, column=0, padx=2)
hyperlinkLabel.bind("<Button-1>", lambda e: hyperlink("http://www.patreon.com/hazebladetv"))
resetButton = Button(aboutFrame, text="Reset", command=reset_config).grid(row=3, column=0, sticky=W, padx=5, pady=5)
audioCheckbutton = Checkbutton (aboutFrame, text="Audio", font='Arial 10', variable=sound_var, onvalue=1, offvalue=0, command=confirm_sound).grid(row=3, column=0, sticky=E, padx=5, pady=5)
#Load Save Widget
loadSaveLabel = Label(main_frame, text="Load Save:", font='Arial 10 bold')
loadSaveLabel.grid(row=0, column=0, sticky=W)
loadSaveButton = Button(main_frame, text="Browse...", command=lambda: open_file_input(selected_profile))
loadSaveButton.grid(row=0, column=0, sticky=E, padx=5)
loadSaveDirLabel = Label(main_frame, textvariable=loadSaveDir, font='Arial 10', wraplength=8000, justify="left")
loadSaveDirLabel.grid(row=1, column=0, sticky=W)
#Listbox Widget
listboxFrame = ttk.Frame(main_frame)
listboxFrame.grid(row=2, column=0, sticky="NSEW", padx=2)
listboxFrame.columnconfigure(0, weight=1)
listboxFrame.rowconfigure(0, weight=1)
savefileListboxItems = Variable(value=input_dir)
savefileListbox = tk.Listbox(listboxFrame, listvariable=savefileListboxItems, selectmode=SINGLE, height=6, width=40)
savefileListbox.grid(row=0, column=0, sticky="NSEW", padx=2)
savefileListbox.bind('<<ListboxSelect>>', input_selected)
savefileListboxScrollbar = Scrollbar(listboxFrame, orient=VERTICAL)
savefileListboxScrollbar.grid(row=0, column=1, sticky=NS, padx=0)
savefileListbox.config(yscrollcommand=savefileListboxScrollbar.set)
savefileListboxScrollbar.config(command=savefileListbox.yview)
input_dir_load(filepath=config['profiles'][selected_profile]['inputfile'], selected_profile=selected_profile, input_dir=[])
#Dynamic Save Slots Widget
dynamicSaveSubFrame = Frame(main_frame)
dynamicSaveSubFrame.grid(row=3, column=0, sticky=W)
dynamicSaveLabel = Label(dynamicSaveSubFrame, text="Dynamic Save Slots", font='Arial 10')
dynamicSaveLabel.grid(row=0, column=0)
dynamicSaveCheckbutton = Checkbutton(dynamicSaveSubFrame, variable=dynamic_filename_var, onvalue=1, offvalue=0, command=toggle_dynamic_filename)
dynamicSaveCheckbutton.grid(row=0, column=1)
#Save Slot 1 Widget
saveSlotLabel = Label(main_frame, text="Save Slot:", font='Arial 10 bold')
saveSlotLabel.grid(row=4, column=0, sticky=W)
saveSlotButton = Button(main_frame, text="Browse...", command=lambda: open_file_output(selected_profile))
saveSlotButton.grid(row=4, column=0, sticky=E, padx=5)
saveSlotDirLabel = Label(main_frame, textvariable=saveSlotDir, font='Arial 10', wraplength=8000, justify="left")
saveSlotDirLabel.grid(row=5, column=0, sticky=W)
#Save Slot 2 Widget
saveSlot2SubFrame = Frame(main_frame)
saveSlot2SubFrame.grid(row=6, column=0, sticky=W)
saveSlot2Label = Label(saveSlot2SubFrame, text="Save Slot 2:", font='Arial 10 bold')
saveSlot2Label.grid(row=0, column=0)
saveSlot2Checkbutton = Checkbutton(saveSlot2SubFrame, variable=secondary_save_enabled, onvalue=1, offvalue=0, command=on_checkbox_change)
saveSlot2Checkbutton.grid(row=0, column=1)
saveSlot2Button = Button(main_frame, text="Browse...", command=open_file_output_secondary, state=config['profiles'][selected_profile]['secondarystate'])
saveSlot2Button.grid(row=6, column=0, sticky=E, padx=5)
saveSlot2DirLabel = Label(main_frame, textvariable=saveSlot2Dir, font='Arial 10', wraplength=800, justify="left", state=config['profiles'][selected_profile]['secondarystate'])
saveSlot2DirLabel.grid(row=7, column=0, sticky=W)
#Start the auto-refresh loop
auto_refresh_listbox()
#Bind the on_close function to the window close event
root.protocol("WM_DELETE_WINDOW", on_close)
#Load and select the profile.
select_profile(None)
#Mainloop
root.mainloop()
