# Note
The current version of mintapi/mintapi available from pypi is not compatible with this version of ynam. Install manually from snowskeleton/mintapi. Clone, navigate inside, and run `pip install --upgrade .`


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
## Python/Chrome
Install from PyPi
```
pip install ynam
```
Or directly from github
```
git clone https://github.com/snowskeleton/ynam.git
cd ynam
pip install .
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

To test it out, simple run
```
ynam
```
The first run can take up to a minute to complete. <!-- (more on that [here]()) -->
## Docker 
To run ynam in docker, you'll need to do a bit of setup.

First,
after running through the instructions above once,
ynam will have created `.ynamrc` in your home directory.
This is one of the files you need to link to the docker container.

You also need to create three empty files,
one each for api keys, cookies, and session.
Here, we'll create those files in our home directory

```
touch ~/.ynam_mint_cookies
touch ~/.ynam_mint_api_key
touch ~/.ynam_mint_session
```
then we can
```
docker run \
    -v "$HOME/.ynam_mint_cookies:/root/.ynam_mint_cookies" \
    -v "$HOME/.ynam_mint_api_key:/root/.ynam_mint_api_key" \
    -v "$HOME/.ynam_mint_session:/root/.ynam_mint_session" \
    -v "$HOME/.ynamrc:/root/.ynamrc" \
    -it \
    snowskeleton/ynam
```
# Considerations
- Mint
   - YNAM expects there to only be one account linked in Mint,
   namely your Apple Card.
   If you add additional cards, ynam will post them to YNAB
   all under your Apple Card.
   - Strictly speaking, MFA is not mandatory.
   With that said,
   a number of potential issues can be avoided entirely if you use MFA.
   The simplest method is a software token, from somewhere like
   [Authy](https://apps.apple.com/us/app/twilio-authy/id494168017),
   Any app will do, as long as it lets you export the seed,
   which you then pass to ynam.
   - The link between Mint and your Apple Card will break every ~90 days,
   and you'll have to manually sign in and relink it.

- Chrome
   - Chrome and chromedriver versions have to match.
   By default, ynam always pulls the most up to date chromedriver.
   If your Chrome install is not also up to date,
   logging into Mint will fail.
   For long term deployment,
   you should use the `--use-chromedriver-on-path`
   with a validated chromedriver.
   Alternatively, Docker can handle everything for you.
   This is the recommeneded method.

# Importing Transactions
You should avoid manually entering transations into
YNAB on your Apple Card account.
ynam can sometimes avoid duplicating transactions,
but not in all cases.
ynam adds a unique ID to each transaction it imports,
so it will never duplicate its own transactions

# Closing
I hope you find ynam useful!

Feel free to open an Issue or Pull Request
with any new ideas or problems.

## Disclaimer
This project is neither associated with, nor endorsed by, YNAB, Mint, or Apple. All rights belong to original creators.
