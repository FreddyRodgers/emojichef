#!/usr/bin/env python3
import sys
from pathlib import Path
from typing import List
from emoji_codec import EmojiCodec, CompressionMethod, VerificationMethod

class Colors:
    """ANSI color codes"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_banner():
    """Display the EmojiChef banner"""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
███████╗███╗   ███╗ ██████╗      ██╗██╗ ██████╗██╗  ██╗███████╗███████╗
██╔════╝████╗ ████║██╔═══██╗     ██║██║██╔════╝██║  ██║██╔════╝██╔════╝
█████╗  ██╔████╔██║██║   ██║     ██║██║██║     ███████║█████╗  █████╗  
██╔══╝  ██║╚██╔╝██║██║   ██║██   ██║██║██║     ██╔══██║██╔══╝  ██╔══╝  
███████╗██║ ╚═╝ ██║╚██████╔╝╚█████╔╝██║╚██████╗██║  ██║███████╗██║     
╚══════╝╚═╝     ╚═╝ ╚═════╝  ╚════╝ ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝     
{Colors.BLUE}═════════════════════════════════════════════════════════════════
        Cooking Up Delicious Emoji Encodings! 👨‍🍳 v2.2
═════════════════════════════════════════════════════════════════{Colors.ENDC}
"""
    print(banner)

def print_menu():
    """Display the main menu"""
    print(f"\n{Colors.GREEN}=== EmojiChef's Kitchen ==={Colors.ENDC}")
    print("1. Quick Encode/Decode")
    print("2. File Operations")
    print("3. Batch Processing")
    print("4. Recipe Settings")
    print("5. View Recipe Book")
    print("6. Exit Kitchen")
    print(f"{Colors.GREEN}========================={Colors.ENDC}")

def get_valid_input(prompt: str, valid_options: List[str]) -> str:
    """Get validated user input"""
    while True:
        choice = input(f"{Colors.CYAN}{prompt}{Colors.ENDC}").strip()
        if choice in valid_options:
            return choice
        print(f"{Colors.RED}Invalid choice. Please choose from {', '.join(valid_options)}{Colors.ENDC}")

def handle_quick_operation(codec: EmojiCodec):
    """Handle quick encode/decode operations"""
    print(f"\n{Colors.YELLOW}Quick Encode/Decode{Colors.ENDC}")
    print("1. Encode Message")
    print("2. Decode Message")
    print("3. Back to Menu")
    
    choice = get_valid_input("Select operation (1-3): ", ['1', '2', '3'])
    
    if choice == '3':
        return
        
    try:
        if choice == '1':
            message = input(f"\n{Colors.CYAN}Enter message to encode: {Colors.ENDC}")
            encoded = codec.encode(message)
            stats = codec.get_stats(message, encoded)
            
            print(f"\n{Colors.GREEN}Encoded message: {Colors.ENDC}{encoded}")
            print(f"{Colors.YELLOW}Statistics:")
            print(f"Original size: {stats['original_bytes']} bytes")
            print(f"Encoded length: {stats['encoded_length']} emojis")
            print(f"Compression ratio: {stats['actual_ratio']:.2f}{Colors.ENDC}")
        else:
            message = input(f"\n{Colors.CYAN}Enter emoji message to decode: {Colors.ENDC}")
            decoded = codec.decode(message)
            print(f"\n{Colors.GREEN}Decoded message: {Colors.ENDC}{decoded}")
            
    except ValueError as e:
        print(f"{Colors.RED}Error: {e}{Colors.ENDC}")

