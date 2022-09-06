# Abstract
The basic idea of YouNeedAMint is to set up a Mint account linked to your Apple Card to automatically import transactions, and then move those transactions from Mint to YNAB. For some reason, this is easier than simply linking directly from Apple Card to YNAB. If you're a developer from one or both of those companies, please make it happen.

# Prerequisits
**You must set up a new Intuit's Mint account** and link it to the desired bank accounts.
If you use a Mint account with the same email address as any other Intuit product, regardless of whether you link them, you will be required to enter a 2FA code on every login, which makes automatiation more difficult.

If you wish to use a Mint account with enforced 2FA, reference [this page](https://github.com/mintapi/mintapi#mfa-authentication-methods) for more details.

# Installation

Available from PyPi:

```pip install ynam```


Manual install:

```git clone https://github.com/snowskeleton/ynam.git```

```cd ynam```

```pip install --upgrade .```


Then simply

```ynam --quickstart```

You will be asked for a YNAB API key (available from your YNAB settings), and your Mint username and password.
After finishing the quickstart path, ynam will automatically pull all yesterday's transactions.

At this point, check your YNAB budget to make sure the transactions imported as you expect, assign categories, make approvals, etc.

If everything looks good, you're ready to setup the longterm task.
If you just want a sample crontab line, here it is:
```
#m h dom mon dow command
1 1 * * * ynam
```

Note that bank transactions have a granularity of one day, so the specific time of day will not affect the results returned.


A cronjob or other similar scheduler is recommended.
Currently ynam is optimized to be run once per day just after midnight.
Future releases will include more flexability.


Note that the first time running (```ynam quickstart```) is best performed on your local machine, i

Credentials are stored at ```~/.ynamrc```.

You can specify how far back ynam should reach for transactions with the ```--days``` flag, or ```-d```, which takes an integer.
ynam will filter for all transactions on or before the day specified.
For example, a value of 1 returns transations from today and yesterday; a value of 0 returns transactions only from today.
