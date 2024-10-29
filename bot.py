import argparse
import json
import os
import time
from deep_translator import GoogleTranslator
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import re

console = Console()

def display_welcome():
    banner = r"""
  _____________
 / ___/ __/ __/
/ (_ /\ \_\ \  
\___/___/___/  
    """
    banner_text = Text(banner, justify="center")
    console.print(banner_text, style="bold cyan")
    time.sleep(1)

def clean_text(text):
    return text.replace("\u200b", "").strip() if text else text

def extract_translatable_text(text):
    return re.split(r'(\\[A-Za-z]+\[\d+\])', text)

def translate_sentence(text, dst='en', log_file=None):
    if not text or not text.strip():
        return ""

    text = clean_text(text).replace("\n", "##NEWLINE##")
    parts = extract_translatable_text(text)
    translated_parts = []

    for part in parts:
        if re.match(r'(\\[A-Za-z]+\[\d+\])', part):
            translated_parts.append(part)
        else:
            if part.strip():
                try:
                    translation = GoogleTranslator(source='auto', target=dst).translate(part)
                    if log_file:
                        log_file.write(f"[LOG - {part}] translate: {part} ->> {translation}\n")
                    translated_parts.append(translation if translation else "")
                except Exception as e:
                    console.print(f"[red]Error translating part: '{part}'. Error: {e}[/red]")
                    translated_parts.append(part)
            else:
                translated_parts.append("")

    return ''.join(translated_parts).replace("##NEWLINE##", "\n")

def translate_file(file_path, dst='en', log_file=None):
    with open(file_path, 'r', encoding='utf-8-sig') as datafile:
        data = json.load(datafile)

    translated_strings = 0
    total_strings = sum(1 for item in data if isinstance(item, dict) and 'list' in item)

    start_time = time.time()
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict) and 'list' in item:
                for command in item['list']:
                    if command['code'] == 401 and command['parameters']:
                        original_text = command['parameters'][0]
                        command['parameters'][0] = translate_sentence(original_text, dst, log_file)
                        translated_strings += 1
                        elapsed_time = time.time() - start_time  # Время, прошедшее с начала обработки
                        console.print(f"[green]{file_path}: {translated_strings} translated | Time: {elapsed_time:.2f}s[/green]", end='\r')

    return data, translated_strings, total_strings

def main(input_folder, dst_lang):
    display_welcome()

    translated_files = 0
    total_translated_strings = 0
    total_all_strings = 0
    dest_folder = f"{input_folder}_{dst_lang}"

    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    files = [f for f in os.listdir(input_folder) if f.endswith('.json')]
    total_files = len(files)

    with open('log.txt', 'w', encoding='utf-8') as log_file:
        for file in files:
            file_path = os.path.join(input_folder, file)
            start_time = time.time()

            translated_data, translated_strings, file_total_strings = translate_file(file_path, dst=dst_lang, log_file=log_file)

            total_translated_strings += translated_strings
            total_all_strings += file_total_strings

            end_time = time.time()
            time_taken = end_time - start_time

            new_file = os.path.join(dest_folder, file)
            with open(new_file, 'w', encoding='utf-8') as f:
                json.dump(translated_data, f, indent=4, ensure_ascii=False)

            translated_files += 1

            console.print(f"[green]Processed: {file} | Time: {time_taken:.2f}s | Translated: {translated_strings}/{file_total_strings} strings[/green]")

    console.print(Panel(f"[cyan]Translation complete![/cyan]\nFiles: {translated_files}, Total Strings Translated: {total_translated_strings}/{total_all_strings}"), style="bold magenta")

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description="[GS] RPG Maker Translator")
    ap.add_argument("-t", "-translate", type=str, required=True, help="Destination language (e.g. 'ru')")
    args = ap.parse_args()

    main(input_folder="dialogs", dst_lang=args.t)
