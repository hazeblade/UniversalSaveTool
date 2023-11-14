### Universal Save Tool by Hazeblade###
version = "ver. 1.2.8"
#Library Imports.
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askdirectory
from tkinter import simpledialog, messagebox
from functools import partial
from pynput.keyboard import Listener
import keyboard, shutil, winsound, json, webbrowser, os, logging, base64, tempfile, threading, time, copy
import tkinter as tk
import pygetwindow as gw
import base64
from tkinter import PhotoImage, ttk
from os.path import basename, join, isfile

#Preload Functions.
def write_data(): #Saves config.
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
    try:
        if cb.get() == 1:
            config['disclaimer'] = 0
        elif cb.get() == 0:
            config['disclaimer'] = 1
    except Exception as e:
        logging.error(f"An error occurred in confirm_opt(): {e}")
        messagebox.showerror("Error", f"An error occurred in confirm_opt(): {e}")
    
def close_opt(): #Closes the Dead Space Remake Impossible Disclaimer.
    try:
        write_data()
        root0.destroy()
    except Exception as e:
        logging.error(f"An error occurred in close_opt(): {e}")
        messagebox.showerror("Error", f"An error occurred in close_opt(): {e}")


def create_profile(): #Creates a new profile.
    try:
        global selected_profile
        profile_name = simpledialog.askstring("Create Profile", "Enter a name for the profile (max 20 characters):")
        if profile_name is not None:
            profile_name = profile_name[:20]
            if profile_name.strip():
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
    except Exception as e:
        logging.error(f"An error occurred in create_profile(): {e}")
        messagebox.showerror("Error", f"An error occurred in create_profile(): {e}")

def edit_profile(): #Edits an existing profile.
    try:
        global selected_profile
        selected_profile = profile_var.get()
        new_profile_name = simpledialog.askstring("Edit Profile", "Enter a new name for the profile:")
        if new_profile_name is not None:
            if new_profile_name.strip():
                if new_profile_name != selected_profile and new_profile_name not in config['profiles']:
                    if selected_profile in config['profiles']:
                        profile_data = config['profiles'][selected_profile]
                        del config['profiles'][selected_profile]
                        config['profiles'][new_profile_name] = profile_data
                        update_profile_dropdown()
                        write_data()

                        profile_var.set(new_profile_name)
                        select_profile(None)
                    else:
                        messagebox.showwarning("Profile Not Found", "Selected profile not found in configuration.")
                else:
                    messagebox.showwarning("Invalid Profile Name", "Please enter a valid and unique profile name.")
            else:
                messagebox.showwarning("Invalid Profile Name", "Please enter a valid profile name.")
    except Exception as e:
        logging.error(f"An error occurred in edit_profile(): {e}")
        messagebox.showerror("Error", f"An error occurred in edit_profile(): {e}")


def duplicate_profile(): #Copies an existing profile.
    try:
        global selected_profile
        selected_profile = profile_var.get()
        copied_profile_name = simpledialog.askstring("Edit Profile", "Enter a new name for the profile:")
        if copied_profile_name is not None:
            if copied_profile_name.strip():
                if copied_profile_name not in config['profiles']:
                    if selected_profile in config['profiles']:
                        profile_data = copy.deepcopy(config['profiles'][selected_profile])
                        config['profiles'][copied_profile_name] = profile_data
                        update_profile_dropdown()
                        write_data()

                        selected_profile = copied_profile_name
                        profile_var.set(selected_profile)
                        select_profile(None)
                    else:
                        messagebox.showwarning("Profile Not Found", "Selected profile not found in configuration.")
                else:
                    messagebox.showwarning("Profile Already Exists", "Profile with this name already exists.")
            else:
                messagebox.showwarning("Invalid Profile Name", "Please enter a valid profile name.")
    except Exception as e:
        logging.error(f"An error occurred in duplicate_profile(): {e}")
        messagebox.showerror("Error", f"An error occurred in duplicate_profile(): {e}")
        