def handle_file_operations(codec: EmojiCodec):
    """Handle file encoding/decoding operations"""
    print(f"\n{Colors.YELLOW}File Operations{Colors.ENDC}")
    print("1. Encode File")
    print("2. Decode File")
    print("3. Back to Menu")
    
    choice = get_valid_input("Select operation (1-3): ", ['1', '2', '3'])
    
    if choice == '3':
        return
        
    try:
        if choice == '1':
            # Get input file
            while True:
                input_file = input(f"{Colors.CYAN}Enter input file path (or 'cancel'): {Colors.ENDC}")
                if input_file.lower() == 'cancel':
                    return
                    
                input_path = Path(input_file).resolve()
                if input_path.exists():
                    break
                print(f"{Colors.RED}File not found. Please enter a valid path.{Colors.ENDC}")
            
            # Get output file
            output_file = input(f"{Colors.CYAN}Enter output filename (default: <input>_encoded.emoji): {Colors.ENDC}")
            if not output_file:
                output_path = input_path.parent / f"{input_path.stem}_encoded.emoji"
            else:
                output_path = Path(output_file).resolve()
                output_path.parent.mkdir(parents=True, exist_ok=True)
            
            print(f"\n{Colors.YELLOW}Processing file...")
            print(f"Input: {input_path}")
            print(f"Output: {output_path}{Colors.ENDC}")
            
            stats = codec.process_file(str(input_path), str(output_path), 'encode')
            
            print(f"\n{Colors.GREEN}File encoded successfully!")
            print(f"Statistics:")
            print(f"Original size: {stats['original_bytes']} bytes")
            print(f"Encoded length: {stats['encoded_length']} emojis")
            print(f"Compression ratio: {stats['actual_ratio']:.2f}{Colors.ENDC}")
        
        else:  # decode
            while True:
                input_file = input(f"{Colors.CYAN}Enter encoded file path (or 'cancel'): {Colors.ENDC}")
                if input_file.lower() == 'cancel':
                    return
                    
                input_path = Path(input_file).resolve()
                if input_path.exists():
                    break
                print(f"{Colors.RED}File not found. Please enter a valid path.{Colors.ENDC}")
            
            output_file = input(f"{Colors.CYAN}Enter output filename (default: <input>_decoded<ext>): {Colors.ENDC}")
            if not output_file:
                output_path = input_path.parent / f"{input_path.stem}_decoded.txt"
            else:
                output_path = Path(output_file).resolve()
                output_path.parent.mkdir(parents=True, exist_ok=True)
            
            print(f"\n{Colors.YELLOW}Processing file...")
            print(f"Input: {input_path}")
            print(f"Output: {output_path}{Colors.ENDC}")
            
            stats = codec.process_file(str(input_path), str(output_path), 'decode')
            
            print(f"\n{Colors.GREEN}File decoded successfully!")
            print(f"Decoded size: {stats['decoded_size']} bytes{Colors.ENDC}")
            
    except ValueError as e:
        print(f"{Colors.RED}Error: {e}{Colors.ENDC}")

def handle_batch_processing(codec: EmojiCodec):
    """Handle batch file processing"""
    print(f"\n{Colors.YELLOW}Batch Processing{Colors.ENDC}")
    print("1. Encode Files")
    print("2. Decode Files")
    print("3. Back to Menu")
    
    choice = get_valid_input("Select operation (1-3): ", ['1', '2', '3'])
    
    if choice == '3':
        return
        
    try:
        pattern = input(f"{Colors.CYAN}Enter file pattern (e.g., *.txt): {Colors.ENDC}")
        output_dir = input(f"{Colors.CYAN}Enter output directory: {Colors.ENDC}")
        
        print(f"\n{Colors.YELLOW}Processing files...{Colors.ENDC}")
        results = codec.batch_process(
            pattern, output_dir,
            'encode' if choice == '1' else 'decode'
        )
        
        successful = len([r for r in results if r['success']])
        print(f"\n{Colors.GREEN}Batch processing complete!")
        print(f"Successfully processed: {successful}/{len(results)} files{Colors.ENDC}")
        
        if successful < len(results):
            print(f"\n{Colors.RED}Failed files:")
            for result in results:
                if not result['success']:
                    print(f"{result['file']}: {result['error']}")
            print(Colors.ENDC)
            
    except Exception as e:
        print(f"{Colors.RED}Error: {str(e)}{Colors.ENDC}")

