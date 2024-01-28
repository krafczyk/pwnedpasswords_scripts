import argparse
import getpass
import hashlib
import gc
import os
import tqdm
import ctypes
import sys
import signal


# Global flag to indicate interrupt
interrupted = False

@ctypes.CFUNCTYPE(ctypes.c_bool)
def is_interrupted():
    global interupted
    return ctypes.c_bool(interrupted)

# Function to input password and return SHA-1 hash
def hash_password(prompt):
    # Input password without echoing
    password = getpass.getpass(prompt=prompt)
    # Calculate SHA-1 hash
    password_hash = hashlib.sha1(password.encode()).hexdigest()
    # Clear password from memory
    del password
    gc.collect()
    return password_hash


def format_hash(hash_str):
    # Convert to uppercase
    formatted_hash = hash_str.upper()
    # Pad with zeros on the left to make the length 40 characters
    formatted_hash = formatted_hash.zfill(40)
    return formatted_hash


def check_database(hash_to_check, db_path):
    with open(db_path, 'r') as file:
        # Get the size of the file for the progress bar
        total_size = os.path.getsize(db_path)

        # Initialize the progress bar
        progress_bar = tqdm.tqdm(total=total_size, unit='B', unit_scale=True, desc="Checking database", leave=False)
        for line in file:
            hash, num = line.strip().split(':')
            if hash == hash_to_check:
                progress_bar.close()
                return num
            # Update the progress bar with the length of the line
            progress_bar.update(len(line))

        progress_bar.close()
    return None


def interrupt_handler(*args,**kwargs):
    print(f"In interrupt handler, args={args}, kwargs={kwargs}")
    sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hash a password using SHA-1, and check a database")
    parser.add_argument("--db", help="Database file", required=True, type=str)
    args = parser.parse_args()

    # Register the interrupt handler
    signal.signal(signal.SIGINT, interrupt_handler)
    signal.signal(signal.SIGTERM, interrupt_handler)

    if not os.path.exists(args.db):
        raise FileNotFoundError(f"Database file {args.db} does not exist")

    # Input password and hash it
    hash1 = hash_password("Enter password: ")

    # Input password again and hash it
    hash2 = hash_password("Re-enter password: ")

    # Compare hashes and print if they match
    if hash1 != hash2:
        raise ValueError("Passwords do not match.")

    print(f"Password SHA-1 Hash: {hash1}")

    # Load the C++ shared library
    search_lib = ctypes.CDLL("./search_hash.so")
    search_lib.search_hash.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    search_lib.search_hash.restype = ctypes.c_int

    # Call the C++ function with the callback for progress update
    # Format the hash
    the_hash = format_hash(hash1).encode()
    db_path = args.db.encode()
    num = search_lib.search_hash(db_path, the_hash)

    # Turn num into a python integer.
    num = int(num)

    if num >= 0:
        print(f"Password found in database, {num} occurances.")
    else:
        print(f"Password not found in database ({num})")