def delete_profile(): #Deletes an existing profile.
    try:
        global selected_profile, stop_scan, dynamic_filename_var, dynamicSaveCheckbutton
        if not selected_profile:
            messagebox.showinfo("Delete Profile", "Please select a profile to delete.")
            return

        confirm = messagebox.askyesno("Delete Profile", f"Do you want to delete the '{selected_profile}' profile? This action cannot be undone.")
        if confirm:
            del config['profiles'][selected_profile]
            update_profile_dropdown()
            profiles = list(config['profiles'].keys())
            if profiles:
                selected_profile = profiles[0]
                profile_var.set(selected_profile)
            else:
                selected_profile = None
                profile_var.set("")
            write_data()
            
    except Exception as e:
        logging.error(f"An error occurred in delete_profile(): {e}")
        messagebox.showerror("Error", f"An error occurred in delete_profile(): {e}")


def load_profiles(): #Loads the list of profiles from the config.
    try:
        profiles = list(config['profiles'].keys())
        return profiles
    except Exception as e:
        logging.error(f"An error occurred in load_profiles(): {e}")
        messagebox.showerror("Error", f"An error occurred in load_profiles(): {e}")


def load_last_used_profile(): #Loads the most recently used profile on startup.
    try:
        last_used_profile = config['last_used_profile']
        if last_used_profile in config['profiles']:
            selected_profile = last_used_profile
        else:
            selected_profile = "Default Profile"
    except Exception as e:
        logging.error(f"An error occurred in load_last_used_profile(): {e}")
        messagebox.showerror("Error", f"An error occurred in load_last_used_profile(): {e}")


def select_profile(event): #Handles the selection of the current profile.
    try:
        global selected_profile, dynamic_filename_var, scan_thread, profile_changed_flag
        selected_profile = profile_var.get()
        config['last_used_profile'] = selected_profile
        stop_scan.set()

        savefileListbox.selection_clear(0, 'end')

        if selected_profile in config['profiles']:
            profile_data = config['profiles'][selected_profile]
            profile_changed_flag = True
            if profile_data['dynamicsaves'] == 0:
                dynamic_filename_var.set(0)
            elif profile_data['dynamicsaves'] == 1:
                dynamic_filename_var.set(1)
                stop_scan.clear()
                scan_thread = threading.Thread(target=scan_folder, args=(selected_profile,))
                scan_thread.daemon = True
                scan_thread.start()

            if profile_data['secondarystate'] == "normal":
                saveSlot2Checkbutton.select()
                saveSlot2Button['state'] = NORMAL
                saveSlot2DirLabel['state'] = NORMAL
            else:
                saveSlot2Checkbutton.deselect()
                saveSlot2Button['state'] = DISABLED
                saveSlot2DirLabel['state'] = DISABLED

            loadSaveDirectory = profile_data['inputfile']
            closest_folder = get_closest_folder(loadSaveDirectory)
            loadSaveDir.set(closest_folder)
            full_file_path = profile_data['outputfile']
            file_name = basename(full_file_path)
            saveSlotDir.set(file_name)
            full_file_path_secondary = profile_data['outputfilesecondary']
            file_name_secondary = basename(full_file_path_secondary)
            saveSlot2Dir.set(file_name_secondary)
            input_dir_load(profile_data['inputfile'], selected_profile, [])
            write_data()
            
            refresh_listbox()
    except Exception as e:
        logging.error(f"An error occurred in select_profile(): {e}")
        messagebox.showerror("Error", f"An error occurred in select_profile(): {e}")
        
    
def listbox_populate(filepath, input_dir): #Appends all .sav files to the listbox.
    try:
        if not os.path.exists(config['profiles'][selected_profile]['inputfile']):
            loadSaveDir.set("Not Assigned")
            messagebox.showwarning("WARNING", "The specified directory for Save Files does not exist. Please choose a different directory.")
            return
        
        for path in os.listdir(filepath):
            if os.path.isfile(os.path.join(filepath, path)):
                if path.endswith('.sav'):
                    input_dir.append(path)
                    
        savefileListboxItems.set(input_dir)
        closest_folder = get_closest_folder(filepath)
        loadSaveDir.set(closest_folder)
    except Exception as e:
        logging.error("Failed to load listbox: {e}")
        messagebox.showerror("Error", f"An error occurred while populating the listbox: {e}")
        
    
