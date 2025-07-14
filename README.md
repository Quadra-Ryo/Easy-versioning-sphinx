# Easy Versioning (Sphinx documentation build tool)
  
This tool was created to address the need for adding versioning to a Sphinx project without relying on Read the Docs (RTD).  
  
This Python script automates the full workflow of preparing, versioning, building, and organizing documentation from Markdown files using the Sphinx Framework.  

It’s designed for teams and organizations who want to **self-host** their documentation sites and prefer full control over the hosting environment and theme customization.  
Easy Versioning works as an **alternative approach** for managing versioned and multilingual docs, complementing existing Sphinx workflows.

By organizing your source files in the expected structure, this tool actively builds your documentation with Sphinx and outputs a fully ready-to-deploy static site.  
With minimal setup, it streamlines the process of managing multiple versions and languages, adding consistent footers, and arranging build artifacts for deployment.

---

## 📖 Features

This project allows you to:

- 🔖 **Manage multiple documentation versions**
- 🌐 **Support multiple languages** for each version
- 📝 **Add custom footers** showing version and language info
- ⚙️ **Build documentation automatically** using Sphinx for every version and language
- 📦 **Organize generated HTML files** into a clean, ready-to-deploy structure

---

## 🚀 Prerequisites

Make sure you have the following installed on your system:

- Python version >= [3.8](https://www.python.org/downloads/)
- Install the required Python libraries using `pip install -r requirements.txt`

---

## 🌲 Folders set-up  
📦 Easy_versioning_Sphinx/  
├── 📂 data/  
│   └── 📄 Footer.md  
├── 📂 project/  
├── 📂 src/  
│   ├── 📁 V. X.XX/  
│   │   ├── 🌐 Language 1/  
│   │   │   └── 📘 Language 1 Sphinx Project/  
│   │   └── 🌐 Language 2/  
│   │       └── 📘 Language 2 Sphinx Project/  
│   ├── 📁 V. Y.YY/  
│   └── 📁 V. Z.ZZ/  
└── 📝 main.py  


## 💡 Why use this?

Easy Versioning offers:
  
✅ A ready-to-deploy website, already structured in the output folder  
✅ Full control of your hosting and deployment  
✅ Freedom to use any Sphinx theme or customization  
✅ A simple and consistent workflow for large, multilingual, versioned docs  

This tool is **not a replacement** for ReadTheDocs but rather a **complementary solution** for teams who prefer to host their own documentation or require a different setup.
