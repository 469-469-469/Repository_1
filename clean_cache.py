import os
import shutil

def remove_pycache(root="."):
    for dirpath, dirnames, filenames in os.walk(root):
        if "__pycache__" in dirnames:
            cache_path = os.path.join(dirpath, "__pycache__")
            print(f"Удаляю: {cache_path}")
            shutil.rmtree(cache_path)

if __name__ == "__main__":
    remove_pycache()
    print("Готово: все __pycache__ удалены")