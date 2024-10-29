# RPG Maker Translator

## Overview
RPG Maker Translator is a Python tool designed for automating the translation of `.json` files in RPG Maker MV, facilitating the localization of game dialogues into various languages.

## Features
- **Automated Translation**: Easily translate game dialogues using Google Translate.
- **Customizable Translations**: Edit `replace.json` for automatic term replacements.
- **Log Output**: Track translation progress and log translated texts.

## Installation

1. **Install Termux** from F-Droid.
2. **Open Termux** and run the following commands:
   ```bash
   termux-setup-storage
   apt-get update
   apt-get upgrade
   pkg install python
   pkg install git
   ```
3. **Create a Folder** (e.g., "rpgmv") in your internal storage.
4. **Navigate to the Folder**:
   ```bash
   cd /storage/emulated/0/rpgmv
   ```
5. **Clone the Repository**:
   ```bash
   git clone https://github.com/Gausstic228/rpg-maker-translator.git
   ```
6. **Install Requirements**:
   ```bash
   cd rpg-maker-translator
   pip install -r requirements.txt
   ```

## Usage

1. **Copy `.json` Files** from your RPG Maker project to `rpg-maker-translator/dialogs`.
2. **Run the Bot**:
   ```bash
   python bot.py -t [language_code]
   ```
   Replace `[language_code]` with your desired target language (e.g., `en` for English).
3. **Output**: Translated files are saved in `dialogs_id/[language_code]`. Ensure these folders are empty before each run.

## Requirements
- **Internet Connection**: Required for translation.
- **Python Version**: Requires Python 3.6 or higher.
