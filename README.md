# Easy Versioning (Sphinx documentation build tool)
  
This tool was created to address the need to add **versioning to a Sphinx** project without relying on Read the Docs (RTD).  
  
This Python script automates the full workflow of **preparing, versioning, building, and organizing documentation from Markdown** files using the Sphinx tool.  

It’s designed for teams and organizations who want to **self-host** their documentation sites and prefer full control over the hosting environment and theme customization.  
Easy Versioning works as an **alternative approach** for managing versioned and multilingual docs, complementing existing Sphinx workflows in a simple way with only one tool.

By organizing your source files in the expected structure, this tool actively builds your documentation with Sphinx and outputs a fully ready-to-deploy static site.  
With minimal setup, it streamlines the process of managing multiple versions and languages, adding consistent footers, and arranging build artifacts for deployment.

---

## Features

Easy Versioning offers the following key features:

-  **Manage multiple documentation versions**
-  **Support multiple languages** for each version
-  **Add custom footers** showing version and language info
-  **Security** by ensuring a safe fallback to an existing page so users are always redirected properly
-  **Build documentation automatically** using Sphinx for every version and language
-  **Organize generated HTML files** into a clean, ready-to-deploy structure

---

## Prerequisites

Make sure you have the following installed on your system:

- Python version >= [3.8](https://www.python.org/downloads/)
- Install the tool using `pip install easy-versioning`

---

## Directory Setup
📦 Easy_versioning_Sphinx/  
├── 📂 data/  
│   └── 📄 Footer.md  
├── 📂 src/  
│   ├── 📁 V. X.XX/  
│   │   ├── 🌐 Language 1/  
│   │   │   └── 📘 Language 1 Sphinx Project/  
│   │   └── 🌐 Language 2/  
│   │       └── 📘 Language 2 Sphinx Project/  
│   ├── 📁 V. Y.YY/  
│   ├── 📁 V. Z.ZZ/  
<br>

You can find a fully working example of a `Footer.md` file in the `Example/data` folder of this project.  
You can start by copying the default file in your `data/` folder and then customize it as you wish by modifying the CSS.  
If you want to create your own `Footer.md` file, please follow the placeholder tags as shown in the example in the folder.

<br>

Inside the `src/` folder, place all your documentation projects you want to build organized according to the directory structure shown above.

<br>

You can find a complete example project in the `Example/` folder, which you can download, build, and use as a setup for your own project!

---

## How to use it

The tool requires the directory structure shown above.  
After opening a terminal in the project’s source directory (which contains the `data/` and `src/` folders), run the command `easy_versioning_build`.

This command can be run without any arguments, or with up to two arguments:

1. **Default language:** The fallback language and the main language of the project (default is "English"). If no arguments are provided, make sure there is an "English" folder in every version of the documentation. Choose a language that exists in **all** versions of your documentation.  
2. **Cleanup flag:** A boolean flag (default is True) that controls whether the `_source` directory is removed from the final build to reduce the project size.  
   - Set this flag to `0` to disable cleanup and keep the `_source` directory.

Examples:  
- `easy_versioning_build` — Uses English as the default language and removes the `_source` directory.  
- `easy_versioning_build Italiano 0` — Sets Italian as the default language and keeps the `_source` directory intact. 

---

##  Why Choose Easy Versioning Over Other Solutions?

| Feature                | Easy Versioning Sphinx | sphinx-multiversion | sphinx-versioning | Read The Docs      |
|------------------------|-----------------------|---------------------|-------------------|-------------------|
| Multi-version          | ✅                    | ✅                  | ✅                | ✅                |
| Multi-language         | ✅                    | ❌                  | ❌                | ✅                |
| Simplified setup       | ✅                    | ⚠️ Complex          | ⚠️ Complex        | ⚠️ Complex        |
| External dependencies  | 🚫 Only Sphinx        | ✅                  | ✅                | ❌                |
| No account required    | ✅                    | ✅                  | ✅                | ❌ (Free for OSS)  |
| Usage cost             | ✅                    | ✅                  | ✅                | Free for OSS, paid plans for private projects |
| Performance consistency| hardware-dependent    | hardware-dependent   | hardware-dependent | Can vary, higher performance require payment          |

---

## Example of the versioning footer using `sphinx_book_theme`
<br>
<img src="https://github.com/user-attachments/assets/36babdf6-bd5d-4c43-86a3-1d65cfaf9f06" width="750" alt="Versioning Example" />

<br>

---

<br><br>

This tool is not a replacement for ReadTheDocs but rather a **complementary free solution** for teams who prefer to host their own documentation or require a different setup.
