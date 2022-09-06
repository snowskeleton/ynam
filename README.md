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
Credentials are stored at ```~/.ynamrc```.
Be careful about who else has access to your machine, as currently they're stored in plain text

After finishing the quickstart path, ynam will automatically pull the latest days transactions.
Subsequent invocations are as simple as ```ynam```.

A cronjob or other similar scheduler is recommended.
Currently ynam is optimized to be run once per day just after midnight.
Future releases will include more flexability.

Note that the first time running (```ynam quickstart```) is best performed on your local machine, i
