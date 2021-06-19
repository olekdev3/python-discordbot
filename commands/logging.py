def log_command(command):
    file_handler = open("./textfiles/command-log.txt","a")
    file_handler.write(f"{command}\n")
    file_handler.close()