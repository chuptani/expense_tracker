class Stdout(object):
    def __init__(self, *files):
        self.files = files

    def write(self, text):
        for file in self.files:
            file.write(text)
            file.flush()  # Ensure output is written immediately

    def flush(self):
        for file in self.files:
            file.flush()


class Stdin(object):
    def __init__(self, stdin, log_file):
        self.stdin = stdin
        self.log_file = log_file

    def readline(self):
        input_line = self.stdin.readline()
        if input_line:
            self.log_file.write(input_line)
            self.log_file.flush()
        return input_line


# formatted_date_time = self.ctx.now.strftime("%Y-%m-%d_%H:%M:%S")
# file_path = f"logs/{formatted_date_time}.log"
# log_file = open(file_path, "a")
# self.original_stdout = sys.stdout
# self.original_stdin = sys.stdin
# sys.stdout = Stdout(sys.stdout, log_file)
# sys.stdin = Stdin(sys.stdin, log_file)
# sys.stdout = original_stdout
# log_file.close()
