# Note
The current version of mintapi/mintapi available from pypi is not compatible with this version of ynam. Install manually from snowskeleton/mintapi by cloning, navigating inside, and running `pip install --upgrade .`.


# Abstract
ynam is a commandline utility to import transactions from an Apple Card into YNAB.
ynam achieves this by using an intermediary, namely Intuit's Mint, who happens to be able to import Apple Card transactions.
For some reason, this is easier than simply linking an Apple Card directly to YNAB.
If you're a developer from one or both of these companies, please make ynam obsolete.

# Prerequisites
 - New Intuit's Mint account with your Apple Card linked.
    - This account should ONLY be linked to your Apple Card to prevent importing other transactions. If you use gmail, you can create a new account using `gmailusername+ynam@gmail.com`.
    - Leaving MFA disabled is recommended, but, if want need to use MFA, see [here](#mint-mfa)
 - YNAB API key.
    - Sign in to the YNAB web app and go to the "Account Settings" page and then to the "Developer Settings" page.
    - Under the "Personal Access Tokens" section, click "New Token", enter your password and click "Generate" to get an access token.
    - Make sure to save it, as it will only be displayed once.
 - Apple Card Account in YNAB.
    - Choose Add Account, then Unlinked.
    - Name the account 'Apple Card', set type to 'Credit Card', and set current account balance to the one shown in Wallet.

# Installation

Available from PyPi:
```
pip install ynam
```
Or for the freshest version:
```
git clone https://github.com/snowskeleton/ynam.git
cd ynam
pip install --upgrade .
```
Then simply:
```
ynam --quickstart
```

Enter YNAB API key and Mint username and password when prompted. Choose the proper budget and Apple Card account when prompted.
All will be saved to `~/.ynamrc` for later use by ynam.

Hurray! Now we're ready to start importing transactions!

# Importing Transactions
For a first time import, run ynam with the `--days` integer argument for however far back you care to.
You may also need to pass the `--graphics` flag the first time ynam is run in order to enter an MFA code (sent to email by default).
The first browser session is saved for subsequent runs, but if you're having issues, check [ here ](#mint-mfa).

The recommended longterm setup is to schedule a cron job for midnight that runs `ynam` (see [ example ](#crontab-example) below). 
If you can think of some other way you'd like this to work, feel free to file an Issue or open a Pull Request.

# crontab example
An example crontab entry that runs every day at 00:00, or midnight.
You may need to specify `--config-file-path` and/or `--mint-session-path` in the command, or amend your path to ensure cron can find them.
```
#m h dom mon dow command
0 0 * * * ynam
```
## Mint MFA
If you use a Mint account with the same email address you use for any other Intuit product, you will be required to enter a 2FA code on every login.
Use a unique email address and password to ensure you're not forced to use MFA for every login.

If you wish to use a Mint account with enforced 2FA, reference [this page](https://github.com/mintapi/mintapi#mfa-authentication-methods) for further instructions.

## chromium crashes
This happens a lot. Just try it again. It usually works after a few attempts.
I'm still not sure how to handle when it crashes with cron
