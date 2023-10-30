import requests
import subprocess
import configparser

# SECTION - config:
config = configparser.ConfigParser()
config.read('/root/dev/config.ini')

USER_KEY = config.get('Pushover', 'user_key') #NOTE - Your Pushover User key
API_KEY = config.get('Pushover', 'api_key') #NOTE - Your Pushover API key

HOSTNAME = subprocess.run(['hostname'], capture_output=True, text=True) #NOTE - This will automatically determine your hostname (can be changed of course)
#!SECTION


def check_updates(): #NOTE - Check System for updates
    # Update the package list
    subprocess.run(['sudo', 'apt-get', 'update'])

    # Check for upgradable packages
    output = subprocess.check_output(['apt-get', 'upgrade', '-s'])

    # Decode the output to a string
    output = output.decode('utf-8')

    # Filter the lines that start with 'Inst' (for "Install")
    updates = [line for line in output.split('\n') if line.startswith('Inst')]

    return len(updates)


updates_count = check_updates() #NOTE - determines how many updates are available

if updates_count > 0: #NOTE - when updates are available it sends a message to the pushover

    message_title = f"{HOSTNAME.stdout.strip()} -> !!! Updates Verfügbar !!!" #NOTE - can be changed
    message_body = f"Es sind {updates_count} updates verfügbar." #NOTE - can be changed

    requests.post("https://api.pushover.net/1/messages.json", data={
        "token": API_KEY,
        "user": USER_KEY,
        "title": message_title,
        "message": message_body
    })

print(f"Es sind {updates_count} updates verfügbar.") #NOTE - can be omitted, this is for debug purposes only
