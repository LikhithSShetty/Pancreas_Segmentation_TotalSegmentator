import os
import sys
import torch
import shutil

def print_separator(title):
    print("\n" + "=" * 50)
    print(f"{title}")
    print("=" * 50)

def verify_pytorch():
    print_separator("PYTORCH & CUDA VERIFICATION")
    print(f"Python version: {sys.version.split()[0]}")
    print(f"PyTorch version: {torch.__version__}")
    
    cuda_available = torch.cuda.is_available()
    print(f"CUDA available: {cuda_available}")
    
    if cuda_available:
        print(f"CUDA version: {torch.version.cuda}")
        print(f"GPU device: {torch.cuda.get_device_name(0)}")
        props = torch.cuda.get_device_properties(0)
        print(f"GPU memory: {props.total_memory / 1e9:.2f} GB")
    else:
        print("⚠️ CUDA not available - inference will be slower on CPU")
    
    print("\n✅ PyTorch installation verified!")

def verify_nnunet_import():
    print_separator("nnU-NET INSTALLATION VERIFICATION")
    try:
        import nnunetv2
        print("✅ nnU-Net successfully imported")
        print("✅ nnU-Net installation verified!")
        return True
    except ImportError as e:
        print(f"❌ nnU-Net import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error checking nnU-Net: {e}")
        return False

def setup_env_vars():
    print_separator("ENVIRONMENT VARIABLES SETUP")
    
    # Get current working directory
    base_dir = os.path.join(os.getcwd(), "nnUNet_data")
    
    # Define paths relative to current location
    env_vars = {
        'nnUNet_raw': os.path.join(base_dir, 'nnUNet_raw'),
        'nnUNet_preprocessed': os.path.join(base_dir, 'nnUNet_preprocessed'),
        'nnUNet_results': os.path.join(base_dir, 'nnUNet_results')
    }
    
    all_set = True
    for var, path in env_vars.items():
        # Set variable for this process
        os.environ[var] = path
        print(f"✅ {var}: {path}")
        
        # Check directory
        if os.path.exists(path):
            print("   📁 Directory exists")
        else:
            print("   ⚠️ Directory does not exist (will be created by nnU-Net if needed)")
            # Create if missing? Maybe better to let user/nnU-Net handle it, but for setup check we can at least checking existence.
    
    print("\n✅ Environment variables configured for this script execution.")
    return env_vars

def verify_directory_structure():
    print_separator("DIRECTORY STRUCTURE VERIFICATION")
    
    base_path = os.getcwd()
    expected_dirs = [
        "nnUNet_data",
        "nnUNet_data/nnUNet_raw",
        "nnUNet_data/nnUNet_preprocessed",
        "nnUNet_data/nnUNet_results",
        "inference_input",
        "inference_output"
    ]
    
    print(f"Base path: {base_path}\n")
    
    missing = []
    for dir_path in expected_dirs:
        full_path = os.path.join(base_path, dir_path)
        if os.path.exists(full_path):
            print(f"✅ {dir_path}")
        else:
            print(f"❌ {dir_path} (missing)")
            missing.append(dir_path)
            
    if not missing:
        print("\n📊 Directory structure verification complete!")
    else:
        print(f"\n⚠️ Missing directories: {len(missing)}")
        print("Creating missing directories...")
        for d in missing:
            os.makedirs(os.path.join(base_path, d), exist_ok=True)
            print(f"Created: {d}")

def main():
    verify_pytorch()
    if verify_nnunet_import():
        setup_env_vars()
        verify_directory_structure()
        
    print_separator("SETUP COMPLETE")
    print("Ready for inference or training if data is present.")

if __name__ == "__main__":
    main()
