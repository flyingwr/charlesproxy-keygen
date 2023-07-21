from charles_keygen import generate_key

if __name__ == "__main__":
    while not (license_name := input("Enter a name for a Charles Proxy license: ")):
        continue
    
    print(f"License generated.\nName: {license_name} | Key: {generate_key(license_name)}")