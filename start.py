import threading
import time

from binance.client import Client
from config import desired_price


def get_key_lists():
    keys_list = []
    with open("api_keys.txt", "r") as file_:
        for row in file_:
            keys_list.append({"api_key": row.split(" ")[0], "secret_key": row.split(" ")[1]})
    return keys_list


def check_balance_and_cell(curr_api_key, curr_secret_key):
    current_client = Client(curr_api_key, curr_secret_key)
    arb_balance = float(current_client.get_asset_balance(asset='ARB')['free'])
    price = float(current_client.get_symbol_ticker(symbol='ARBUSDT')["price"])

    print(f"На аккаунте {curr_api_key}  монет {arb_balance}  ")

    # Ждем пополнения
    while arb_balance == 0:
        pass

    if arb_balance != 0:
        print(f"На аккаунте {curr_api_key} появились монеты  ")

        while price <= desired_price:
            pass
        # Продаем по нужной цене
        order = current_client.order_market_sell(symbol='ARBUSDT', quantity=arb_balance)
        print(f"Продажа {arb_balance} монет ARB в USDT на аккаунте {curr_api_key} завершена.")


def main():
    threads = []
    accounts = get_key_lists()
    for account in accounts:
        thread = threading.Thread(target=check_balance_and_cell, args=(account['api_key'], account['secret_key']))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
        time.sleep(3)


if __name__ == '__main__':
    main()
