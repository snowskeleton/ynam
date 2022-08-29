import ynab_api
from ynab_api.api import transactions_api, budgets_api
from utils import YNABTransaction, Secrets, allTransactions
# from config import username, password


def main():
    transactions = allTransactions()
    configuration = ynab_api.Configuration(
        host="https://api.youneedabudget.com/v1")
    configuration.api_key['bearer'] = Secrets.api_key()
    configuration.api_key_prefix['bearer'] = 'Bearer'

    with ynab_api.ApiClient(configuration) as api_client:
        api_instance = transactions_api.TransactionsApi(api_client)
        budgets = budgets_api.BudgetsApi(api_client)
        print(budgets)
        import sys
        sys.exit()

        for transaction in transactions:
            try:
                transaction = YNABTransaction(transaction)
                api_instance.create_transaction(
                    data=transaction.__dict__(),
                    budget_id=Secrets.budget_id())
            except ynab_api.ApiValueError:
                #not actually an error
                pass
            except ynab_api.ApiException as e:
                print("Exception: %s\n" % e)


if __name__ == "__main__":
    main()
