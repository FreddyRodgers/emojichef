#!/usr/bin/env python3
import sys
import argparse
from pathlib import Path
from typing import Optional
from emoji_codec import EmojiCodec, CompressionMethod, VerificationMethod

__version__ = "2.2.0"

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

class EmojiChefCLI:
    def __init__(self):
        self.parser = self._create_parser()
        self.use_color = True

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create argument parser with all options"""
        parser = argparse.ArgumentParser(
            description="""
EmojiChef v2.2 - Cook up some delicious emoji encodings! 👨‍🍳

A versatile tool for encoding data using emoji characters with support for:
- Multiple encoding bases (64, 128, 256, 1024)
- File processing with compression
- Batch operations
- Data verification
- Interactive menu interface
""",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Basic text encoding
  emojichef-cli.py encode "Hello World"
  
  # Encode with gourmet recipe (base-1024)
  emojichef-cli.py encode -r gourmet "Hello World"
  
  # Encode file with compression and verification
  emojichef-cli.py encode -f input.txt -o output.emoji -c zlib -v sha256
  
  # Decode emoji file
  emojichef-cli.py decode -f encoded.emoji -o decoded.txt
  
  # Batch process text files
  emojichef-cli.py batch "*.txt" --batch-output encoded_files/
  
  # File analysis
  emojichef-cli.py analyze -f document.txt
  
  # Interactive mode
  emojichef-cli.py interactive

For more details and documentation:
https://github.com/FreddyRodgers/emojichef
"""
        )

        # Command groups
        commands = parser.add_argument_group('Commands')
        recipe_opts = parser.add_argument_group('Recipe Options')
        file_opts = parser.add_argument_group('File Options')
        process_opts = parser.add_argument_group('Processing Options')

        # Commands
        commands.add_argument(
            'command',
            choices=['encode', 'decode', 'batch', 'interactive', 'analyze'],
            help="""
Operation to perform:

  encode      - Convert text/files to emoji encoding
  decode      - Convert emoji data back to original form
  batch       - Process multiple files
  interactive - Start interactive menu interface
  analyze     - Analyze input and suggest optimal settings
"""
        )

        commands.add_argument(
            'input',
            nargs='?',
            help="Input text or file pattern for batch operations"
        )

        # Recipe options
        recipe_opts.add_argument(
            '-r', '--recipe',
            choices=['quick', 'light', 'classic', 'gourmet'],
            default='classic',
            help="""
Encoding recipe to use:
  quick   - Base-64 (food emojis)      [compact]
  light   - Base-128 (activity emojis) [balanced]
  classic - Base-256 (smiley emojis)   [standard]
  gourmet - Base-1024 (extended set)   [efficient]
"""
        )

        recipe_opts.add_argument(
            '-c', '--compression',
            choices=['none', 'zlib'],
            default='none',
            help="Enable data compression"
        )

        recipe_opts.add_argument(
            '-v', '--verification',
            choices=['none', 'sha256'],
            default='none',
            help="Enable integrity verification"
        )

        # File options
        file_opts.add_argument(
            '-f', '--file',
            help="Input file path"
        )

        file_opts.add_argument(
            '-o', '--output',
            help="Output file path (default: auto-generated)"
        )

        file_opts.add_argument(
            '--batch-output',
            help="Output directory for batch processing"
        )

        # Processing options
        process_opts.add_argument(
            '-q', '--quiet',
            action='store_true',
            help="Suppress progress output"
        )

        process_opts.add_argument(
            '--no-color',
            action='store_true',
            help="Disable colored output"
        )

        process_opts.add_argument(
            '--debug',
            action='store_true',
            help="Enable debug output"
        )

        # Version
        parser.add_argument(
            '--version',
            action='version',
            version=f'EmojiChef v{__version__}'
        )

        return parser

    def colorize(self, text: str, color: str) -> str:
        """Apply color if enabled"""
        if self.use_color:
            return f"{color}{text}{Colors.ENDC}"
        return text

    def process_text(self, text: str, codec: EmojiCodec, operation: str, quiet: bool = False) -> str:
        """Process text input"""
        try:
            if operation == 'encode':
                result = codec.encode(text)
                if not quiet:
                    print(self.colorize("Encoded: ", Colors.GREEN) + result)
            else:
                result = codec.decode(text)
                if not quiet:
                    print(self.colorize("Decoded: ", Colors.GREEN) + result)
            return result
            
        except Exception as e:
            print(self.colorize(f"Error: {e}", Colors.RED), file=sys.stderr)
            sys.exit(1)

    def process_file(self, input_path: str, output_path: str, 
                    codec: EmojiCodec, operation: str, quiet: bool = False) -> None:
        """Process single file"""
        try:
            stats = codec.process_file(input_path, output_path, operation)
            
            if not quiet:
                print(self.colorize("\nFile Processing:", Colors.CYAN))
                print(f"Input:  {input_path}")
                print(f"Output: {output_path}")
                
                if operation == 'encode':
                    print(self.colorize("\nStatistics:", Colors.YELLOW))
                    print(f"Original size: {stats['original_bytes']} bytes")
                    print(f"Encoded length: {stats['encoded_length']} emojis")
                    print(f"Ratio: {stats['actual_ratio']:.2f}")
                else:
                    print(f"\nDecoded size: {stats['decoded_size']} bytes")
                    
        except Exception as e:
            print(self.colorize(f"Error: {e}", Colors.RED), file=sys.stderr)
            sys.exit(1)

    def batch_process(self, pattern: str, output_dir: str,
                     codec: EmojiCodec, operation: str, quiet: bool = False) -> None:
        """Process multiple files"""
        try:
            results = codec.batch_process(pattern, output_dir, operation)
            
            if not quiet:
                successful = len([r for r in results if r['success']])
                print(self.colorize(f"\nProcessed {successful}/{len(results)} files", Colors.GREEN))
                
                if successful < len(results):
                    print(self.colorize("\nFailed files:", Colors.RED))
                    for result in results:
                        if not result['success']:
                            print(f"- {result['file']}: {result['error']}")
                            
        except Exception as e:
            print(self.colorize(f"Error: {e}", Colors.RED), file=sys.stderr)
            sys.exit(1)

    def analyze_input(self, input_path: str, codec: EmojiCodec) -> None:
        """Analyze input and suggest optimal settings"""
        try:
            info = codec.get_file_info(input_path)
            
            print(self.colorize("\nFile Analysis:", Colors.CYAN))
            print(f"Size: {info['size']} bytes")
            print(f"MIME type: {info['mime_type']}")
            print(f"Can process: {info['can_process']}")
            
            print(self.colorize("\nRecommendations:", Colors.YELLOW))
            print(f"Suggested recipe: {info['suggested_recipe']}")
            print("Compression: " + 
                  ("Recommended" if info['size'] > 1024 else "Optional"))
            
        except Exception as e:
            print(self.colorize(f"Error: {e}", Colors.RED), file=sys.stderr)
            sys.exit(1)

    def run(self) -> None:
        """Run CLI with provided arguments"""
        args = self.parser.parse_args()
        
        # Handle color setting
        self.use_color = not args.no_color
        
        # Create codec with specified options
        codec = EmojiCodec(
            recipe_type=args.recipe,
            compression=args.compression.upper(),
            verification=args.verification.upper()
        )
        
        # Handle commands
        if args.command == 'encode':
            if args.file:
                output = args.output or f"{args.file}.emoji"
                self.process_file(args.file, output, codec, 'encode', args.quiet)
            elif args.input:
                self.process_text(args.input, codec, 'encode', args.quiet)
            else:
                print(self.colorize("Error: No input provided", Colors.RED), 
                      file=sys.stderr)
                sys.exit(1)
                
        elif args.command == 'decode':
            if args.file:
                output = args.output or f"decoded_{Path(args.file).stem}"
                self.process_file(args.file, output, codec, 'decode', args.quiet)
            elif args.input:
                self.process_text(args.input, codec, 'decode', args.quiet)
            else:
                print(self.colorize("Error: No input provided", Colors.RED), 
                      file=sys.stderr)
                sys.exit(1)
                
        elif args.command == 'batch':
            if not args.input:
                print(self.colorize("Error: No input pattern provided", Colors.RED), 
                      file=sys.stderr)
                sys.exit(1)
                
            output_dir = args.batch_output or 'emoji_output'
            self.batch_process(
                args.input,
                output_dir,
                codec,
                'encode',
                args.quiet
            )
            
        elif args.command == 'analyze':
            if not args.file:
                print(self.colorize("Error: No input file provided", Colors.RED), 
                      file=sys.stderr)
                sys.exit(1)
            self.analyze_input(args.file, codec)
            
        elif args.command == 'interactive':
            # Import and run interactive menu
            from emojichef import main as run_interactive
            run_interactive()

def main():
    """Main entry point"""
    try:
        cli = EmojiChefCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
