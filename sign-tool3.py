import subprocess
import sys
import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QFileDialog, QVBoxLayout,
    QLabel, QLineEdit, QHBoxLayout, QTextEdit, QMessageBox, QCheckBox
)
from PySide6.QtGui import QIcon

class SignTool(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Macan Sign Tool v2.2 (Batch Mode Ready)")
        self.setFixedSize(550, 500)  # Slightly taller to accommodate the checkbox
        icon_path = "sign.ico"
        if hasattr(sys, "_MEIPASS"):
            icon_path = os.path.join(sys._MEIPASS, icon_path)
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # --- CHANGE 1: Automatic signtool.exe Path ---
        # Determine signtool.exe path based on whether the script is run as a .py file or a PyInstaller build
        if hasattr(sys, '_MEIPASS'):
            # Running as a bundled executable (PyInstaller result)
            base_path = sys._MEIPASS
        else:
            # Running as a regular .py script
            base_path = os.path.abspath(".")
        
        self.signtool_executable_path = os.path.join(base_path, 'signtool.exe')
        # Stores the list of files to be signed
        self.target_files_list = []

        # --- Main Layout ---
        main_layout = QVBoxLayout()

        # --- Widget for signtool.exe Path REMOVED ---
        # No longer needed as the path is automatic

        # --- Widget for File Path to be signed ---
        self.file_label = QLabel("Select file(s) to sign (.exe/.dll):")
        self.file_path = QLineEdit()
        self.file_path.setPlaceholderText("Select one or more files...")
        self.file_path.setReadOnly(True) # Made read-only so the user cannot type manually
        self.file_browse_btn = QPushButton("Browse")
        file_layout = QHBoxLayout()
        file_layout.addWidget(self.file_path)
        file_layout.addWidget(self.file_browse_btn)

        # --- CHANGE 2: Added Checkbox for Batch Mode ---
        self.batch_mode_checkbox = QCheckBox("Sign multiple files at once (Batch Mode)")

        # --- Widget for Certificate Path (.pfx) ---
        self.cert_label = QLabel("Path to certificate file (.pfx):")
        self.cert_path = QLineEdit()
        self.cert_browse_btn = QPushButton("Browse")
        cert_layout = QHBoxLayout()
        cert_layout.addWidget(self.cert_path)
        cert_layout.addWidget(self.cert_browse_btn)

        # --- Widget for Certificate Password ---
        self.password_label = QLabel("Certificate password (leave blank if none):")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # --- Button to Run Process ---
        self.sign_btn = QPushButton("Start Signing")
        self.sign_btn.setStyleSheet("font-weight: bold; padding: 5px;")

        # --- Text Area for Log/Output ---
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setPlaceholderText("Output from signtool will appear here...")

        # --- Adding all widgets to the main layout ---
        main_layout.addWidget(self.file_label)
        main_layout.addLayout(file_layout)
        main_layout.addWidget(self.batch_mode_checkbox) # Checkbox added to the layout
        main_layout.addSpacing(10)
        main_layout.addWidget(self.cert_label)
        main_layout.addLayout(cert_layout)
        main_layout.addWidget(self.password_label)
        main_layout.addWidget(self.password_input)
        main_layout.addSpacing(15)
        main_layout.addWidget(self.sign_btn)
        main_layout.addWidget(QLabel("Log:"))
        main_layout.addWidget(self.log_output)
        
        self.setLayout(main_layout)

        # --- Connecting buttons to functions ---
        self.file_browse_btn.clicked.connect(self.browse_target_files) # Function changed
        self.cert_browse_btn.clicked.connect(self.browse_cert_file)
        self.sign_btn.clicked.connect(self.run_sign)
        # Remove connection for signtool browse button
            
    def browse_target_files(self):
        # --- CHANGE 3: File Browse Logic Updated for Batch Mode ---
        self.target_files_list = [] # Clear the list every time browse is clicked
        
        if self.batch_mode_checkbox.isChecked():
            # If batch mode is active, use getOpenFileNames (plural)
            paths, _ = QFileDialog.getOpenFileNames(self, "Select Target Files (Multiple files allowed)", "", "Windows Executable (*.exe *.dll)")
            if paths:
                self.target_files_list = paths
                self.file_path.setText(f"{len(paths)} file(s) selected.")
        else:
            # If batch mode is not active, use getOpenFileName (single)
            path, _ = QFileDialog.getOpenFileName(self, "Select Target File", "", "Windows Executable (*.exe *.dll)")
            if path:
                self.target_files_list.append(path)
                self.file_path.setText(path)
            
    def browse_cert_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Certificate File", "", "Certificate File (*.pfx)")
        if path:
            self.cert_path.setText(path)

    def run_sign(self):
        # --- CHANGE 4: Signing Logic Updated for Batch Mode ---
        signtool = self.signtool_executable_path
        cert = self.cert_path.text()
        password = self.password_input.text()

        # Input validation: ensure target file(s) and certificate are selected
        if not self.target_files_list or not cert:
            QMessageBox.warning(self, "Input Incomplete", "Please select target file(s) and a certificate file first.")
            return

        self.log_output.clear()
        self.sign_btn.setEnabled(False)
        self.log_output.append("Starting signing process...")
        QApplication.processEvents()

        success_count = 0
        failure_count = 0

        # Loop for each file in the target list
        for i, target_file in enumerate(self.target_files_list):
            self.log_output.append("\n" + "="*50)
            self.log_output.append(f"({i+1}/{len(self.target_files_list)}) Processing file: {os.path.basename(target_file)}")
            self.log_output.append("="*50)
            QApplication.processEvents()

            # Build base command
            cmd = [
                signtool, "sign", 
                "/f", cert,
            ]
            
            # Add password only if provided
            if password:
                cmd.extend(["/p", password])
            
            # Continue with the rest of the command
            cmd.extend([
                "/fd", "SHA256", 
                "/tr", "http://timestamp.digicert.com",
                "/td", "SHA256", 
                "/v", target_file
            ])
            
            try:
                # Check if signtool.exe actually exists before running
                if not os.path.exists(signtool):
                    raise FileNotFoundError

                process = subprocess.run(
                    cmd, 
                    capture_output=True, 
                    text=True, 
                    check=False,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )

                if process.stdout:
                    self.log_output.append("\n--- OUTPUT ---")
                    self.log_output.append(process.stdout)
                if process.stderr:
                    self.log_output.append("\n--- ERROR ---")
                    self.log_output.append(process.stderr)
                
                if process.returncode == 0:
                    self.log_output.append(f">>> SUCCESSFULLY signed: {os.path.basename(target_file)}")
                    success_count += 1
                else:
                    self.log_output.append(f">>> FAILED to sign: {os.path.basename(target_file)} (Error Code: {process.returncode})")
                    failure_count += 1

            except FileNotFoundError:
                error_msg = f"Error: '{signtool}' not found. Make sure signtool.exe is in the same directory as this application."
                self.log_output.append(error_msg)
                QMessageBox.critical(self, "File Not Found", error_msg)
                self.sign_btn.setEnabled(True)
                return # Stop the process if signtool.exe is missing
            except Exception as e:
                self.log_output.append(f"\nAn unexpected error occurred with file {os.path.basename(target_file)}: {str(e)}")
                failure_count += 1
        
        # Summary message after all processes are complete
        self.log_output.append("\n" + "#"*50)
        self.log_output.append(f"PROCESS COMPLETE | Success: {success_count} | Failed: {failure_count}")
        self.log_output.append("#"*50)
        QMessageBox.information(self, "Process Complete", f"Signing process finished.\n\nSuccessful: {success_count} file(s)\nFailed: {failure_count} file(s)")

        self.sign_btn.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = SignTool()
    viewer.show()
    sys.exit(app.exec())