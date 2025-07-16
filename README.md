# Easy Versioning (Sphinx documentation build framework)
  
This framework was created to address the need to add **versioning to a Sphinx** project without relying on Read the Docs (RTD).  
  
This Python script automates the full workflow of **preparing, versioning, building, and organizing documentation from Markdown** files using the Sphinx Framework.  

It’s designed for teams and organizations who want to **self-host** their documentation sites and prefer full control over the hosting environment and theme customization.  
Easy Versioning works as an **alternative approach** for managing versioned and multilingual docs, complementing existing Sphinx workflows in a simple way with only one framework.

By organizing your source files in the expected structure, this framework actively builds your documentation with Sphinx and outputs a fully ready-to-deploy static site.  
With minimal setup, it streamlines the process of managing multiple versions and languages, adding consistent footers, and arranging build artifacts for deployment.

---

## Features

This project allows you to:

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
- Install the framework using `pip install easy-versioning`

---

## Directorys set-up  
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
│   ├── 📁 V. Y.YY/  
<br>

You can find a fully working example of a `Footer.md` file in the `Easy_versioning/data` folder of this project.  
You can start by coping the default file in your `data/` folder and then customize it as you wish by modifying the CSS.  
If you want to create your own `Footer.md` file, please follow the placeholder tags as shown in the example in the folder.

<br>

Inside the `src/` folder, place all your documentation projects you want to build organized according to the directory structure shown above.

---

## How to use it

The framework needs the directory structure shown above, after opening a terminal in the source directory of the project containing `data/` and `src/` run the command `easy_versioning_build`.   
This command can be run without arguments but can support up to 2 arguments.   
The first one will be the default language, the fallback language for undefined pages. Make sure to choose a language that is in ALL the versions of the documentation.   
The second one is a flag, initialized to True that removes the `_source` directory from the final build to reduce the project directory size, set the second parameter to 0 to disable cleanup and keep the directory.   
<br>
`easy_versioning_build` <- The main language of the project is English, and the `_source` directory is removed.  
`easy_versioning_build Italiano 0`  <- The main language of the project is Italian, and the `_source` directory is consistently retained.  

---

## Why use this?

Easy Versioning offers:
  
✅ A **ready-to-deploy** website, already structured in the output directory  
✅ **Full control** of your hosting and deployment  
✅ **Freedom** to use any Sphinx theme or customization  
✅ **Safe** fallback automatically redirects users to a valid page if their requested version or language is unavailable   
✅ A **simple** and consistent workflow for large, multilingual, versioned docs  

---

## Example of the versioning footer using `sphinx_book_theme`
<br>
<img src="https://github.com/user-attachments/assets/36babdf6-bd5d-4c43-86a3-1d65cfaf9f06" width="750" alt="Versioning Example" />

---

<br><br>

This framework is not a replacement for ReadTheDocs but rather a **complementary free solution** for teams who prefer to host their own documentation or require a different setup.