def handle_settings(codec: EmojiCodec) -> EmojiCodec:
    """Handle codec settings"""
    print(f"\n{Colors.YELLOW}Current Recipe Settings:{Colors.ENDC}")
    print(f"Recipe type: {codec.recipe_type}")
    print(f"Compression: {codec.compression}")
    print(f"Verification: {codec.verification}")
    
    print("\nChange settings:")
    print("1. Recipe Type")
    print("2. Compression")
    print("3. Verification")
    print("4. Back to Menu")
    
    choice = get_valid_input("Select setting to change (1-4): ", ['1', '2', '3', '4'])
    
    if choice == '4':
        return codec
        
    if choice == '1':
        print("\nAvailable recipes:")
        print("1. Quick (Base-64)")
        print("2. Light (Base-128)")
        print("3. Classic (Base-256)")
        print("4. Gourmet (Base-1024)")
        
        recipe = get_valid_input("Select recipe (1-4): ", ['1', '2', '3', '4'])
        recipes = {
            '1': 'quick',
            '2': 'light',
            '3': 'classic',
            '4': 'gourmet'
        }
        return EmojiCodec(
            recipes[recipe],
            codec.compression,
            codec.verification
        )
        
    elif choice == '2':
        print("\nCompression options:")
        print("1. None")
        print("2. ZLIB")
        
        comp = get_valid_input("Select option (1-2): ", ['1', '2'])
        codec.compression = CompressionMethod.NONE if comp == '1' else CompressionMethod.ZLIB
        
    else:
        print("\nVerification options:")
        print("1. None")
        print("2. SHA256")
        
        verify = get_valid_input("Select option (1-2): ", ['1', '2'])
        codec.verification = VerificationMethod.NONE if verify == '1' else VerificationMethod.SHA256
    
    print(f"\n{Colors.GREEN}Settings updated!{Colors.ENDC}")
    return codec

def view_recipe_book():
    """Display information about available recipes"""
    print(f"\n{Colors.YELLOW}=== EmojiChef's Recipe Book ==={Colors.ENDC}")
    
    recipes = [
        {
            'name': 'Quick Recipe (Base-64)',
            'emojis': '🍅🍆🍇',
            'best_for': 'Small messages, maximum compatibility',
            'features': [
                'Food emojis',
                '6 bits per emoji',
                'Fast processing'
            ]
        },
        {
            'name': 'Light Recipe (Base-128)',
            'emojis': '🎰🎱🎲',
            'best_for': 'Medium-sized messages',
            'features': [
                'Activity emojis',
                '7 bits per emoji',
                'Good compatibility'
            ]
        },
        {
            'name': 'Classic Recipe (Base-256)',
            'emojis': '😀😃😄',
            'best_for': 'General purpose encoding',
            'features': [
                'Smiley emojis',
                '8 bits per emoji',
                'Excellent compatibility'
            ]
        },
        {
            'name': 'Gourmet Recipe (Base-1024)',
            'emojis': '🤠🤡🤢',
            'best_for': 'Large files, maximum efficiency',
            'features': [
                'Extended emoji set',
                '10 bits per emoji',
                'Best compression'
            ]
        }
    ]
    
    for recipe in recipes:
        print(f"\n{Colors.GREEN}{recipe['name']}{Colors.ENDC}")
        print(f"Sample: {recipe['emojis']}")
        print(f"Best for: {recipe['best_for']}")
        print("Features:")
        for feature in recipe['features']:
            print(f"  • {feature}")
        print("-" * 40)
    
    input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.ENDC}")

def main():
    """Main program loop"""
    print_banner()
    codec = EmojiCodec()
    
    while True:
        print_menu()
        choice = get_valid_input("Select option (1-6): ", ['1', '2', '3', '4', '5', '6'])
        
        if choice == '1':
            handle_quick_operation(codec)
        elif choice == '2':
            handle_file_operations(codec)
        elif choice == '3':
            handle_batch_processing(codec)
        elif choice == '4':
            codec = handle_settings(codec)
        elif choice == '5':
            view_recipe_book()
        else:
            print(f"\n{Colors.GREEN}Thanks for visiting EmojiChef's Kitchen! 👨‍🍳{Colors.ENDC}")
            sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Chef had to leave early. Goodbye! 👨‍🍳{Colors.ENDC}")
        sys.exit(0)
