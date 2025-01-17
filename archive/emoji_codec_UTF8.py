"""
emoji_codec.py - Core encoding/decoding functionality for EmojiChef v2.1
"""
import math
import zlib
import hashlib
from typing import Dict, Union, List
from pathlib import Path


class CompressionMethod:
    """Compression method options"""
    NONE = 'none'
    ZLIB = 'zlib'


class VerificationMethod:
    """Verification method options"""
    NONE = 'none'
    SHA256 = 'sha256'


class EmojiCodec:
    """
    EmojiChef encoder/decoder with compression and verification support
    """
    
    def __init__(self, recipe_type: str = "classic", 
                 compression: str = CompressionMethod.NONE,
                 verification: str = VerificationMethod.NONE):
        """
        Initialize codec with specified settings
        
        Args:
            recipe_type: Base encoding type ("quick", "light", "classic", "gourmet")
            compression: Compression method to use
            verification: Verification method for integrity checks
        """
        self.recipe_type = recipe_type
        self.compression = compression
        self.verification = verification
        self._initialize_ingredients()

    def _initialize_ingredients(self):
        """Initialize encoding maps based on recipe type"""
        # Recipe configuration: (base_size, unicode_start)
        recipes = {
            "quick": (64, 0x1F345),    # Food emojis
            "light": (128, 0x1F3B0),   # Activity emojis
            "classic": (256, 0x1F600), # Smiley emojis
            "gourmet": (1024, 0x1F900) # Extended emojis
        }
        
        base_size, start_code = recipes.get(
            self.recipe_type, 
            recipes["classic"]
        )
        
        # Create encoding/decoding maps
        self.emoji_map = {
            i: chr(start_code + i) 
            for i in range(base_size)
        }
        self.reverse_map = {v: k for k, v in self.emoji_map.items()}
        
        # Calculate encoding parameters
        self.base_size = base_size
        self.bits_per_chunk = int(math.log2(base_size))
        self.mask = (1 << self.bits_per_chunk) - 1

    def _process_data(self, data: bytes, compress: bool = True) -> bytes:
        """Process data with optional compression"""
        if compress and self.compression == CompressionMethod.ZLIB:
            return zlib.compress(data)
        return data

    def _unprocess_data(self, data: bytes, decompress: bool = True) -> bytes:
        """Reverse data processing"""
        if decompress and self.compression == CompressionMethod.ZLIB:
            return zlib.decompress(data)
        return data

    def _calculate_hash(self, data: bytes) -> str:
        """Calculate hash of data if verification enabled"""
        if self.verification == VerificationMethod.SHA256:
            return hashlib.sha256(data).hexdigest()
        return ''

    def encode(self, data: str) -> str:
        """
        Encode a string into emoji representation
        
        Args:
            data: String to encode
            
        Returns:
            Emoji-encoded string
            
        Raises:
            ValueError: If encoding fails
        """
        try:
            # Convert to bytes and process
            byte_data = data.encode('utf-8')
            processed = self._process_data(byte_data)
            
            # Encode to emojis
            result = []
            current_bits = 0
            current_value = 0
            
            for byte in processed:
                current_value = (current_value << 8) | byte
                current_bits += 8
                
                while current_bits >= self.bits_per_chunk:
                    current_bits -= self.bits_per_chunk
                    index = (current_value >> current_bits) & self.mask
                    result.append(self.emoji_map[index])
                    current_value &= (1 << current_bits) - 1
            
            # Handle remaining bits
            if current_bits > 0:
                index = (current_value << (self.bits_per_chunk - current_bits)) & self.mask
                result.append(self.emoji_map[index])
                
            return ''.join(result)
            
        except Exception as e:
            raise ValueError(f"Encoding error: {str(e)}")

    def decode(self, emoji_data: str) -> str:
        """
        Decode emoji representation back to original string
        
        Args:
            emoji_data: Emoji string to decode
            
        Returns:
            Decoded string
            
        Raises:
            ValueError: If decoding fails
        """
        try:
            # Decode emojis
            result = bytearray()
            current_bits = 0
            current_value = 0
            
            for emoji in emoji_data:
                value = self.reverse_map[emoji]
                current_value = (current_value << self.bits_per_chunk) | value
                current_bits += self.bits_per_chunk
                
                while current_bits >= 8:
                    current_bits -= 8
                    byte = (current_value >> current_bits) & 0xFF
                    result.append(byte)
                    current_value &= (1 << current_bits) - 1
            
            # Unprocess data
            processed = bytes(result)
            original = self._unprocess_data(processed)
            
            return original.decode('utf-8')
            
        except Exception as e:
            raise ValueError(f"Decoding error: {str(e)}")

    def get_stats(self, original: str, encoded: str) -> Dict[str, float]:
        """
        Calculate encoding statistics
        
        Args:
            original: Original string
            encoded: Encoded emoji string
            
        Returns:
            Dictionary containing:
            - original_bytes: Original size in bytes
            - encoded_length: Number of emojis
            - actual_ratio: Actual compression ratio
            - theoretical_ratio: Theoretical compression ratio
            - bits_per_emoji: Bits represented per emoji
        """
        orig_bytes = len(original.encode('utf-8'))
        enc_len = len(encoded)
        ratio = enc_len/orig_bytes if orig_bytes > 0 else 0
        bits_per_char = math.log2(self.base_size)
        
        return {
            'original_bytes': orig_bytes,
            'encoded_length': enc_len,
            'actual_ratio': ratio,
            'theoretical_ratio': 8/bits_per_char,
            'bits_per_emoji': bits_per_char
        }

    def process_file(self, input_path: str, output_path: str, 
                    operation: str = 'encode') -> Dict:
        """
        Process a single file
        
        Args:
            input_path: Path to input file
            output_path: Path to output file
            operation: 'encode' or 'decode'
            
        Returns:
            Dictionary with processing statistics
            
        Raises:
            ValueError: If file processing fails
        """
        try:
            if operation == 'encode':
                with open(input_path, 'r', encoding='utf-8') as f:
                    data = f.read()
                encoded = self.encode(data)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(encoded)
                    
                return self.get_stats(data, encoded)
                
            else:  # decode
                with open(input_path, 'r', encoding='utf-8') as f:
                    data = f.read()
                decoded = self.decode(data)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(decoded)
                    
                return {'decoded_size': len(decoded)}
                
        except Exception as e:
            raise ValueError(f"File processing error: {str(e)}")

    def batch_process(self, file_pattern: str, output_dir: str, 
                     operation: str = 'encode') -> List[Dict]:
        """
        Process multiple files
        
        Args:
            file_pattern: Glob pattern for input files
            output_dir: Directory for output files
            operation: 'encode' or 'decode'
            
        Returns:
            List of dictionaries with processing results
        """
        from glob import glob
        
        # Create output directory
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Get files and process
        files = glob(file_pattern)
        results = []
        
        for input_file in files:
            input_path = Path(input_file)
            if operation == 'encode':
                output_path = output_dir / f"{input_path.stem}.emoji"
            else:
                output_path = output_dir / f"decoded_{input_path.stem}{input_path.suffix}"
                
            try:
                stats = self.process_file(input_file, str(output_path), operation)
                stats['file'] = input_file
                stats['success'] = True
                results.append(stats)
            except Exception as e:
                results.append({
                    'file': input_file,
                    'success': False,
                    'error': str(e)
                })
        
        return results


# Example usage
if __name__ == "__main__":
    # Create codec with default settings
    codec = EmojiCodec()
    
    # Simple encoding example
    message = "Hello, World!"
    encoded = codec.encode(message)
    decoded = codec.decode(encoded)
    
    print(f"Original: {message}")
    print(f"Encoded: {encoded}")
    print(f"Decoded: {decoded}")
    
    # Get encoding statistics
    stats = codec.get_stats(message, encoded)
    print("\nStats:")
    for key, value in stats.items():
        print(f"{key}: {value}")
