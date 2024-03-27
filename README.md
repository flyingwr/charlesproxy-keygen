## Charles Proxy License Generator for Python
This program generates a valid license key for Charles Proxy using the RC5 algorithm found in its Java source code
### Usage
```py
from charles_keygen import generate_key

if __name__ == "__main__":
    license_name = "dummy"
    key = generate_key(license_name)

    print(f"License generated. Name: {license_name} | Key: {key}")
```
### Output
```
License generated. Name: dummy | Key: 800856A2498358FBBC
```

###### tested on versions 4.6.4, 4.6.5 and 4.6.6 of Charles Proxy