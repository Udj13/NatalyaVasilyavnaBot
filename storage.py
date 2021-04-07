import sqlite3

from transaction_class import Transaction


# CREATE TABLE Transactions (
#     [key]             INT    PRIMARY KEY,
#     pp_num            STRING,
#     pp_name_of_client STRING,
#     pp_inn            STRING,
#     pp_summ           STRING,
#     pp_info           STRING
# );
#
# TransactionsOOO
# TransactionsIP


class Storage:
    db = None
    cur = None

    def __init__(self):
        self.db = sqlite3.connect('nv-bot.db')
        self.cur = self.db.cursor()

    def close(self):
        self.db.commit()
        self.db.close()

    def check_new_ip_transactions(self, transactions):
        return self.check_new_transactions(transactions, "TransactionsIP")

    def check_new_ooo_transactions(self, transactions):
        return self.check_new_transactions(transactions, "TransactionsOOO")

    def check_new_transactions(self, transactons, table_name):
        new_transactions = []
        for t in transactons:
            if self.check_and_storage_transaction(t, table_name):
                new_transactions.append(t)
        return new_transactions

    def check_and_storage_transaction(self, transaction: Transaction, table_name):
        result = False

        self.cur.execute(f"SELECT * FROM {table_name} WHERE pp_num={transaction.pp_num} and pp_inn={transaction.pp_inn}")

        if self.cur.fetchone() is None:
            self.cur.execute(
                f"INSERT INTO {table_name} (pp_num, pp_name_of_client, pp_inn, pp_summ, pp_info) VALUES ('{transaction.pp_num}', '{transaction.pp_name_of_client}', '{transaction.pp_inn}', '{transaction.pp_summ}', '{transaction.pp_info}')"
            )
            result = True

        return result