def refresh_listbox(new_save_name=None): #Refreshes the listbox.
    try:
        global selected_input, profile_changed_flag
        if not os.path.exists(config['profiles'][selected_profile]['inputfile']):
            messagebox.showwarning("Filepath Not Found", "The specified filepath does not exist.")
            return

        listbox_populate(filepath=config['profiles'][selected_profile]['inputfile'], input_dir=[])

        if new_save_name and not profile_changed_flag:
            new_save_index = savefileListbox.get(0, END).index(new_save_name)
            savefileListbox.selection_clear(0, END)
            savefileListbox.selection_set(new_save_index)
            savefileListbox.see(new_save_index)
        elif selected_input and not profile_changed_flag:
            new_save_index = savefileListbox.get(0, END).index(selected_input)
            savefileListbox.selection_clear(0, END)
            savefileListbox.selection_set(new_save_index)
            
        profile_changed_flag = False
    except Exception as e:
        logging.error(f"Failed to refresh listbox: {e}")
        messagebox.showerror("Error", f"An error occurred while refreshing the listbox: {e}")
        

def auto_refresh_listbox(): #Schedules automatic refreshing of the listbox.
    try:
        selected_items = savefileListbox.curselection()
        if selected_items:
            selected_item = selected_items[0]
            refresh_listbox()
            savefileListbox.selection_set(selected_item)
        root.after(5000, auto_refresh_listbox)
    except Exception as e:
        logging.error(f"An error occurred in auto_refresh_listbox(): {e}")
        messagebox.showerror("Error", f"An error occurred in auto_refresh_listbox(): {e}")
        

def update_config(config, default_config): #Ensures config data is available and creates it if not.
    try:
        for key, value in default_config.items():
            config.setdefault(key, value)
        if not config["profiles"]:
            config["profiles"]["Default Profile"] = {
                "inputfile": "Saves/",
                "outputfile": "Not Assigned",
                "outputfilesecondary": "Not Assigned",
                "secondarystate": "disabled",
                "dynamicsaves": 0
            }
        for profile, profile_data in config["profiles"].items():
            for key, value in default_config["profiles"]["Default Profile"].items():
                profile_data.setdefault(key, value)
        with open('data\\config.json', 'w') as config_file:
            json.dump(config, config_file, indent=4)
    except Exception as e:
        logging.error(f"An error occurred in update_config(): {e}")
        messagebox.showerror("Error", f"An error occurred in update_config(): {e}")
        
###################################################################
#Base64 String Encodes the logo/icon for the program.
icon_base64 = "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"
icon_data = base64.b64decode(icon_base64)

#Create Default Directories if they don't exist.
if not os.path.exists("Saves/"):
    os.makedirs("Saves/")
if not os.path.exists("data/"):
    os.makedirs("data/")

