from json import JSONDecodeError
import requests
import time
import datetime

from colorama import Fore, init

# Remove colorama config after each print()
init(autoreset=True)

with open('emails.txt', 'r', encoding='utf-8') as f:
    emails_list = f.read().splitlines()

leaked_emails = []

len_emails_list = len(emails_list)

print(f"Estimated time: {Fore.GREEN}{str(datetime.timedelta(seconds=len_emails_list*5))}\n")

for n, email in enumerate(emails_list):
    if n != 0:
        time.sleep(1)
    print(f"\n{Fore.GREEN}{email}")
    response = requests.get(
        f'https://haveibeenpwned.com/api/v3/breachedaccount/{email.lower()}',
        params={
            'truncateResponse': 'false',
        },
        headers={
            'hibp-api-key': 'fb1701b6e7674975a243c43e5c180f34',
        }
    )
    if response:
        with open('leaks.md', 'w', encoding='utf-8') as f:
            leaks = response.json()
            # print(leaks)
            for leak in leaks:
                # for k, v in leak.items():
                #     print(f"{k}: {v}")
                name = leak["Name"]
                title = leak["Title"]
                domain = leak["Domain"]
                breach_date = leak["BreachDate"]
                pwn_count = leak["PwnCount"]
                print(f"\tLeak: {Fore.YELLOW}{name}")
                print(f"\tTitle: {Fore.CYAN}{title}")
                if domain:
                    print(f"\tDomain: {Fore.CYAN}{domain}")
                print(f"\tBreach Date: {Fore.CYAN}{breach_date}")
                print(f"\tPwn Count: {Fore.CYAN}{pwn_count:,}")
                print()
            leaked_emails.append({email: leaks})
        
    else:
        print(f"\t{Fore.RED}No se han encontrado leaks de este email")
    

with open('leaks.md', 'w', encoding='utf-8') as f:
    f.write("# Leaked Emails\n\n")
    f.write(f"Number of analyzed emails: **{len(emails_list)}**\n\n")
    f.write(f"Number of leaked emails: **{len(leaked_emails)}**\n\n")
    for n, email in enumerate(leaked_emails):
        for k, v in email.items():
            leak_s = "leaks" if len(v) > 1 else "leak"
            f.write(f"#### {n+1}. {k} -> {len(v)} {leak_s}\n\n")
            for n, leak in enumerate(v):
                f.write(f"{n+1}. **{leak['Title']}**\n\n")
                f.write(f"\t- **Name:** {leak['Name']}\n\n")
                f.write(f"\t- **Breach Date:** {leak['BreachDate']}\n\n")
                f.write(f"\t- **Pwn Count:** {leak['PwnCount']:,}\n\n")
                if leak['Domain']:
                    f.write(f"\t- **Domain:** {leak['Domain']}\n\n")
                f.write(f"\t- **Description:** {leak['Description']}\n\n\n\n")