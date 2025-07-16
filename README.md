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
-  **Security** by ensuring a safe fallback to an existing page so users are always redirected proprely
-  **Build documentation automatically** using Sphinx for every version and language
-  **Organize generated HTML files** into a clean, ready-to-deploy structure

---

## Prerequisites

Make sure you have the following installed on your system:

- Python version >= [3.8](https://www.python.org/downloads/)
- Install the framework using `pip install easy-versioning`

---

## Folders set-up  
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

## How to use it

The framework needs the folder structure shown above, after opening a terminal in the source folder of the project containing data/ and src/ run the command "easy_versioning_build".   
This command can be run without arguments but can support up to 2 arguments.   
The first one will be the default language, the fallback language for undefined pages. Make sure to choose a language that is in ALL the versions of the documentation.   
The second one is a flag, initialized to True that deletes the "_source" folder from the final build to reduce the project folder size, set the second parameter to 0 to disable cleanup and keep the folder.   
`easy_versioning_build`  
`easy_versioning_build Italiano 0`  <- Main project language Italian and keeping the "_source" folder of the project 

## Why use this?

Easy Versioning offers:
  
✅ A **ready-to-deploy** website, already structured in the output folder  
✅ **Full control** of your hosting and deployment  
✅ **Freedom** to use any Sphinx theme or customization  
✅ **Safe** fallback automatically redirects users to a valid page if their requested version or language is unavailable 
✅ A **simple** and consistent workflow for large, multilingual, versioned docs  

This framework is not a replacement for ReadTheDocs but rather a **complementary free solution** for teams who prefer to host their own documentation or require a different setup.
