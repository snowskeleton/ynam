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
- New Intuit's [Mint](https://accounts.intuit.com/signup.html) account.
- Dedicated [YNAB API key](https://app.youneedabudget.com/settings/developer),
and unlinked credit account
- Chrome or chromium
- (Recommended) Docker 
- (Recommended) MFA soft token
# Usage
## Pip/PyPi
Install from PyPi
```
pip install ynam
```
Or directly from github
```
pip install git+https://github.com/snowskeleton/ynam
```
Go through the quickstart process
```
$ ynam --quickstart
Mint username: 
Mint password: 
Mint mfa seed (optional): 
YNAB API key: 
YNAB budget...
YNAB account... 
```
ynam will login to YNAB and have you select from among the budgets and accounts listed

To test it out, simply run
```
ynam
```
The first run can take up to a minute to complete.
Run with `-x` to see what's happening! <!-- (more on that [here]()) -->
## Docker 
First complete the `--quickstart` process,
passing ynam's config directory as a volume mount.
```
docker run -v "$HOME/.ynam:/root/.ynam" -it snowskeleton/ynam --quickstart
```
Subsequent runs should use:
```
docker run -v "$HOME/.ynam:/root/.ynam" -it -d snowskeleton/ynam
```
Note the inclusion of `-d`,
which runs the image in detached mode.

Run with your preferred scheduler.
I use cron.
# Considerations
- Mint
   - ynam expects that you will have one card,
   and only one card,
   linked to Mint.
   ynam does not differentiate between different cards,
   and thus assumes that all transactions present are for the same card.

   - [Enable MFA for your Intuit account](https://accounts.intuit.com/app/account-manager/security/mfa).
   The simplest and least fragiile method is a software token,
   which you should backup in an app like
   [Authy](https://apps.apple.com/us/app/twilio-authy/id494168017).
   When linking an app,
   you will have the option to view the secret as text instead of as a QR code.
   Run `ynam --quickstart` and paste that text when prompted for mfa seed.
   Automated login with SMS and/or email MFA is not supported by ynam.
   Strictly speaking,
   MFA is not mandatory.
   With that said,
   enabling MFA prevents entire categories of automation issues,
   and is thus strongly recommended.

   - Mint's link to your Apple Card will break every ~90 days.
   You must manually sign in to Mint and relink it.

- Chrome
   - Chrome and chromedriver versions must match.
   Docker will handel this process automatically,
   but simpler deployments not using Docker must match versions manually.
   Use `--use-chromedriver-on-path` to pass in a working chromedriver,
   and ensure Chrome does not auto update.

# Importing Transactions
Avoid manually entering your Apple Card transations
ynam can sometimes detect that you manually enterd a charge and not overwrite it,
but not in all cases.
ynam adds a unique ID to each transaction it imports,
so it will never duplicate its own transactions

## Structure of config file
ynam requires a few pieces of info to do its job.
Specifically, it requires:
- YNAB API key
   - This comes from your YNAB account's [developer settings](https://app.youneedabudget.com/settings/developer),
- Selected YNAB budget
   - Most people will only have a single budget, which ynam will select by default.
   If you have more, the quickstart process will prompt you to select one.
- Apple Card account ID
   - The specific ID of your Apple credit card.
   This is unique to the budget selected above.
   If you want to use ynam to import transactions from multiple Apple cards or into multiple YNAB budgets,
   specify each combination with sparate credentials using the `--config-file` option.
- Mint
   - Username
   - Password
   - MFA soft token seed
      - it is HIGHLY RECOMMENDED that you provide this value.
      Not only is it the most secure option,
      but it's also the least fragile.
      Opting to not use MFA,
      or to use email or SMS MFA,
      will increase the amount of login failures you experience.
      Setup is as follows:
         - Go to your 
         [Intuit account MFA settings](https://accounts.intuit.com/app/account-manager/security/mfa)
         (login if necessary)
         - If you already have an MFA app linked to your account,
         go through the process of unlinking it
         - Start adding an authenticator app of your choice,
         but DO NOT click all the way through yet.
         - You will receive a QR code,
         as well as a short string representation of that QR code.
         This is your MFA seed.
         Save it somewhere safe (password manager, lockbox, etc)
         before you finish linking the app.

# Closing
I hope you find ynam useful!

Feel free to open an Issue or Pull Request
with any new ideas or problems.

## Disclaimer
This project is neither associated with, nor endorsed by, YNAB, Intuit (or its subsidiary Mint), or Apple. All rights belong to original creators.
