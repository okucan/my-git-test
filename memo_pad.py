def add_memo(memo_text):
  """Appends the given memo_text to the memos.txt file.

  Args:
    memo_text: The string to be added as a memo.
  """
  if not memo_text.strip():
    print("Error: Memo text cannot be empty.")
    return
  try:
    with open("memos.txt", "a") as f:
      f.write(memo_text.strip() + "\n")
  except IOError:
    print("Error: Could not write to memo file.")

def view_memos():
  """Reads and prints all memos from memos.txt.

  If memos.txt doesn't exist or is empty, it prints "No memos found."
  """
  try:
    with open("memos.txt", "r") as f:
      memos = f.readlines()
      if not memos:
        print("No memos found.")
      else:
        for i, memo in enumerate(memos):
          print(f"{i+1}. {memo.strip()}")
  except FileNotFoundError:
    print("No memos found.")
  except IOError:
    print("Error: Could not read memo data.")

def delete_memo(memo_number):
  """Deletes a specific memo from memos.txt based on its 1-indexed number.

  Args:
    memo_number: The 1-indexed number of the memo to delete.
  """
  memos = []
  try:
    with open("memos.txt", "r") as f:
      memos = f.readlines()
  except FileNotFoundError:
    print("No memos to delete.")
    return
  except IOError:
    print("Error: Could not access memo data.")
    return

  if not memos:
    print("No memos to delete.")
    return

  try:
    memo_num_int = int(memo_number)
  except ValueError:
    print("Error: Invalid input. Memo number must be an integer.")
    return

  if not (1 <= memo_num_int <= len(memos)):
    print(f"Error: Invalid memo number. Please enter a number between 1 and {len(memos)}.")
    return

  # Adjust for 0-based indexing
  deleted_memo_content = memos.pop(memo_num_int - 1).strip()

  try:
    with open("memos.txt", "w") as f:
      f.writelines(memos)
    print(f"Memo {memo_num_int} ('{deleted_memo_content}') deleted.")
  except IOError:
    print("Error: Could not save changes to memo file.")
  except Exception as e:
    print(f"An unexpected error occurred: {e}")

def main():
  """Runs the command-line interface for the Memo Pad."""
  while True:
    print("\nMemo Pad")
    print("1. Add memo")
    print("2. View memos")
    print("3. Delete memo")
    print("4. Exit")

    choice = input("Choose an option: ")

    if choice == '1':
      memo_text = input("Enter memo text: ")
      add_memo(memo_text)
    elif choice == '2':
      view_memos()
    elif choice == '3':
      view_memos() # Show memos first so user knows which number to pick
      # Check if there are memos before asking for input
      # This check can be implicit if view_memos indicates no memos,
      # but an explicit check after calling view_memos or by checking memos.txt content might be better.
      # For now, we'll rely on delete_memo to handle "no memos" scenario if user tries to delete.
      memo_number = input("Enter memo number to delete: ")
      delete_memo(memo_number)
    elif choice == '4':
      print("Exiting Memo Pad.")
      break
    else:
      print("Invalid choice. Please try again.")

if __name__ == "__main__":
  main()
