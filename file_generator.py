from faker import Faker
import threading
import multiprocessing
import sys
import time

def generate_text_file(file_name, word_count):
    """Generate a text file with a specified number of words using Faker."""
    fake = Faker()
    text_content = ' '.join(fake.word() for _ in range(word_count))
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(text_content)
    print(f"File '{file_name}' has been generated with {word_count} words.")

def thread_function(file_index, word_count):
    """Function to be executed in a thread for generating a single file."""
    filename = f"output_thread_{file_index}.txt"
    generate_text_file(filename, word_count)

def process_function(file_index, word_count):
    """Function to be executed in a process for generating a single file."""
    filename = f"output_process_{file_index}.txt"
    generate_text_file(filename, word_count)

def sequential_function(file_index, word_count):
    """Function to generate a single file without threading or multiprocessing."""
    filename = f"output_sequential_{file_index}.txt"
    generate_text_file(filename, word_count)

def main(num_files, num_words, method):
    start_time = time.time()  # Start timing here
    if method == 'threading':
        threads = []
        for i in range(num_files):
            t = threading.Thread(target=thread_function, args=(i, num_words))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
    elif method == 'multiprocessing':
        processes = []
        for i in range(num_files):
            p = multiprocessing.Process(target=process_function, args=(i, num_words))
            processes.append(p)
            p.start()
        for p in processes:
            p.join()
    elif method == 'sequential':
        for i in range(num_files):
            sequential_function(i, num_words)

    elapsed_time = time.time() - start_time  # Calculate the elapsed time
    print(f"All {num_files} files have been generated each with {num_words} words.")
    print(f"Total time taken: {elapsed_time:.2f} seconds using {method}.")

if __name__ == "__main__":
    print("Welcome to the file generator tool!")
    num_files = int(input("How many files would you like to generate? "))
    num_words = int(input("How many words per file? "))
    method = input("Choose method (threading/multiprocessing/sequential): ").strip().lower()
    if method not in ['threading', 'multiprocessing', 'sequential']:
        print("Invalid method. Please choose 'threading', 'multiprocessing', or 'sequential'.")
    else:
        main(num_files, num_words, method)
