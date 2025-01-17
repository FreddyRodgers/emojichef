import math
import zlib
import hashlib
import mimetypes
import base64
from typing import Dict, Union, List, Tuple, BinaryIO
from pathlib import Path
import json

class CompressionMethod:
    NONE = 'none'
    ZLIB = 'zlib'

class VerificationMethod:
    NONE = 'none'
    SHA256 = 'sha256'

class FileHandler:
    """Handle different file types"""
    
    @staticmethod
    def read_file(file_path: Union[str, Path]) -> Tuple[bytes, str]:
        """
        Read file content and determine mime type
        
        Returns:
            Tuple of (file_content, mime_type)
        """
        file_path = Path(file_path)
        mime_type, _ = mimetypes.guess_type(str(file_path))
        
        with open(file_path, 'rb') as f:
            content = f.read()
            
        return content, mime_type or 'application/octet-stream'
    
    @staticmethod
    def write_file(file_path: Union[str, Path], content: bytes):
        """Write content to file"""
        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'wb') as f:
            f.write(content)

class EmojiCodec:
    def __init__(self, recipe_type: str = "classic",
                 compression: str = CompressionMethod.NONE,
                 verification: str = VerificationMethod.NONE):
        """Initialize codec with specified settings"""
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

    def _prepare_binary_data(self, data: bytes, mime_type: str = None) -> Dict:
        """
        Prepare binary data for encoding
        
        Returns dictionary with:
            - content: Base64 encoded data
            - mime_type: MIME type if provided
            - size: Original size in bytes
        """
        return {
            'content': base64.b64encode(data).decode('utf-8'),
            'mime_type': mime_type,
            'size': len(data)
        }

    def _restore_binary_data(self, data: Dict) -> bytes:
        """Restore binary data from prepared format"""
        return base64.b64decode(data['content'].encode('utf-8'))

    def encode_binary(self, data: bytes, mime_type: str = None) -> str:
        """
        Encode binary data with mime type information
        """
        try:
            # Prepare binary data
            prepared = self._prepare_binary_data(data, mime_type)
            
            # Convert to JSON and encode
            json_data = json.dumps(prepared)
            return self.encode(json_data)
            
        except Exception as e:
            raise ValueError(f"Binary encoding error: {str(e)}")

    def decode_binary(self, encoded: str) -> Tuple[bytes, str]:
        """
        Decode binary data and return content with mime type
        
        Returns:
            Tuple of (content, mime_type)
        """
        try:
            # Decode emoji encoding
            json_data = self.decode(encoded)
            data = json.loads(json_data)
            
            # Restore binary data
            content = self._restore_binary_data(data)
            return content, data.get('mime_type')
            
        except Exception as e:
            raise ValueError(f"Binary decoding error: {str(e)}")

    def process_file(self, input_path: Union[str, Path], 
                    output_path: Union[str, Path],
                    operation: str = 'encode') -> Dict:
        """
        Process a file with binary support
        """
        try:
            if operation == 'encode':
                # Read and encode file
                content, mime_type = FileHandler.read_file(input_path)
                encoded = self.encode_binary(content, mime_type)
                
                # Write encoded data
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(encoded)
                
                return {
                    'original_bytes': len(content),
                    'encoded_length': len(encoded),
                    'mime_type': mime_type,
                    'actual_ratio': len(encoded)/len(content)
                }
                
            else:  # decode
                # Read encoded data
                with open(input_path, 'r', encoding='utf-8') as f:
                    encoded = f.read()
                
                # Decode and write file
                content, mime_type = self.decode_binary(encoded)
                FileHandler.write_file(output_path, content)
                
                return {
                    'decoded_size': len(content),
                    'mime_type': mime_type
                }
                
        except Exception as e:
            raise ValueError(f"File processing error: {str(e)}")

    def batch_process(self, file_pattern: str, output_dir: str,
                     operation: str = 'encode') -> List[Dict]:
        """
        Process multiple files with binary support
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
                # Try to preserve original extension for decoding
                mime_type, _ = mimetypes.guess_type(str(input_path))
                extension = mimetypes.guess_extension(mime_type) if mime_type else '.bin'
                output_path = output_dir / f"decoded_{input_path.stem}{extension}"
                
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

    def get_file_info(self, file_path: Union[str, Path]) -> Dict:
        """
        Get detailed information about a file
        """
        try:
            content, mime_type = FileHandler.read_file(file_path)
            
            return {
                'size': len(content),
                'mime_type': mime_type,
                'can_process': True,
                'suggested_recipe': self._suggest_recipe(len(content))
            }
        except Exception as e:
            return {
                'error': str(e),
                'can_process': False
            }

    def _suggest_recipe(self, size: int) -> str:
        """Suggest optimal recipe based on file size"""
        if size < 1024:  # < 1KB
            return "quick"
        elif size < 10240:  # < 10KB
            return "light"
        elif size < 102400:  # < 100KB
            return "classic"
        else:
            return "gourmet"