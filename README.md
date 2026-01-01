# 🚀 Shell-Finder PRO

[![Python 3.x](https://img.shields.io/badge/python-3.x-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/exploit1337)

A powerful, multi-threaded admin panel and shell finder tool written in Python 3. Designed for penetration testers and researchers to quickly identify potential entry points.

## ✨ Features

- ⚡ **Multi-Threaded**: Blazing fast scanning with concurrent threads.
- 🎯 **Smart Detection**: Random User-Agents to bypass basic WAF/filters.
- 🎨 **Modern Interface**: Clean, colored CLI output.
- 🛠 **Customizable**: Adjustable thread count and dictionary support.
- 🐍 **Python 3**: Fully modernized codebase.

## 📦 Installation

```bash
git clone https://github.com/exploit1337/Shell-Finder.git
cd Shell-Finder
# No external dependencies required! (Uses standard library)
```

## 🚀 Usage

### Basic Scan

```bash
python3 shellfinder.py -u http://example.com
```

### Advanced Scan

Scan with 50 threads and a custom wordlist:

```bash
python3 shellfinder.py -u http://example.com -t 50 -w my_wordlist.txt
```

### Help Menu

```bash
python3 shellfinder.py --help
```

---

## 📝 GitHub Short Description

> A blazing fast, multi-threaded web shell and admin panel finder written in Python 3. 🚀

## ⚠️ Disclaimer

This tool is for educational purposes and authorized penetration testing only. The author is not responsible for any misuse.

---

**Original Author**: exploit1337
**Updated by**: Community
