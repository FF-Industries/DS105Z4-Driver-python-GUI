import socket  # Import the socket module for network communication
import tqdm    # Import tqdm for progress bars
import os      # Import os for filesystem operations
import tkinter as tk  # Import tkinter for GUI
from tkinter import filedialog  # Import specific functions for file dialogs
import threading  # Import threading for managing multiple threads

# Define constants
SEPARATOR = "<SEPARATOR>"  # Separator for splitting data in messages
BUFFER_SIZE = 4096  # Size of data chunks for sending and receiving

# Define the GUI application class
class FileTransferApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("500x400")
        self.root.configure(bg="pink")
        self.root.title("Oscilloscope File Transfer")

        # Create a label to display information
        self.info_label = tk.Label(self.root, text="Choose Source File and Destination", font=("Helvetica", 11, "bold"),
                                   width=83, height=3, bg="#B2EBF2", relief="solid",
                                   highlightthickness=4, highlightbackground="#37d3ff")
        self.info_label.pack(pady=20)

        # Create a button to start the server and client threads
        self.server_client_button = tk.Button(self.root, text="Transfer File", font=("Helvetica", 14),
                                              command=self.start_server_client_thread, bg='#FFD700', fg='black',
                                              width=25, height=2)
        self.server_client_button.pack(pady=10)

        # Create a button to choose the source file
        self.choose_save_location_button = tk.Button(self.root, text="Source File", font=("Helvetica", 14),
                                                     command=self.choose_file_to_transfer, bg='#FFD700', fg='black',
                                                     width=25, height=2)
        self.choose_save_location_button.pack(pady=10)
        
        # Create a button to choose the destination folder
        self.choose_file_button = tk.Button(self.root, text="Destination Folder", font=("Helvetica", 14),
                                            command=self.choose_save_location, bg='#FFD700', fg='black',
                                            width=25, height=2)
        self.choose_file_button.pack(pady=10)
        
        # Initialize variables to store chosen paths
        self.file_location = None
        self.destination_location = None

    # Method to choose the destination folder
    def choose_save_location(self):
        chosen_dir = filedialog.askdirectory(title="Select Destination Folder")
        if chosen_dir:
            self.destination_location = chosen_dir
            self.update_info_label()

    # Method to choose the source file
    def choose_file_to_transfer(self):
        chosen_file = filedialog.askopenfilename(initialdir=os.path.dirname(__file__), title="Select Source File to Transfer")
        if chosen_file:
            self.file_location = chosen_file
            self.update_info_label()

    # Method to update the information label
    def update_info_label(self):
        if self.file_location and self.destination_location:
            self.info_label.config(text=f"Source File: {os.path.basename(self.file_location)}\nDestination: {os.path.basename(self.destination_location)}")
        elif self.file_location:
            self.info_label.config(text=f"Source File: {os.path.basename(self.file_location)}\nDestination: Not chosen")
        elif self.destination_location:
            self.info_label.config(text=f"Source File: Not chosen\nDestination: {os.path.basename(self.destination_location)}")
        else:
            self.info_label.config(text="Choose Source File and Destination")

    # Method to start the server and client threads
    def start_server_client_thread(self):
        if not self.file_location or not self.destination_location:
            self.info_label.config(text="No file was chosen.")
            return
        server_client_thread = threading.Thread(target=self.start_server_client)
        server_client_thread.start()

    # Method to start the server and client processes
    def start_server_client(self):
        self.info_label.config(text="Data ready...")
        self.start_server()
        self.start_client()
        self.info_label.config(text="Transferred!")

    # Method to start the server process
    def start_server(self):
        SERVER_HOST = "127.0.0.1"  # Server IP address
        SERVER_PORT = 5001  # Server port

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object

        try:
            s.bind((SERVER_HOST, SERVER_PORT))  # Bind the socket to the host and port
            s.listen(5)  # Listen for incoming connections
            print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

            client_socket, address = s.accept()  # Accept a client connection
            print(f"[+] {address} is connected.")

            received = client_socket.recv(BUFFER_SIZE).decode()  # Receive the file information
            filename, filesize = received.split(SEPARATOR)
            filename = os.path.basename(filename)
            filesize = int(filesize)

            save_path = os.path.join(self.destination_location, filename)  # Path to save the received file

            # Create a progress bar for receiving the file
            progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
            with open(save_path, "wb") as f:
                while True:
                    bytes_read = client_socket.recv(BUFFER_SIZE)
                    if not bytes_read:
                        break
                    f.write(bytes_read)
                    progress.update(len(bytes_read))

            client_socket.close()  # Close the client socket
            print(f"[+] File saved to: {save_path}")
        except Exception as e:
            print(f"[-] Error: {str(e)}")
        finally:
            s.close()  # Close the server socket

    # Method to start the client process
    def start_client(self):
        host = "127.0.0.1"  # Server IP address
        port = 5001  # Server port

        file_location = getattr(self, "file_location", None)  # Get the chosen file location
        
        if not file_location:
            print("Please choose a file to transfer.")
            return

        filesize = os.path.getsize(file_location)  # Get the size of the chosen file

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object

        try:
            s.connect((host, port))  # Connect to the server

            # Send the file information to the server
            s.send(f"{os.path.basename(file_location)}{SEPARATOR}{filesize}".encode())

            # Create a progress bar for sending the file
            progress = tqdm.tqdm(range(filesize), f"Sending {file_location}", unit="B", unit_scale=True, unit_divisor=1024)
            with open(file_location, "rb") as f:
                while True:
                    bytes_read = f.read(BUFFER_SIZE)
                    if not bytes_read:
                        break
                    s.sendall(bytes_read)
                    progress.update(len(bytes_read))
            print("[+] File sent successfully.")
        except Exception as e:
            print(f"[-] Error: {str(e)}")
        finally:
            s.close()  # Close the client socket

# Main entry point
if __name__ == "__main__":
    # Create the main GUI window
    root = tk.Tk()
    # Initialize the FileTransferApp class
    app = FileTransferApp(root)
    # Start the GUI event loop
    root.mainloop()
