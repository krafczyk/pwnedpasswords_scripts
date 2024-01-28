import argparse
import getpass
import hashlib
import gc
import os
import tqdm


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hash a password using SHA-1, and check a database")
    parser.add_argument("--db", help="Database file", required=True, type=str)
    args = parser.parse_args()

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

    the_hash = format_hash(hash1)
    
    num = check_database(the_hash, args.db)
    if num is not None:
        print(f"Password found in database, {num} occurances.")
    else:
        print("Password not found in database")
