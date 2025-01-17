# EmojiChef Character Mappings Reference

This document details the emoji character mappings used in each encoding base (recipe) type.

## Quick Recipe (Base-64) 🍅

Uses food and drink emojis starting at Unicode point 0x1F345.

```
Range: 0x1F345 - 0x1F384
Capacity: 64 characters (6 bits per emoji)
Theme: Food and drink emojis
```

### Sample Mapping
```
0  -> 🍅 (TOMATO)
1  -> 🍆 (EGGPLANT)
2  -> 🍇 (GRAPES)
3  -> 🍈 (MELON)
4  -> 🍉 (WATERMELON)
5  -> 🍊 (TANGERINE)
...
63 -> 🎄 (CHRISTMAS TREE)
```

## Light Recipe (Base-128) 🎰

Uses activity and game emojis starting at Unicode point 0x1F3B0.

```
Range: 0x1F3B0 - 0x1F42F
Capacity: 128 characters (7 bits per emoji)
Theme: Activities, games, and entertainment
```

### Sample Mapping
```
0   -> 🎰 (SLOT MACHINE)
1   -> 🎱 (BILLIARDS)
2   -> 🎲 (GAME DIE)
3   -> 🎳 (BOWLING)
4   -> 🎴 (FLOWER PLAYING CARDS)
5   -> 🎵 (MUSICAL NOTE)
...
127 -> 🐯 (TIGER FACE)
```

## Classic Recipe (Base-256) 😀

Uses smiley and emotion emojis starting at Unicode point 0x1F600.

```
Range: 0x1F600 - 0x1F6FF
Capacity: 256 characters (8 bits per emoji)
Theme: Smileys and emotion emojis
```

### Sample Mapping
```
0   -> 😀 (GRINNING FACE)
1   -> 😃 (GRINNING FACE WITH BIG EYES)
2   -> 😄 (GRINNING FACE WITH SMILING EYES)
3   -> 😁 (BEAMING FACE WITH SMILING EYES)
4   -> 😆 (GRINNING SQUINTING FACE)
5   -> 😅 (GRINNING FACE WITH SWEAT)
...
255 -> 🛿 (END RANGE)
```

## Gourmet Recipe (Base-1024) 🤠

Uses extended emoji set starting at Unicode point 0x1F900.

```
Range: 0x1F900 - 0x1F9FF
Capacity: 1024 characters (10 bits per emoji)
Theme: Extended emoji set
```

### Sample Mapping
```
0    -> 🤠 (COWBOY HAT FACE)
1    -> 🤡 (CLOWN FACE)
2    -> 🤢 (NAUSEATED FACE)
3    -> 🤣 (ROLLING ON THE FLOOR LAUGHING)
4    -> 🤤 (DROOLING FACE)
5    -> 🤥 (LYING FACE)
...
1023 -> 🧿 (END RANGE)
```

## Implementation Details

### Unicode Range Selection
Each recipe type uses a specific Unicode range chosen for:
- Continuous character availability
- Visual distinctiveness
- Cross-platform support
- Theme consistency

### Code Implementation
```python
def _initialize_ingredients(self):
    """Initialize encoding maps based on recipe type"""
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
    
    self.emoji_map = {
        i: chr(start_code + i) 
        for i in range(base_size)
    }
```

## Character Availability

### Base-64 (Quick Recipe)
- Complete food/drink emoji set
- Excellent cross-platform support
- High visual recognition
- Limited capacity

### Base-128 (Light Recipe)
- Activity and game emojis
- Good cross-platform support
- Mixed theme consistency
- Moderate capacity

### Base-256 (Classic Recipe)
- Smiley and emotion emojis
- Best cross-platform support
- Strong theme consistency
- Standard capacity

### Base-1024 (Gourmet Recipe)
- Extended emoji set
- Variable cross-platform support
- Mixed theme consistency
- Maximum capacity

## Platform Compatibility

### Considerations
- Terminal support for emoji display
- Font availability
- Unicode version support
- Display width consistency

### Recommended Usage
```python
# Check emoji support
def check_emoji_support():
    test_chars = {
        "quick": "🍅",    # Base-64
        "light": "🎰",    # Base-128
        "classic": "😀",  # Base-256
        "gourmet": "🤠"   # Base-1024
    }
    
    for recipe, char in test_chars.items():
        try:
            print(f"Testing {recipe}: {char}")
        except UnicodeEncodeError:
            print(f"Warning: {recipe} not fully supported")
```

## Usage Examples

### Text Encoding
```python
# Choose recipe based on character range needs
codec = EmojiCodec("classic")  # Base-256 for general text

# Encode text
text = "Hello!"
encoded = codec.encode(text)
print(f"Encoded: {encoded}")  # Uses smiley emojis

# Verify uniqueness
unique_chars = len(set(encoded))
print(f"Unique emojis used: {unique_chars}")
```

### Binary Data
```python
# Use gourmet recipe for binary data
codec = EmojiCodec("gourmet")  # Base-1024 for efficiency

# Encode binary data
with open('file.bin', 'rb') as f:
    data = f.read()
    encoded = codec.encode_binary(data)
```

## Notes and Recommendations

1. **Recipe Selection**
   - Use Quick/Light recipes for human-readable output
   - Use Classic recipe for general purpose encoding
   - Use Gourmet recipe for efficient binary encoding

2. **Platform Support**
   - Test emoji display on target platforms
   - Consider fallback options for limited environments
   - Monitor Unicode version requirements

3. **Performance**
   - Higher bases provide better compression
   - Lower bases offer better compatibility
   - Consider memory usage for large datasets

4. **Future Expansion**
   - Additional emoji ranges possible
   - Custom mapping support planned
   - Extended character set support upcoming

---

*Note: Emoji appearances may vary by platform and font support. Always test encoding/decoding on target platforms.*