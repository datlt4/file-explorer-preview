import os

def read_db(filename="quickaccess.txt"):
    with open(filename, "r", encoding="utf-8") as fr:
        # Read the contents of the file into a list of lines
        lines = []
        for line in fr.read().strip().split("\n"):
            if os.path.isfile(line):
                lines.append(os.path.dirname(line.replace("\\", "/")))
            elif os.path.isdir(line):
                lines.append(line.replace("\\", "/"))
            else:
                pass

    return lines

def write_db(quick_access, filename="quickaccess.txt"):
    with open(filename, "w", encoding="utf-8") as fw:
        # Read the contents of the file into a list of lines
        fw.write("\n".join(quick_access))

if __name__ == "__main__":
    print(read_db())
