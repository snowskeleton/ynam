# Abstract
The basic idea of YouNeedAMint is to set up a Mint account linked to your Apple Card to automatically import transactions, and then move those transactions from Mint to YNAB. For some reason, this is easier than simply linking directly from Apple Card to YNAB. If you're a developer from one or both of those companies, please make it happen.

# Installation
Ensure your have a recent version of Python installed.

For an automated install, run 

```curl -l https://raw.githubusercontent.com/snowskeleton/ynam/master/remote_install.sh > i.sh && bash i.sh```

Or manually like:

```git clone https://github.com/snowskeleton/ynam.git```

```cd ynam```

```./install.sh```


Then simply

```ynam quickstart```
