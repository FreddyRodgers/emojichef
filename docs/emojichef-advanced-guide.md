# EmojiChef Advanced User Guide

## Table of Contents
1. [API Reference](#api-reference)
2. [Advanced Usage](#advanced-usage)
3. [Implementation Details](#implementation-details)
4. [Performance Optimization](#performance-optimization)
5. [Integration Guide](#integration-guide)

## API Reference

### Core Classes

#### EmojiCodec Class
```python
from emoji_codec import EmojiCodec, CompressionMethod, VerificationMethod

# Initialize codec
codec = EmojiCodec(
    recipe_type="classic",      # Encoding base
    compression="ZLIB",         # Compression method
    verification="SHA256"       # Verification method
)
```

#### Available Methods

##### Basic Encoding/Decoding
```python
def encode(self, data: str) -> str:
    """
    Encode string data to emoji sequence
    
    Args:
        data: Input string
        
    Returns:
        Emoji-encoded string
    """

def decode(self, emoji_data: str) -> str:
    """
    Decode emoji sequence back to string
    
    Args:
        emoji_data: Emoji-encoded string
        
    Returns:
        Original string
    """
```

##### Binary Data Handling
```python
def encode_binary(self, data: bytes, mime_type: str = None) -> str:
    """
    Encode binary data with MIME type
    
    Args:
        data: Binary data
        mime_type: Optional MIME type
        
    Returns:
        Emoji-encoded string
    """

def decode_binary(self, encoded: str) -> Tuple[bytes, str]:
    """
    Decode binary data
    
    Returns:
        Tuple of (data, mime_type)
    """
```

##### File Operations
```python
def process_file(
    self,
    input_path: Union[str, Path],
    output_path: Union[str, Path],
    operation: str = 'encode'
) -> Dict[str, float]:
    """
    Process a single file
    
    Args:
        input_path: Source file
        output_path: Destination file
        operation: 'encode' or 'decode'
        
    Returns:
        Processing statistics
    """

def batch_process(
    self,
    file_pattern: str,
    output_dir: str,
    operation: str = 'encode'
) -> List[Dict]:
    """
    Process multiple files
    
    Args:
        file_pattern: Glob pattern
        output_dir: Output directory
        operation: 'encode' or 'decode'
        
    Returns:
        List of processing results
    """
```

##### Analysis and Statistics
```python
def get_stats(
    self,
    original: str,
    encoded: str
) -> Dict[str, float]:
    """
    Calculate encoding statistics
    
    Returns:
        Dictionary of statistics
    """

def get_file_info(
    self,
    file_path: Union[str, Path]
) -> Dict:
    """
    Analyze file and suggest settings
    
    Returns:
        File information and recommendations
    """
```

## Advanced Usage

### Custom Recipe Creation
```python
def create_custom_recipe(start_code: int, size: int) -> Dict[int, str]:
    """Create custom emoji mapping"""
    return {i: chr(start_code + i) for i in range(size)}

# Create custom base-512 recipe
custom_emoji_map = create_custom_recipe(0x1F600, 512)
```

### Stream Processing
```python
def process_stream(input_stream: BinaryIO, output_stream: BinaryIO):
    """Process data streams"""
    codec = EmojiCodec(recipe_type="gourmet")
    
    while chunk := input_stream.read(8192):
        encoded = codec.encode(chunk.decode('utf-8'))
        output_stream.write(encoded.encode('utf-8'))
```

### Memory-Efficient Processing
```python
def process_large_file(input_path: str, output_path: str):
    """Process large files with memory constraints"""
    codec = EmojiCodec()
    chunk_size = 1024 * 1024  # 1MB chunks
    
    with open(input_path, 'rb') as inf, \
         open(output_path, 'w') as outf:
        while chunk := inf.read(chunk_size):
            encoded = codec.encode(chunk.decode('utf-8'))
            outf.write(encoded)
```

### Error Handling
```python
def safe_process(data: str) -> Optional[str]:
    """Process with error handling"""
    try:
        codec = EmojiCodec()
        return codec.encode(data)
    except ValueError as e:
        print(f"Encoding error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
```

## Implementation Details

### Bit Manipulation
```python
def bit_manipulation_example():
    """Example of bit manipulation process"""
    # For base-64 (6 bits per emoji)
    value = 0b101010111100  # 12 bits
    bits = 12
    
    while bits >= 6:
        bits -= 6
        index = (value >> bits) & 0x3F  # Extract 6 bits
        emoji = emoji_map[index]
        # Process emoji...
```

### Compression Integration
```python
def compression_example():
    """Example of compression usage"""
    codec = EmojiCodec(compression=CompressionMethod.ZLIB)
    
    # Compression occurs before encoding
    compressed = zlib.compress(data.encode())
    encoded = codec.encode(compressed.decode('utf-8'))
    
    # Decompression occurs after decoding
    decoded = codec.decode(encoded)
    original = zlib.decompress(decoded.encode())
```

### Verification System
```python
def verification_example():
    """Example of verification system"""
    codec = EmojiCodec(verification=VerificationMethod.SHA256)
    
    # Calculate hash before encoding
    data_hash = hashlib.sha256(data.encode()).hexdigest()
    
    # Include hash in encoded data
    encoded = codec.encode(f"{data}|{data_hash}")
    
    # Verify during decoding
    decoded_data, stored_hash = decoded.split('|')
    calc_hash = hashlib.sha256(decoded_data.encode()).hexdigest()
    assert calc_hash == stored_hash
```

## Performance Optimization

### Recipe Selection
```python
def optimize_recipe(data_size: int) -> str:
    """Select optimal recipe based on data size"""
    if data_size < 1024:  # < 1KB
        return "quick"    # Base-64
    elif data_size < 10240:  # < 10KB
        return "light"    # Base-128
    elif data_size < 102400:  # < 100KB
        return "classic"  # Base-256
    else:
        return "gourmet"  # Base-1024
```

### Memory Usage
```python
def calculate_memory_usage(data_size: int) -> Dict[str, int]:
    """Calculate memory requirements"""
    return {
        'input_buffer': data_size,
        'processing_buffer': data_size * 2,
        'output_buffer': data_size * 1.5,
        'total': data_size * 4.5
    }
```

### Threading
```python
def parallel_process(files: List[str], max_workers: int = 4):
    """Process files in parallel"""
    with concurrent.futures.ThreadPoolExecutor(max_workers) as executor:
        futures = {
            executor.submit(process_file, f): f 
            for f in files
        }
        
        for future in concurrent.futures.as_completed(futures):
            file = futures[future]
            try:
                stats = future.result()
                print(f"Processed {file}: {stats}")
            except Exception as e:
                print(f"Error processing {file}: {e}")
```

## Integration Guide

### Python Integration
```python
from emoji_codec import EmojiCodec

def integrate_with_project():
    """Example project integration"""
    codec = EmojiCodec()
    
    class DataProcessor:
        def __init__(self):
            self.codec = codec
            
        def process_data(self, data: str) -> str:
            return self.codec.encode(data)
```

### CLI Integration
```python
def cli_integration():
    """Example CLI integration"""
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--encode', help='Text to encode')
    parser.add_argument('--recipe', default='classic')
    args = parser.parse_args()
    
    codec = EmojiCodec(recipe_type=args.recipe)
    if args.encode:
        print(codec.encode(args.encode))
```

### Web Service Integration
```python
from flask import Flask, request, jsonify

app = Flask(__name__)
codec = EmojiCodec()

@app.route('/encode', methods=['POST'])
def encode_endpoint():
    data = request.json.get('text')
    try:
        encoded = codec.encode(data)
        return jsonify({'encoded': encoded})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
```

## Best Practices

1. **Recipe Selection**
   - Use appropriate base for data size
   - Consider platform compatibility
   - Balance efficiency vs readability

2. **Error Handling**
   - Validate input data
   - Handle encoding errors
   - Implement retry logic

3. **Performance**
   - Use batch processing for multiple files
   - Implement memory constraints
   - Monitor processing stats

4. **Security**
   - Remember encoding isn't encryption
   - Validate input/output
   - Handle sensitive data appropriately

## Appendix

### Recipe Characteristics
```python
RECIPE_INFO = {
    'quick': {
        'base': 64,
        'bits_per_emoji': 6,
        'emoji_range': '🍅-🍊',
        'best_for': 'Small messages'
    },
    'light': {
        'base': 128,
        'bits_per_emoji': 7,
        'emoji_range': '🎰-🎯',
        'best_for': 'Medium data'
    },
    'classic': {
        'base': 256,
        'bits_per_emoji': 8,
        'emoji_range': '😀-😴',
        'best_for': 'General use'
    },
    'gourmet': {
        'base': 1024,
        'bits_per_emoji': 10,
        'emoji_range': '🤠-🤯',
        'best_for': 'Large files'
    }
}
```

---

## Further Reading
- [Emoji Standards](https://unicode.org/emoji/)
- [Data Encoding Best Practices](https://en.wikipedia.org/wiki/Binary-to-text_encoding)
- [Python Unicode Handling](https://docs.python.org/3/howto/unicode.html)

## Support
Support? There is no support. MIT [LICENSE](LICENSE).
