import os
import subprocess

def check_hex(file_path, offset, hex_to_check):
    skip_bytes = offset - 0x101000
    read_bytes = len(hex_to_check) // 2
    command = [
        'od', file_path,
        '--skip-bytes={}'.format(skip_bytes),
        '--read-bytes={}'.format(read_bytes),
        '--endian=little',
        '-t', 'x1',
        '-An'
    ]

    command_output = subprocess.check_output(command).decode().replace(' ', '').strip()
    return command_output == hex_to_check

def patch_hex(file_path, offset, original_hex, new_hex):
    file_offset = offset - 0x101000
    if check_hex(file_path, offset, original_hex):
        hex_in_bin = bytes.fromhex(new_hex)
        with open(file_path, 'r+b') as f:
            f.seek(file_offset)
            f.write(hex_in_bin)
        print(f"Patched {file_path} at {file_offset} with new hex {new_hex}")
    elif check_hex(file_path, offset, new_hex):
        print("Already patched")
    else:
        print("Hex mismatch!")

def patch_ndk_library(ndk_path):
    if os.path.isfile(ndk_path):
        if os.access(ndk_path, os.W_OK) or os.geteuid() == 0:
            patch_hex(ndk_path, 0x307dd1, '83e2fa', '83e2ff')
            patch_hex(ndk_path, 0x307cd6, '83e2fa', '83e2ff')
        else:
            print("libndk_translation is not writable. Please run with sudo.")
    else:
        print("libndk_translation not found. Please install it first.")

# 调用示例
if __name__ == "__main__":
    ndk_path = "ndk/system/lib64/libndk_translation.so"
    patch_ndk_library(ndk_path)
