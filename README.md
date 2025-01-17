# 👨‍🍳 EmojiChef v2.1 | LoadedTater

Welcome to EmojiChef's Kitchen, where plain text gets cooked into delicious [emoji](https://home.unicode.org/emoji/) encodings! EmojiChef is a Python-based text encoder that transforms your messages into tasty emoji representations using various "recipe" types. Our kitchen serves up both classic and gourmet emoji dishes, with a focus on efficiency and flavor!

For peer review: [mathematic principles and encoding theory](docs/emojichef-v2-math.md) supporting EmojiChef v2.1

![image](images/interactive-menu.png)

## Features

- 🔄 Multiple encoding bases (64, 128, 256, 1024)
- 📦 UTF-8 text and Binary file support
- 🗜️ Optional compression
- 📁 Batch processing
- 🛠️ Interactive menu for those who shall not be named

## Installation

```bash
git clone https://github.com/FreddyRodgers/emojichef.git
cd emojichef
```

Requires Python 3.6 or later. No additional dependencies needed!

## Quick Start

### Basic Text Encoding
```python
from emoji_codec import EmojiCodec

# Create codec
codec = EmojiCodec()

# Encode text
encoded = codec.encode("Hello!")
print(encoded)  # Output: 😀😃😄😁😆😅

# Decode text
decoded = codec.decode(encoded)
print(decoded)  # Output: Hello!
```

### File Processing
```python
# Encode a file
codec.process_file('document.txt', 'encoded.emoji', 'encode')

# Decode a file
codec.process_file('encoded.emoji', 'decoded.txt', 'decode')
```

### Using Different Recipes
```python
# Quick recipe (Base-64)
quick_codec = EmojiCodec("quick")
quick_encoded = quick_codec.encode("Hi!")  # Uses food emojis

# Gourmet recipe (Base-1024)
gourmet_codec = EmojiCodec("gourmet")
gourmet_encoded = gourmet_codec.encode("Hi!")  # Uses extended emojis
```

### With Compression
```python
from emoji_codec import EmojiCodec, CompressionMethod

# Enable compression
codec = EmojiCodec(
    recipe_type="gourmet",
    compression=CompressionMethod.ZLIB
)

# Process large file with compression
codec.process_file('large_file.txt', 'compressed.emoji', 'encode')
```

### Batch Processing
```python
# Process multiple text files
results = codec.batch_process(
    "*.txt",
    "encoded_files",
    operation='encode'
)

# Process multiple encoded files
results = codec.batch_process(
    "*.emoji",
    "decoded_files",
    operation='decode'
)
```

## Interactive Menu

Run the interactive menu:
```bash
python emojichef.py
```

This provides access to:
- Quick encode/decode
- File operations
- Batch processing
- Settings management
- Analysis tools

## Recipe Types

- 🍅 **Quick** (Base-64): Food emojis, best for small messages
- 🎰 **Light** (Base-128): Activity emojis, balanced encoding
- 😀 **Classic** (Base-256): Smiley emojis, standard encoding
- 🤠 **Gourmet** (Base-1024): Extended emojis, maximum efficiency

###
[Emoji Mapping Documentation](docs/emoji-mappings.md)

## Planned Features

- [ ] Custom emoji mapping definitions
- [ ] Support ecoji 2.0 (base 1024) encoding scheme
- [ ] Streaming support for large files
- [ ] Configuration file support

## Security Note

⚠️ EmojiChef is an encoding tool, not an encryption tool. [Do not use it for sensitive data](docs/emojichef-security-notice.md).

## Acknowledgments

- Inspired by [Wingdings](https://en.wikipedia.org/wiki/Wingdings), [CyberChef](https://github.com/gchq/CyberChef), and the prior experimental emoji encoding schemes 
   - emojicoding (Base1024): [https://github.com/shea256/emojicoding](https://github.com/shea256/emojicoding)
   - Ecoji 2.0 (Base1024): [https://github.com/keith-turner/ecoji](https://github.com/keith-turner/ecoji)
- Motivated by [Mr. Jeff the Man](https://x.com/MrJeffMan), [shmoocon](https://shmoocon.org) lobbycon, and [nyxgeek](https://x.com/nyxgeek) 
- Special thanks to the emoji standards committee and Claude 3.5 Sonnet

## Version History

- v2.1: Added binary file support and enhanced menu
- v2.0: Flawed Rewrite: Added compression and file operations
- v1.0: Initial release with basic encoding

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.MD) file for details.