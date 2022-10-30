# Note
The current version of mintapi/mintapi available from pypi is not compatible with this version of ynam. Install manually from snowskeleton/mintapi by cloning, navigating inside, and running `pip install --upgrade .`.


# Abstract
ynam is a commandline utility
to import transactions from an Apple Card into YNAB.
ynam achieves this by using an intermediary,
namely Intuit's Mint,
who happens to be able to import Apple Card transactions.
For some reason,
this is easier than simply linking an Apple Card directly to YNAB.
If you're a developer from either one of these companies,
please make this project obsolete.

# Prerequisites
 - Intuit's Mint account linked to your Apple Card.
    - Your Apple Card should be the ONLY linked
    account in order to prevent importing other transactions.
    Many email providers, including gmail,
    support adding a new account using the format:
    `<originalusername>+<anystring>@<domain>` (notice the plus + )
    - (Recommended) Link an MFA app with Mint.
    Choose one that lets you export the seed, and pass that seed to ynam.
 - Unique YNAB API key.
    - Sign in to the YNAB web app and go to
    `Account Settings > Developer Settings > Personal Access Tokens`
    and click New Token.
    Follow the prompts.
    (Copy the key now, as it will only be displayed once.)
 - Chrome or chromium, and chromedriver.
   - install with `apt install google-chrome-browser chromedriver` or similar.
   - NOTE: if running in Docker, this step is not necessary.
 - Unlinked Apple Card account in YNAB.
    - Choose Add Account, Unlinked.
    - Name the account whatever you'd like and set its type to 'Credit Card'.
    Also make sure the current balance is correct,
    otherwise everything will be confused later.

# Installation

Available from PyPi:
```
pip install ynam
```
Or, for the freshest version:
```
git clone https://github.com/snowskeleton/ynam.git
cd ynam
pip install --upgrade .
```
# Secrets
ynam accepts authentication details
either from a file or as arguments on the command line.

From a file (default):
```
ynam --config-file-path /path/to/credentials
```
(if no path is specified,
ynam defaults to using `$HOME/.ynamrc`)

From command line:
```
ynam \
   --api-key-literal "API key as string" \
   --budget-id "YNAB budget id" \
   --account-id "YNAB account ID (this is your Apple Card)" \
   --username "mint username" \
   --mfa-seed "MFA token seed" \
   --password "mint password"
```


# Importing Transactions
ynam will smartly import only transactions
it determines to be unique.
This allows you to manually enter a transaction in YNAB
without worrying that ynam will duplicate the data.

The recommended longterm setup is to
schedule a cron job for some regular interval,
such as every 15 minutes,
that runs `ynam` (see [ example ](#crontab-example) below). 
# chromium crashes
Just try it again.
I have ynam on a 15 minute schedule
and I get about one crash per day,
Usually a 401 HTTP error that goes
away with subsequent runs

# Closing
I hope you find ynam useful!

Feel free to open an Issue or Pull Request
with any new ideas or problems.

## Disclaimer
This project is neither associated with, nor endorsed by, YNAB. All rights belong to original creators.
