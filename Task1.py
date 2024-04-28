import asyncio
import os
from argparse import ArgumentParser
import shutil
from concurrent.futures import ThreadPoolExecutor
import logging

# Налаштування логера
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

executor = ThreadPoolExecutor(max_workers=4)

async def read_folder(source_path):
    """Асинхронно читає файли з вихідної папки та її підпапок."""
    files = []
    for root, _, filenames in os.walk(source_path):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files

async def copy_file(file_path, output_path):
    """Асинхронно копіює файл в підпапку на основі його розширення."""
    try:
        extension = os.path.splitext(file_path)[1][1:] or "no_extension"
        target_folder = os.path.join(output_path, extension)
        os.makedirs(target_folder, exist_ok=True)
        target_path = os.path.join(target_folder, os.path.basename(file_path))
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(executor, shutil.copy, file_path, target_path)
        logging.info(f"Файл {file_path} скопійовано до {target_path}")
    except Exception as e:
        logging.error(f"Помилка при копіюванні файлу {file_path}: {e}")

async def main(source_path, output_path):
    files = await read_folder(source_path)
    tasks = [copy_file(file, output_path) for file in files]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    parser = ArgumentParser(description="Асинхронне розподілення файлів по підпапках на основі розширень.")
    parser.add_argument("source_path", type=str, help="Шлях до вихідної папки")
    parser.add_argument("output_path", type=str, help="Шлях до цільової папки")
    args = parser.parse_args()

    asyncio.run(main(args.source_path, args.output_path))
