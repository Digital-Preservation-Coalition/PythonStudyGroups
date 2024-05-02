from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QCheckBox, QDialog, QFrame, QFormLayout, QMainWindow, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QCheckBox, QHBoxLayout, QProgressBar, QVBoxLayout, QFileDialog, QMessageBox, QLineEdit, QGroupBox, QGridLayout, QTreeView, QFileSystemModel, QAction, QMenu
from PyQt5.QtGui import QIcon, QTextCursor, QFont
import subprocess
import sys
import psutil
import os
# import threading

# QRegisterMetaType(QTextCursor)

def set_font(widget, point_size, font_family):
    font = QFont()
    font.setPointSize(point_size)
    font.setFamily(font_family)
    widget.setFont(font)


class DeselectDialog(QDialog):
    def __init__(self, drives, directories, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Deselect Items")
        
        self.selected_drives = drives
        self.selected_directories = directories
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Add checkboxes for drives
        drive_group = QGroupBox("Drives")
        drive_layout = QVBoxLayout()
        drive_group.setLayout(drive_layout)
        self.drive_checkboxes = []
        for drive in self.selected_drives:
            checkbox = QCheckBox(drive)
            drive_layout.addWidget(checkbox)
            self.drive_checkboxes.append(checkbox)
            set_font(checkbox, 12, "Times New Roman")
        layout.addWidget(drive_group)
        
        # Add checkboxes for directories
        
        directory_group = QGroupBox("Directories")
        directory_layout = QVBoxLayout()
        directory_group.setLayout(directory_layout)
        self.directory_checkboxes = []
        for directory in self.selected_directories:
            checkbox = QCheckBox(directory)
            directory_layout.addWidget(checkbox)
            self.directory_checkboxes.append(checkbox)
            set_font(checkbox, 12, "Times New Roman")
        layout.addWidget(directory_group)

        # Add OK button
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

    def get_selected_items(self):
        selected_drives = [checkbox.text() for checkbox in self.drive_checkboxes if checkbox.isChecked()]
        selected_directories = [checkbox.text() for checkbox in self.directory_checkboxes if checkbox.isChecked()]
        return selected_drives, selected_directories
    
    
class DirOutputApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.output_directory = ""
        self.preserve_output_directory_var = False
        
        self.selected_drives = set()
        self.selected_directories = set()
        
        self.media_count_dir = set()
        self.media_count_drive = set()
        
        #Replace 
        self.selected_directories_media_no = []
        self.selected_drives_media_no = []
        
        self.media_numbers_drives = set()
        self.media_numbers_directories = set()
        
        #dictionaries for drive and directories output naming
        self.selected_drives_dict = {}
        self.selected_directories_dict = {}
        
        self.init_ui()
        
        self.create_menu()

    def init_ui(self):
        font_size = 9
        font_family = "Times New Roman"
        
        ## Label of the window/program
        self.setWindowTitle("Born-Digital Processing Application") 
        self.setFont(QFont(font_family, font_size))
        self.setGeometry(100, 100, 900, 600)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.deselect_directory_button = QPushButton("Deselect Directory/Drive")
        self.deselect_directory_button.setFont(QFont(font_family, font_size))
        self.deselect_directory_button.clicked.connect(self.deselect_items)
        # set_font(self.deselect_directory_button, font_size, font_family)
        # Create the main layout
        main_layout = QHBoxLayout()
        self.central_widget.setLayout(main_layout)
        self.central_widget.setFont(QFont(font_family, font_size))

        # Create the layout for the left section
        left_layout = QVBoxLayout()
       
        
        
        # Create the Selected Items widget and Window
        # Selected items text window
        self.selected_drives_widget = QWidget() 
        self.selected_drives_layout = QVBoxLayout()
        self.selected_drives_widget.setLayout(self.selected_drives_layout)    
        self.selected_drives_label = QLabel("<b>Selected Drives:</b>")
        self.selected_drives_text = QTextEdit()
    
        
        # Create the Selected Items widget and Window
        # Selected items text window
        self.selected_directories_widget = QWidget()
        self.selected_directories_layout = QVBoxLayout()
        self.selected_directories_widget.setLayout(self.selected_directories_layout)
        self.selected_directories_label = QLabel("<b>Selected Directory Items:</b>")
        self.selected_directories_text = QTextEdit()

        
        ## Deselect button
        self.deselect_selected_items_button = QPushButton("Deselect Selected Items")
        self.deselect_selected_items_button.clicked.connect(self.deselect_selected_items)
        self.selected_drives_layout.addWidget(self.selected_drives_label)
        self.selected_drives_layout.addWidget(self.selected_drives_text)
        
        # self.selected_items_layout.addWidget(self.deselect_selected_items_button)

        # Add the Selected Items widget to the left layout
        left_layout.addWidget(self.selected_drives_widget)
        self.selected_directories_layout.addWidget(self.selected_directories_label)
        self.selected_directories_layout.addWidget(self.selected_directories_text)  # Add QTextEdit widget here
        left_layout.addWidget(self.selected_directories_widget)
        
        left_layout.addWidget(self.deselect_directory_button)
        
        # Create the layout for the right section (current grid layout)
        right_layout = QGridLayout()
        
        # Add the left and right layouts to the main layout
        main_layout.addLayout(right_layout)
        main_layout.addLayout(left_layout)
        
        

        # Add your current widgets to the right layout
        ## Select Directory button--call function
        self.select_directory_button = QPushButton("Select Directory/Drive")
        self.select_directory_button.clicked.connect(self.select_directory)
        
        ##labels that display selected directories and drives
        self.selected_directory_label = QLabel()
        self.selected_drive_label = QLabel()
        
        ##Deselect directory button--call function
        self.deselect_directory_button = QPushButton("Deselect Directory/Drive")
        self.deselect_directory_button.clicked.connect(self.deselect_items)
        
        #bag ID User enter in characters
        ##Header--just a Label
        self.label_file_name = QLabel("<b>Enter the file name (without extension):</b>")
        
        ##User entry for Collection number
        self.label_file_name_collection_no = QLabel("Enter the <b>collection number</b>:")
        self.label_file_name_collection_no.setContentsMargins(20, 0, 0, 0)
        self.entry_file_name_collection_no = QLineEdit()
        self.entry_file_name_collection_no.setStyleSheet("QLineEdit {color: rgba(0, 0, 0, 100); }")
        self.entry_file_name_collection_no.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        ##User entry for registration number
        self.label_file_name_registration_no = QLabel("Enter the <b>registration number</b>:")
        self.label_file_name_registration_no.setContentsMargins(20, 0, 0, 0)
        self.entry_file_name_registration_no = QLineEdit()
        self.entry_file_name_registration_no.setStyleSheet("QLineEdit {color: rgba(0, 0, 0, 100); }")
        self.entry_file_name_registration_no.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.entry_file_name_registration_no.editingFinished.connect(self.validate_registration_number)
        
        ##User entry for media number
        self.label_file_name_media_count_number_label = QLabel("Media Count Number")
        self.label_file_name_media_count_number_label.setContentsMargins(20, 0, 0, 0)
        
        self.label_file_name_media_no_directories = QLabel("<b>Directories</b>:")
        self.label_file_name_media_no_directories.setContentsMargins(30, 0, 0, 0)
        self.entry_file_name_media_no_directories = QLineEdit("")
        self.entry_file_name_media_no_directories.setStyleSheet("QLineEdit {color: rgba(0, 0, 0, 100); }")
        self.entry_file_name_media_no_directories.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.label_file_name_media_no_drives = QLabel("<b>Drives</b>:")
        self.label_file_name_media_no_drives.setContentsMargins(30, 0, 0, 0)
        self.entry_file_name_media_no_drives = QLineEdit("")
        self.entry_file_name_media_no_drives.setStyleSheet("QLineEdit {color: rgba(0, 0, 0, 100); }")
        self.entry_file_name_media_no_drives.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        ##Checkbox to save the path to the selected directory
        self.checkbox_preserve_output = QCheckBox("Preserve Output Directory")
        
        #button to select the output directory
        self.button_select_output_dir = QPushButton("Select Output Directory")
        
        ##button to execute the program
        self.button_run_program = QPushButton("Run")
        
        ##Showing the directory listing output 
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        
        # Layout of the Right side of the GUI
        right_layout.addWidget(self.select_directory_button, 0, 0)
        right_layout.addWidget(self.selected_directory_label, 0, 1)
        # right_layout.addWidget(self.deselect_directory_button, 1, 0)
        right_layout.addWidget(self.selected_drive_label, 1, 1)
        right_layout.addWidget(self.label_file_name, 2, 0)
        
        right_layout.addWidget(self.label_file_name_collection_no, 3, 0)
        right_layout.addWidget(self.entry_file_name_collection_no, 3, 1)
        
        right_layout.addWidget(self.label_file_name_registration_no, 4, 0)
        right_layout.addWidget(self.entry_file_name_registration_no, 4, 1)
        
        right_layout.addWidget(self.label_file_name_media_count_number_label, 5, 0)
        right_layout.addWidget(self.label_file_name_media_no_directories, 6, 0)
        right_layout.addWidget(self.entry_file_name_media_no_directories, 6, 1)
        right_layout.addWidget(self.label_file_name_media_no_drives, 7, 0)
        right_layout.addWidget(self.entry_file_name_media_no_drives, 7, 1)
        
        right_layout.addWidget(self.checkbox_preserve_output, 8, 0, 1, 2)
        right_layout.addWidget(self.button_select_output_dir, 9, 0, 1, 2)
        right_layout.addWidget(self.button_run_program, 10, 0, 1, 2)
        right_layout.addWidget(self.output_text, 11, 0, 1, 2)

        
        ## When run and select output directory buttons are pressed -- calls functions
        self.button_select_output_dir.clicked.connect(self.set_output_dir)
        self.button_run_program.clicked.connect(self.on_run_button_clicked)

        self.run_button_color = "gray"
        
    # Validation of user entered collection, registration, and media numbers
    ## Registration Number validation
    
    def validate_registration_number(self):
        text = self.entry_file_name_registration_no.text()
        if text.isdigit() and len(text) == 5:
            # Continue with the rest of the script
            pass
        else:
        # Show warning message
            QMessageBox.warning(self, "Invalid Registration Number", f"The entered string '{text}' is not a valid registration number.\nIt must be a 5-digit number.")
        
    def create_menu(self):
        # Create a menu bar creating a menu bar
        
        menu_bar = self.menuBar()
        
        # Create a "file" menu
        file_menu = menu_bar.addMenu('File')
        
        # Create a font menu
        font_menu = menu_bar.addMenu("Font")
        

        
        # Create the 'Type' action
        type_action = QAction('Type', self)
        type_action.triggered.connect(self.on_type_selected)
        
        # Action to change font family
        font_family_action = QAction("Change Font Family", self)
        font_family_action.triggered.connect(self.change_font_family)
        font_menu.addAction(font_family_action)
        
        # Action to change font size
        font_size_action = QAction("Change Font Size", self)
        font_size_action.triggered.connect(self.change_font_size)
        font_menu.addAction(font_size_action)
        
        
        # Add the 'Type' action to the 'Font' submenu
        font_menu.addAction(type_action)
        
        # Add the 'Font' submenu to the 'File' menu
        file_menu.addMenu(font_menu)
        
    def on_type_selected(self):
        print('Type selected')
    def change_font_family(self):
        # Implement function to change font family
        pass
    
    def change_font_size(self):
        # Implement function to change font size
        pass
        
    def deselect_selected_items(self):
        # Deselect all selected items
        self.selected_drives.clear()
        self.selected_directories.clear()
        self.update_selected_drives_text()

    # Select Directory section
    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        
        if directory:
            if os.path.ismount(directory):
                if directory not in self.selected_drives:
                    media_numbers_drives_text = self.entry_file_name_media_no_drives.text()
                    self.media_numbers_drives = set(media_numbers_drives_text.split(','))
                    
                    # self.selected_drives.update(directory)
                    self.selected_drives.add(directory)
                    print(f"This is a drive: {self.selected_drives }")
                    self.parse_media_numbers(self.entry_file_name_media_no_directories.text(), self.media_numbers_directories)
                    # self.update_selected_drive_label()
                    self.update_selected_drives_text()
                else:
                    QMessageBox.warning(self, "Warning", "Drive already selected.", QMessageBox.StandardButton.Ok)
            elif os.path.isdir(directory):
                if directory not in self.selected_directories:
                    media_numbers_directories_text = self.entry_file_name_media_no_directories.text()
                    self.media_numbers_directories = set(media_numbers_directories_text.split(','))
                    
                    
                    # self.selected_directories.update(directory)
                    self.selected_directories.add(directory)
                    print(f"This is a directory: {self.selected_directories }")
                    self.parse_media_numbers(self.entry_file_name_media_no_drives.text(), self.media_numbers_drives)
                    # self.update_selected_directories_label()
                    self.update_selected_directories_text()
                else:
                    QMessageBox.warning(self, "Warning", "Directory already selected.", QMessageBox.StandardButton.Ok)
            
    def parse_media_numbers(self, media_numbers_text, target_set):
        media_numbers = media_numbers_text.split(',')
        media_numbers = [num.strip() for num in media_numbers if num.strip()]
        target_set.update(media_numbers)
            

# Function to run when the Select Output button is clicked and the selected is a drive
    def set_output_dir(self):
        self.validate_registration_number
        directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if directory:
            self.output_directory = directory
            print(self.output_directory)
            
# Function to run when the Run button is clicked and the selected is a drive


    def on_run_button_clicked(self):
        if self.run_button_color == "gray" or self.run_button_color == "red":
            self.run_button_color = "green"
            self.button_run_program.setStyleSheet("background-color: gray;")
            if self.selected_drives:
                self.run_drive_command()
            if self.selected_directories:
                self.run_dir_command()
        elif self.run_button_color == "red":
            self.run_button_color = "green"
            self.button_run_program.setStyleSheet("background-color: green;")
            #when run display the files being checked
   
#Run Directory Command--Called when the run button is clicked; Apart of the on_run_button_clicked function      
    def run_dir_command(self):

        media_numbers = self.entry_file_name_media_no_directories.text().split(',')
        media_numbers = list(set(media_numbers))
        collection_no = self.entry_file_name_collection_no.text()
        registration_no = self.entry_file_name_registration_no.text()
        
#NOTEconvert media_no to a list allow single digit, listed series of digits, or a range##
        for selected_directory in self.selected_directories:
            for media_number in media_numbers:
                print(f"this is a test to see if dir comes up: {selected_directory}")
                if os.path.isdir(selected_directory):
                    bat_command = f'dir "{selected_directory}" /a /s /t:w > "{self.output_directory}/{"mss"+collection_no}_{registration_no}_{media_number}_dir.txt"'
                    bat_viewable = f'dir "{selected_directory}" /a /s /t:w'
                else:
                    print(f"Not a valid directory: {selected_directory}")
                try:
                    subprocess.run(bat_command, shell=True, check=True)
                    viewable_cmd = subprocess.run(bat_viewable, shell=True, check=True, stdout=subprocess.PIPE, text=True, encoding='utf-8')
                    self.output_text.append(f"Output for directory {selected_directory}:\n{viewable_cmd.stdout}")
                except subprocess.CalledProcessError as e:
                    self.output_text.append(f"Error for directory {selected_directory}: {e}")
            # Set button color to red after completion of all directories
            self.run_button_color = "red"
            self.button_run_program.setStyleSheet("background-color: red;")
        
    def run_drive_command(self):
        media_numbers = self.entry_file_name_media_no_drives.text().split(',')
        media_numbers = list(set(media_numbers))
        collection_no = self.entry_file_name_collection_no.text()
        registration_no = self.entry_file_name_registration_no.text()
#NOTEconvert media_no to a list allow single digit, listed series of digits, or a range##
        for selected_drive in self.selected_drives:
            for media_number in media_numbers:
                if os.path.ismount(selected_drive):
                    bat_command = f'dir "{selected_drive}" /a /s /t:w > "{self.output_directory}/{"mss"+collection_no}_{registration_no}_{media_number}_dir.txt"'
                    bat_viewable = f'dir "{selected_drive}" /a /s /t:w'
                else:
                    print(f"Not a valid drive entry: {selected_drive}")
                try:
                    subprocess.run(bat_command, shell=True, check=True)
                    viewable_cmd = subprocess.run(bat_viewable, shell=True, check=True, stdout=subprocess.PIPE, text=True)
                    self.output_text.append(f"Output for drive {selected_drive}:\n{viewable_cmd.stdout}")
                except subprocess.CalledProcessError as e:
                    self.output_text.append(f"Error for drive {selected_drive}: {e}")
            # Set button color to red after completion of all directories
            self.run_button_color = "red"
            self.button_run_program.setStyleSheet("background-color: red;")

    def print_media_numbers(self, media_numbers_set):
        print("Media Numbers:")
        for number in media_numbers_set:
            collection_no = self.entry_file_name_collection_no.text()
            registration_no = self.entry_file_name_registration_no.text()
            print(f"{collection_no}_{registration_no}_{number}")

##UPDATE THIS TO MANIPULATE THE TEXT
    # Select Drive section--start        
    def update_selected_drives_text(self):
        #old
        selected_drives_text = "<br>"+"<br>".join(self.selected_drives) + "<br>"+ "<br>"
        self.selected_drives_text.setHtml(f"<b><font color='blue'>Drive Selection:</font></b> <br> <font color='red'>{selected_drives_text}</font>")
        print(f"drives updated_selected_drives_text): {self.print_media_numbers(self.media_numbers_drives)}")
        
        #new
        # selected_drives_text = "<br>"+"<br>".join(self.selected_drives) + "<br>"+ "<br>"
        # self.selected_drives_text.setHtml(f"<b><font color='blue'>Drive Selection:</font></b> <br> <font color='red'>{selected_drives_text}</font>")
        # concatenated_media_numbers = self.get_concatenated_media_numbers(self.entry_file_name_collection_no.text(), self.entry_file_name_registration_no.text(), self.entry_file_name_media_no_drives.text())
        # self.selected_drives_dict[concatenated_media_numbers] = self.selected_drives
        # for drive in self.selected_drives:
        #     print(f"Assigned concatenated number '{concatenated_media_numbers}' to drive '{drive}'.")
        print(f"drives numbers set{self.media_numbers_drives}")
        print(f"drives path set{self.selected_drives }")
        
    
    def update_selected_directories_text(self):
        #Old
        selected_directories_text = "<br>".join(self.selected_directories) + "<br>"+ "<br>"
        print(selected_directories_text)
        self.selected_directories_text.setHtml(f"<lb><b><font color='blue'>Directory Selection</font></b><br>  <font color='red'>{selected_directories_text}</font><lb>")
        print(f"directories (updated_selected_directories_text): {self.print_media_numbers(self.media_numbers_directories)}")
        
        #New
    #     selected_directories_text = "<br>".join(self.selected_directories) + "<br>"+ "<br>"
    #     self.selected_directories_text.setHtml(f"<lb><b><font color='blue'>Directory Selection</font></b><br>  <font color='red'>{selected_directories_text}</font><lb>")
    #     concatenated_media_numbers = self.get_concatenated_media_numbers(self.entry_file_name_collection_no.text(), self.entry_file_name_registration_no.text(), self.entry_file_name_media_no_directories.text())
    #     self.selected_directories_dict[concatenated_media_numbers] = self.selected_directories
    #     for directory in self.selected_directories:
    #         print(f"Assigned concatenated number '{concatenated_media_numbers}' to directory '{directory}'.")
        
    # def get_concatenated_media_numbers(self, collection_no, registration_no, media_numbers):
    #     media_numbers = media_numbers.split(',')
    #     media_numbers = list(set(media_numbers))
    #     concatenated_numbers = '_'.join(['mss'+ collection_no, registration_no] + media_numbers)
        # return concatenated_numbers
        print(f"directories set{self.media_numbers_directories}")
        print(f"drives path set{self.selected_directories_dict}")
        
    def deselect_selected_items(self):
        # Deselect all selected items
        self.selected_drives.clear()
        self.selected_directories.clear()
        self.update_selected_items_text()
        
    def deselect_items(self):
        # Create and display the deselect dialog
        deselect_dialog = DeselectDialog(self.selected_drives, self.selected_directories)
        if deselect_dialog.exec() == QDialog.DialogCode.Accepted:
            # Get selected items from the dialog
            selected_drives, selected_directories = deselect_dialog.get_selected_items()
            
            # Remove selected drives and directories
            for drive in selected_drives:
                self.selected_drives.remove(drive)
            for directory in selected_directories:
                self.selected_directories.remove(directory)
                
        
            # Update displayed lists
            # self.update_selected_drives_label()
            # self.update_selected_directories_label()
            
           # Update the text in the selected items window
            self.update_selected_drives_text()
            self.update_selected_directories_text()

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = DirOutputApp()
    icon_path = os.path.join("images", "US-LibraryOfCongress-Logo.jpg")
    window.setWindowIcon(QIcon(icon_path))
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
