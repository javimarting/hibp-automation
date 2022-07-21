import requests
import time
import datetime
import argparse

from colorama import Fore, init
from md2pdf.core import md2pdf


# Remove colorama config after each print()
init(autoreset=True)

parser = argparse.ArgumentParser(description='Have I Been Pwned automation')
parser.add_argument('-i', '--input', type=str, help='Input file', required=True)
parser.add_argument('-o', '--output', type=str, help='Output file')
args = parser.parse_args()

with open(args.input, 'r', encoding='utf-8') as f:
    emails_list = f.read().splitlines()

leaked_emails = []

len_emails_list = len(emails_list)

print(f"\nEstimated time: {Fore.GREEN}{str(datetime.timedelta(seconds=len_emails_list*2))}")

for n, email in enumerate(emails_list):
    if n != 0:
        time.sleep(2)
    print(f"\n-> {Fore.GREEN}{email}")
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
        print(f"{Fore.RED}No se han encontrado leaks de este email")
    
if args.output:
    md_file = f'{args.output}.md'
    with open(md_file, 'w', encoding='utf-8') as f:
        # md_content = f'''
        # # Leaked Emails\n\nNumber of analyzed emails: **{len(emails_list)}**\n\n
        # Number of leaked emails: **{len(leaked_emails)}**\n\n
        # '''
        f.write("# Leaked Emails\n\n")
        f.write(f"Number of analyzed emails: **{len(emails_list)}**\n\n")
        f.write(f"Number of leaked emails: **{len(leaked_emails)}**\n\n")
        for n, email in enumerate(leaked_emails):
            for k, v in email.items():
                leak_s = "leaks" if len(v) > 1 else "leak"
                # md_content += f"### {n+1}. **{k}** -> {len(v)} {leak_s}\n\n"
                f.write(f"### {n+1}. **{k}** -> {len(v)} {leak_s}\n\n")
                for n2, leak in enumerate(v):
                    # md_content += f'''
                    # {n2+1}. **{leak['Title']}**\n\n\t- **Name:** {leak['Name']}\n\n
                    # \t- **Breach Date:** {leak['BreachDate']}\n\n\t- **Pwn Count:** {leak['PwnCount']:,}\n\n
                    # '''

                    f.write(f"{n2+1}. **{leak['Title']}**\n\n")
                    f.write(f"\t- **Name:** {leak['Name']}\n\n")
                    f.write(f"\t- **Breach Date:** {leak['BreachDate']}\n\n")
                    f.write(f"\t- **Pwn Count:** {leak['PwnCount']:,}\n\n")
                    if leak['Domain']:
                        # md_content += f"\t- **Domain:** {leak['Domain']}\n\n"
                        f.write(f"\t- **Domain:** {leak['Domain']}\n\n")
                    # md_content += f"\t- **Description:** {leak['Description']}\n\n\n\n"
                    f.write(f"\t- **Description:** {leak['Description']}\n\n\n\n")
                    
    md2pdf(f"{args.output}.pdf",
           md_file_path=md_file)
