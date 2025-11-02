# Macan Sign Tool

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Release](https://img.shields.io/badge/release-v2.2-brightgreen.svg)
![Platform](https://img.shields.io/badge/platform-Windows-blue)
![Framework](https://img.shields.io/badge/framework-PySide6-cyan)

A professional, enterprise-grade GUI utility for digitally signing Windows executables (.exe, .dll) and libraries using `signtool.exe`. This tool is designed to streamline the code signing process, offering a robust batch mode for signing multiple files in a single, verified operation.

![Macan Sign Tool Screenshot]
<img width="552" height="529" alt="Screenshot 2025-11-02 201019" src="https://github.com/user-attachments/assets/0fc39424-eac3-4cb6-8a09-f6df161f0ff7" />




## Overview

Macan Sign Tool is a front-end for Microsoft's `signtool.exe` designed to simplify and accelerate the release process for software developers and release managers. While `signtool.exe` is a powerful command-line utility, it can be cumbersome for repetitive tasks or for signing large sets of files.

This application provides a clean, user-friendly interface that standardizes the signing process, enforcing best practices like SHA256 digests and trusted timestamping, while also providing a clear log for diagnostics and verification. Its primary feature is a "Batch Mode" that allows for the selection and signing of hundreds of files at once.

## Key Features

* **Batch Mode:** Sign dozens or hundreds of `.exe` and `.dll` files in a single operation.
* **Simple Interface:** A clean, intuitive GUI eliminates the need to remember complex command-line flags.
* **Secure Standards:** Automatically implements `SHA256` for both file (`/fd`) and timestamp (`/td`) digests.
* **Trusted Timestamping:** Enforces the use of a trusted timestamp server (`http://timestamp.digicert.com`) to ensure long-term signature validity, even after the certificate expires.
* **PFX Certificate Support:** Securely sign applications using a `.pfx` certificate file.
* **Password Handling:** Supports password-protected certificates via a secure password-entry field.
* **Real-time Logging:** A built-in log window displays the complete, verbose output from `signtool.exe` for easy diagnostics and success/failure confirmation.
* **Portable & Bundled:** Designed to be bundled with PyInstaller. It automatically locates the included `signtool.exe` relative to its own executable, creating a fully portable tool.

## Requirements

To use this tool, you will need:

1.  A valid `.pfx` code signing certificate.
2.  The password for your `.pfx` certificate (if applicable).


## Installation & Setup (For Compiled Release)

1.  Download the latest compiled release from the [Releases](https://github.com/danx123/signtool/releases) page.
2.  Obtain `signtool.exe` from the Windows SDK.
    * *You can typically find it in a path like: `C:\Program Files (x86)\Windows Kits\10\bin\<version>\x64\signtool.exe`*
3.  Place `signtool.exe` in the **exact same directory** as the `Macan Sign Tool.exe` executable.

Your application directory should look like this:

YourAppDirectory/ ├── Macan Sign Tool.exe ├── signtool.exe └── (other dependency files/folders, if any)

## Usage 1. Launch `Macan Sign Tool.exe`. 2. **Select Target Files:** * **Single File:** Ensure the "Sign multiple files" checkbox is *unchecked*. Click "Browse" and select your `.exe` or `.dll` file. * **Batch Mode:** *Check* the "Sign multiple files at once (Batch Mode)" box. Click "Browse" and select all the `.exe` and `.dll` files you wish to sign in the file dialog. 3. **Select Certificate:** Click "Browse" next to the certificate path field and select your `.pfx` file. 4. **Enter Password:** Type the password for your `.pfx` file. If it has no password, leave this field blank. 5. **Start Signing:** Click the "Start Signing" button. 6. **Monitor Output:** Watch the "Log" window for real-time progress. A summary of successful and failed files will be displayed upon completion. ## Building from Source If you prefer to build the tool from the source code: 1. **Clone the repository:** ```bash git clone [https://github.com/danx123/signtool.git](https://github.com/danx123/signtool.git) cd YOUR_REPO ``` 2. **Create and activate a virtual environment:** ```bash python -m venv venv .\venv\Scripts\activate ``` 3. **Install dependencies:** ```bash pip install PySide6 ``` 4. **Add `signtool.exe`:** Place your copy of `signtool.exe` and your `sign.ico` file in the root of the repository (alongside `sign-tool3.py`). 5. **Run the application:** ```bash python sign-tool3.py ``` 6. **(Optional) Build a Standalone Executable:** Use PyInstaller to bundle the application into a single `.exe`. ```bash pip install pyinstaller # Run from the repository root pyinstaller --onefile --windowed --icon=sign.ico --add-data "signtool.exe;." "sign-tool3.py" -n "MacanSignTool" ``` *Note: The `--add-data` flag bundles `signtool.exe` directly into the package. The syntax uses `;` on Windows and would use `:` on Linux/macOS.* ## License This project is licensed under the MIT License. See the `LICENSE` file for details.
