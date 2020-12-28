def create_log_file(path: str) -> None:
    open(path, "a").close()


def write_log_file(path: str, log: str) -> None:
    with open(path, "a") as log_file:
        log_file.write(f"{log}\n")
