import os

def list_dir_tree(start_path, max_depth=3, prefix=""):
    for root, dirs, files in os.walk(start_path):
        depth = root[len(start_path):].count(os.sep)
        if depth > max_depth:
            continue
        indent = "    " * depth
        print(f"{indent}{os.path.basename(root)}/")
        for f in files:
            print(f"{indent}    {f}")

if __name__ == "__main__":
    print("\n--- nnUNet_results/ ---")
    list_dir_tree(r"nnUNet_data/nnUNet_results", max_depth=2)
    print("\n--- inference_input/ ---")
    list_dir_tree(r"inference_input", max_depth=1)
    print("\n--- nnUNet_raw/ ---")
    list_dir_tree(r"nnUNet_data/nnUNet_raw", max_depth=2)
