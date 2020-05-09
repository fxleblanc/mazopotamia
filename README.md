# Mazopotamia

## Convert base64 encoded maze to numpy array
Put you base64 string in a file and then invoke the `convert_to_maze` script:

```
python convert_to_maze.py encoded.txt
```

Example: You can use the `test_encoded_maze.txt` file to test the converter

### Symbols
- 0: Wall
- 255: Floor
- 74: blue
- 80: red
- 1: start
- 2: end
