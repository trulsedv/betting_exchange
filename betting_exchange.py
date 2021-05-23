import pandas as pd


def main():
    (list_betters,
     list_events,
     list_placed_bets,
     list_matched_bets) = import_data_from_csv()
    list_matched_stakes = get_list_matched_stakes(
                               list_placed_bets, list_matched_bets)


def import_data_from_csv():
    list_betters = pd.read_csv('list_betters.csv')
    list_events = pd.read_csv('list_events.csv')
    list_placed_bets = pd.read_csv('list_placed_bets.csv')
    list_matched_bets = pd.read_csv('list_matched_bets.csv')
    return (list_betters,
            list_events,
            list_placed_bets,
            list_matched_bets)


def get_list_matched_stakes(list_placed_bets, list_matched_bets):
    columns = ['matched staked']
    index = list_placed_bets.index

    list_matched_stakes = pd.DataFrame(0.0, index=index, columns=columns)
    list_matched_stakes.index.name = 'ref placed bet'
    for index, bet in list_placed_bets.iterrows():
        # if bet is a Lay bet
        if bet['lay or back'] == 0:
            mask = list_matched_bets['lay bet'] == index
            matched_sum = list_matched_bets["layer's stake"][mask].sum()
            list_matched_stakes.iat[index, 0] = matched_sum
        else:
            mask = list_matched_bets['back bet'] == index
            matched_sum = list_matched_bets["backer's stake"][mask].sum()
            list_matched_stakes.iat[index, 0] = matched_sum
    return list_matched_stakes


def match_bets(list_placed_bets, list_matched_bets, list_matched_stakes):
    
    

if __name__ == '__main__':
    main()
