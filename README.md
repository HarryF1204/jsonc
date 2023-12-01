# JSONC


## Overview
**JSONC** is a python module to encode and decode json comments. It allows you to work with JSON files that include
both single and double line comments without loosing them. This allows you to create more human-readable JSON files.

## Features
- **Comment Support:** This module allows you to include single, and double line comments in JSON code.
- **Encoding and Decoding:** The module uses the built-in JSON library to parse JSON after the comments have been
formatted.
- **File Operations:** This module allows reading and writing JSONC to/from files.

<br></br>

----


## Usage
### JSONC to Python Dictionary
```python
import jsonc

# Note that in JSON, single line comments require a new line after to be parsed
data = '''{
    "name": "Harry" // defines name
}'''

# loads(tring) allows you to parse a JSONC string
# load is a similar function taking the same parameters that allows you to load JSONC from a file
# to a pythondictionary
jsonData = jsonc.loads(data)
print(jsonData)
print(type(jsonData))




# OUTPUT: 
{'name': 'Harry', '__comment_22_38': {'__comment_content': '// defines name\n', '__is_inline': True}}
<class 'dict'>

```

### Python Dictionary to JSONC
```python
import jsonc

jsonData = jsonc.load(filePath)
# As the JSONC is loaded as a dictionary, it is very simple to edit
jsonData['name'] = 'Bill'

jsonCData = jsonc.dumps(jsonData)
print(jsonCData)



# OUTPUT
{
    "name": "Bill" // defines name
}
```




<br></br>


---

# Known Issues

- 
