import pandas as pd


def main():
    (list_betters,
     list_events,
     list_placed_bets,
     list_matched_bets) = import_data_from_csv()

    print(list_matched_bets)


def import_data_from_csv():
    list_betters = pd.read_csv('list_betters.csv')
    list_events = pd.read_csv('list_events.csv')
    list_placed_bets = pd.read_csv('list_placed_bets.csv')
    list_matched_bets = pd.read_csv('list_matched_bets.csv')
    return list_betters, list_events, list_placed_bets, list_matched_bets


if __name__ == '__main__':
    main()