#Initialize error logging.
logging.basicConfig(filename='data\logs.txt', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
        
#Default Configuration Dictionary.
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

###################################################################
#Primary Functions
is_setting_hotkey = False #Global flag variable. Will be used to prevent accidental hotkey activations.
is_in_prompt = False #Global flag variable. Will be used to prevent accidentally saving/loading during renaming.

def input_dir_load(filepath, selected_profile, input_dir): #Provides a directory for the listbox to populate.
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
    if filepath == "/":
        return
    
    else:
        if selected_profile in config['profiles']:
            config['profiles'][selected_profile]['inputfile'] = filepath
            write_data()
            input_dir_load(filepath=filepath, selected_profile=selected_profile, input_dir=[])
        else:
            messagebox.showwarning("Profile Not Found", "Selected profile not found in configuration.")


def import_files():  #Converts a directory of files into .sav files.
    filepath = askdirectory(title="Select a Folder") + '/'
    import_counter = 0
    non_save_files = []
    if filepath == "/":
        return

    else:
        if selected_profile in config['profiles']:
            for path in os.listdir(filepath):
                full_path = join(filepath, path)
                if isfile(full_path) and not path.endswith('.sav'):
                    import_counter += 1
                    non_save_files.append(path)

            if import_counter >= 1:
                import_message = f"{import_counter} files detected that are not .sav files:\n\n"
                import_message += "\n".join(f"- {file}" for file in non_save_files)
                import_confirm = messagebox.askyesno("Import", f"{import_message}\nWould you like to import them?")
                if import_confirm:
                    for filename in non_save_files:
                        new_filename = os.path.splitext(filename)[0] + ".sav"
                        source_path = join(filepath, filename)
                        destination_path = join(config['profiles'][selected_profile]['inputfile'], new_filename)
                        counter = 0
                        while os.path.exists(destination_path):
                            new_filename = f"{os.path.splitext(filename)[0]}_{counter}.sav"
                            destination_path = os.path.join(filepath, new_filename)
                            counter += 1
                        if counter >=1:
                            import_duplicate = messagebox.showinfo("Duplicate Files", f"{counter} file(s) already exist. Appended integer to filename")
                        os.rename(source_path, destination_path)
                        input_dir.append(new_filename)

            config['profiles'][selected_profile]['inputfile'] = filepath
            write_data()
            input_dir_load(filepath=filepath, selected_profile=selected_profile, input_dir=[])
        else:
            messagebox.showwarning("Profile Not Found", "Selected profile not found in configuration.")

        
def open_file_output(selected_profile): #Requests the user to choose a save slot for loading and creating save files.
    try:
        filepath = filedialog.askopenfilename(title="Select a Save File", filetype=[("SAV Files", "*.sav"), ("All Files", "*.*")])
        if filepath == "":
            return
            
        else:
            if selected_profile in config['profiles']:
                config['profiles'][selected_profile]['outputfile'] = filepath
                write_data()
                file_name = basename(filepath)
                saveSlotDir.set(file_name)
            else:
                messagebox.showwarning("Profile Not Found", "Selected profile not found in configuration.")
    except Exception as e:
        logging.error(f"An error occurred in open_file_output(): {e}")
        messagebox.showerror("Error", f"An error occurred in open_file_output(): {e}")
        

def open_file_output_secondary(): #Requests the user to choose a secondary save slot for loading and creating save files.
    try:
        filepath = filedialog.askopenfilename(title="Select a Save File", filetype=[("SAV Files","*.sav"), ("All Files", "*.*")])
        if filepath == "":
            return
            
        else:
            if selected_profile in config['profiles']:
                config['profiles'][selected_profile]['outputfilesecondary'] = filepath
                write_data()
                file_name = basename(filepath)
                saveSlot2Dir.set(file_name)
            else:
                messagebox.showwarning("Profile Not Found", "Selected profile not found in configuration.")
    except Exception as e:
        logging.error(f"An error occurred in open_file_output_secondary(): {e}")
        messagebox.showerror("Error", f"An error occurred in open_file_output_secondary(): {e}")
        
        
def input_selected(event): #Handles the actively selected listbox item.
    try:
        global selected_input
        try:
            selected_indice_input = savefileListbox.curselection()[0]
            selected_input = savefileListbox.get(selected_indice_input)
        except:
            selected_input = ""
    except Exception as e:
        logging.error(f"An error occurred in input_selected(): {e}")
        messagebox.showerror("Error", f"An error occurred in input_selected(): {e}")

            
def on_press(origin, key):  #Binds a process to a hotkey and writes the new keybind to user settings.
    try:
        global is_setting_hotkey, hotkey_success, new_hotkey
        is_setting_hotkey = True
        new_hotkey = str(key).replace("'", "").replace("Key.", "").upper()
        
        if config['saveHotkey'] == new_hotkey or config['loadHotkey'] == new_hotkey or config['renameHotkey'] == new_hotkey or config['deleteHotkey'] == new_hotkey:
            hotkey_success = False
            return False
        
        if origin == 'save':
            keyboard.remove_hotkey(config['saveHotkey'])
            keyboard.add_hotkey(new_hotkey, lambda: createSave())
            config['saveHotkey'] = new_hotkey
            
        elif origin == 'load':
            keyboard.remove_hotkey(config['loadHotkey'])
            keyboard.add_hotkey(new_hotkey, lambda: loadSave())
            config['loadHotkey'] = new_hotkey
            
        elif origin == 'rename':
            keyboard.remove_hotkey(config['renameHotkey'],)
            keyboard.add_hotkey(new_hotkey, lambda: check_window_and_rename())
            config['renameHotkey'] = new_hotkey

        elif origin == 'delete':
            keyboard.remove_hotkey(config['deleteHotkey'],)
            keyboard.add_hotkey(new_hotkey, lambda: check_window_and_delete())
            config['deleteHotkey'] = new_hotkey
            
        write_data()
        is_setting_hotkey = False
        hotkey_success = True
        return False
    except Exception as e:
        logging.error(f"An error occurred in on_press(): {e}")
        messagebox.showerror("Error", f"An error occurred in on_press(): {e}")


def set_hotkey_save(): #Activates the listener to accept the new SAVE keybind.
    try:
        global is_setting_hotkey, hotkey_success, new_hotkey
        is_setting_hotkey = True
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


def set_hotkey_load(): #Activates the listener to accept the new LOAD keybind.
    try:
        global is_setting_hotkey, hotkey_success
        is_setting_hotkey = True
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


def set_hotkey_rename(): #Activates the listener to accept the new RENAME keybind.
    try:
        global is_setting_hotkey, hotkey_success
        is_setting_hotkey = True
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


def set_hotkey_delete(): #Activates the listener to accept the new DELETE keybind.
    try:
        global is_setting_hotkey, hotkey_success
        is_setting_hotkey = True
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


def check_window_and_rename(): #Handles allowing renaming only when tabbed into the UST.
    try:
        active_window = gw.getActiveWindow()
        if active_window is not None and "Universal Save Tool" in active_window.title:
            rename_file_scheduler()
    except Exception as e:
        logging.error(f"An error occurred in check_window_and_resume(): {e}")
        messagebox.showerror("Error", f"An error occurred in check_window_and_resume(): {e}")


def check_window_and_delete(): #Handles allowing deleting only when tabbed into the UST.
    try:
        active_window = gw.getActiveWindow()
        if active_window is not None and "Universal Save Tool" in active_window.title:
            deleteSave_scheduler()
    except Exception as e:
        logging.error(f"An error occurred in check_window_and_delete(): {e}")
        messagebox.showerror("Error", f"An error occurred in check_window_and_delete(): {e}")

def confirm_sound(): #Toggles the audio setting for the program.
    try:
        if sound_var.get() == 1:
            config['sound'] = 1
            write_data()
        elif sound_var.get() == 0:
            config['sound'] = 0
            write_data()
    except Exception as e:
        logging.error(f"An error occurred in confirm_sound(): {e}")
        messagebox.showerror("Error", f"An error occurred in confirm_sound(): {e}")
    
def reset_config(): #Resets the program to defaults and closes.
    try:
        confirmation = messagebox.askyesno("Reset Confirmation", "Are you sure you want to reset? All data will be wiped!")
        if confirmation:
            global config
            config = default_config
            write_data()
            messagebox.showinfo("Reset Complete", "Reset complete! The software will close.")
            root.destroy()
    except Exception as e:
        logging.error(f"An error occurred in reset_config(): {e}")
        messagebox.showerror("Error", f"An error occurred in reset_config(): {e}")
        
    
def hyperlink(url): #Opens a web link.
    try:
        webbrowser.open_new(url)
    except Exception as e:
        logging.error(f"An error occurred in hyperlink(): {e}")
        messagebox.showerror("Error", f"An error occurred in hyperlink(): {e}")

    
def createSave(): #Creates a new save file.
    try:
        global selected_input
        if is_setting_hotkey:
            return
        if is_in_prompt:
            return
        
        dst_path = config['profiles'][selected_profile]['outputfile']
        if dst_path == "Not Assigned":
            messagebox.showwarning("Save Slot Not Selected", "You must select a Save Slot to continue.")
            return False
            
        saveName = f"UST.sav"
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
        messagebox.showwarning ("ERROR", "An Error occurred while creating the save.")

        
def loadSave(): #Loads a selected save file.
    try:
        global selected_input
        if is_setting_hotkey:
            return
        if is_in_prompt:
            return
        
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
    except Exception as e:
        logging.error(f"An error occurred while loading the save: {e}")
        messagebox.showwarning ("ERROR", "An Error occurred while loading the save.")


def rename_file_scheduler(): #Checks that the user isn't setting a keybind or already renaming/deleting a file before executing a rename.
    try:
        if is_setting_hotkey:
            return
        if is_in_prompt:
            return
        root.after(0,rename_file)
    except Exception as e:
        logging.error(f"An error occurred in rename_file_scheduler(): {e}")
        messagebox.showwarning ("ERROR", "An Error occurred in rename_file_scheduler(): {e}")
        

def rename_file(): #Renames a file.
    try:
        global is_in_prompt
        global selected_input
        is_in_prompt = True
        
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


def deleteSave_scheduler(): #Checks that the user isn't setting a keybind or already renaming/deleting a file before executing a delete.
    try:
        if is_setting_hotkey:
            return
        if is_in_prompt:
            return
        root.after(0,deleteSave())
    except Exception as e:
        logging.error(f"An error occurred in deleteSave_scheduler(): {e}")
        messagebox.showwarning ("ERROR", "An Error occurred in deleteSave_scheduler(): {e}")
        

def deleteSave(): #Deletes a file.
    try:
        global is_in_prompt
        global selected_input
        is_in_prompt = True
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

        
        refresh_listbox()

    except IndexError:
        messagebox.showwarning("No Save Selected", "No save file selected. Please select a save file to delete.")
    except Exception as e:
        logging.error(f"An error occurred in deleteSave: {e}")
        messagebox.showerror("Error", f"An error occurred while deleting a save: {e}")

    is_in_prompt = False
    
#####################
# Init scan variables
scan_thread = None
stop_scan = threading.Event()

def scan_folder(selected_profile): #Actively scans save file folders to detect filename changes.
    global stop_scan, dynamic_filename_var
    while not stop_scan.is_set():
        try:
            output_file_path = config['profiles'][selected_profile]['outputfile']
            folder_path, file_name = os.path.split(output_file_path)

            if not os.path.exists(folder_path):
                messagebox.showinfo("Reminder", "Please configure your main save slot before enabling Dynamic Save Slots.")
                stop_scan.set()
                dynamic_filename_var.set(0)
                config['profiles'][selected_profile]['dynamicsaves'] = 0
                write_data()
                continue

            files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
            found_file = find_file_with_numbers(files)

            if found_file:
                file_name = basename(os.path.join(folder_path, found_file))
                saveSlotDir.set(file_name)
                config['profiles'][selected_profile]['outputfile'] = os.path.join(folder_path, found_file)
                write_data()

            if config['profiles'][selected_profile]['secondarystate'] == "normal":
                    output_file_path_secondary = config['profiles'][selected_profile]['outputfilesecondary']
                    folder_path_secondary, file_name_secondary = os.path.split(output_file_path_secondary)
                    if config['profiles'][selected_profile]['outputfilesecondary'] == "Not Assigned" or not os.path.exists(folder_path_secondary):
                        messagebox.showinfo("Reminder", "Please configure your secondary save slot before enabling Dynamic Save Slots.")
                        stop_scan.set()
                        dynamic_filename_var.set(0)
                        config['profiles'][selected_profile]['dynamicsaves'] = 0
                        write_data()
                        continue

                    files_secondary = [f for f in os.listdir(folder_path_secondary) if os.path.isfile(os.path.join(folder_path_secondary, f))]
                    found_file_secondary = find_file_with_numbers(files_secondary)

                    if found_file_secondary:
                        file_name_secondary = basename(os.path.join(folder_path_secondary, found_file_secondary))
                        saveSlot2Dir.set(file_name_secondary)
                        config['profiles'][selected_profile]['outputfilesecondary'] = os.path.join(folder_path_secondary, found_file_secondary)
                        write_data()
                        

        except FileNotFoundError as e:
            logging.error(f"Error in scanning folder: {e}")
            messagebox.showerror("File Not Found", f"Error in scanning folder: {e}")
        
        time.sleep(5)
    

def find_file_with_numbers(files): #Looks for files that contain numbers and excludes container files.
    try:
        filtered_files = [file for file in files if 'container' not in file.lower() and not any(char.isdigit() for char in os.path.splitext(file)[1])]
        for file in filtered_files:
            if any(char.isdigit() for char in file):
                return file
        return None
    except Exception as e:
        logging.error(f"An error occurred in find_file_with_numbers(): {e}")
        messagebox.showwarning ("ERROR", "An Error occurred in find_file_with_numbers(): {e}")
        

def toggle_dynamic_filename():
    try:
        global scan_thread, stop_scan
        if dynamic_filename_var.get() == 1:
            confirmation = messagebox.askyesno("Confirm", "Dynamic Filename only works for games with saves that are renamed when overwritten. Are you sure you want to enable this feature?")
            if confirmation:
                config['profiles'][selected_profile]['dynamicsaves'] = 1
                stop_scan.clear()
                scan_thread = threading.Thread(target=scan_folder, args=(selected_profile,))
                scan_thread.daemon = True
                scan_thread.start()
            else:
                dynamic_filename_var.set(0)
        elif dynamic_filename_var.get() == 0:
            config['profiles'][selected_profile]['dynamicsaves'] = 0
            if scan_thread:
                dynamic_filename_var.set(0)
                message_box = messagebox.showinfo("Dynamic Filename Disabled", "Dynamic filename detection is disabled. There will be one final scan after you click OK. After that you will be able to resume using the software.")
                stop_scan.set()
                scan_thread.join()          
        write_data()
    except Exception as e:
        logging.error(f"An error occurred in toggle_dynamic_filename(): {e}")
        messagebox.showwarning ("ERROR", "An Error occurred in toggle_dynamic_filename(): {e}")
        

def on_checkbox_change(): #Toggles the Secondary Save Slot Button
    try:
        if secondary_save_enabled.get() == 1:
            config['profiles'][selected_profile]['secondarystate'] = "normal"
            saveSlot2DirLabel.config(state=NORMAL)
            saveSlot2Button.config(state=NORMAL)
        else:
            config['profiles'][selected_profile]['secondarystate'] = "disabled"
            saveSlot2DirLabel.config(state=DISABLED)
            saveSlot2Button.config(state=DISABLED)

        write_data()
    except Exception as e:
        logging.error(f"An error occurred in on_checkbox_change(): {e}")
        messagebox.showwarning ("ERROR", "An Error occurred in on_checkbox_change(): {e}")
        

def update_profile_dropdown(): #Updates the profile dropdown window
    try:
        profiles = list(config['profiles'].keys())
        profileDropdown['values'] = profiles
    except Exception as e:
        logging.error(f"An error occurred in update_profile_dropdown(): {e}")
        messagebox.showwarning ("ERROR", "An Error occurred in update_profile_dropdown(): {e}")
        
    
def adjust_wraplength(event, *labels): #Automatically adjusts wraplength of GUI when window is resized.
    try:
        new_width = event.width
        new_wraplength = min(new_width - 10, 1000)
        for label in labels:
            label.config(wraplength=new_wraplength)
    except Exception as e:
        logging.error(f"An error occurred in adjust_wraplength(): {e}")
        messagebox.showwarning ("ERROR", "An Error occurred in adjust_wraplength(): {e}")


def get_closest_folder(directory): #Consolidates full directories down to the closest (most childish) folder.
    try:
        closest_folder = '/' + os.path.basename(os.path.normpath(directory)) + '/'
        return closest_folder
    except Exception as e:
        logging.error(f"An error occurred in get_closest_folder(): {e}")
        messagebox.showwarning ("ERROR", "An Error occurred in get_closest_folder(): {e}")
    

def on_close(): #Handles closing the program.
    try:
        global stop_scan
        stop_scan.set()
        width = root.winfo_width()
        height = root.winfo_height()
        config['window_size'] = {"width": width, "height": height}
        update_config(config, default_config)
        root.destroy()
    except Exception as e:
        logging.error(f"An error occurred in on_close(): {e}")
        messagebox.showwarning ("ERROR", "An Error occurred in on_close(): {e}")
    

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
import_button = Button(main_frame, text="Import", command=import_files)
import_button.grid(row=1, column=0, sticky=E, pady=5, padx=5)
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
main_frame.bind("<Configure>", lambda event: adjust_wraplength(event, loadSaveDirLabel, saveSlotDirLabel, saveSlot2DirLabel))
root.protocol("WM_DELETE_WINDOW", on_close)
#Load and select the profile.
select_profile(None)
#Mainloop
root.mainloop()
