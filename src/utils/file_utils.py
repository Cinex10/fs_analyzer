import mmap


def create_mapped_file(filename):
    with open(filename, 'r+b') as f:
        mm = mmap.mmap(f.fileno(), 0)
        return mm