import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
# pd.set_option('display.max_columns', None)


def main():
    (list_betters,
     list_events,
     list_placed_bets,
     list_matched_bets) = import_data_from_csv()
    available_bets = get_available_bets(list_placed_bets, list_matched_bets, 1)
    print(available_bets)


def import_data_from_csv():
    list_betters = pd.read_csv('list_betters.csv')
    list_events = pd.read_csv('list_events.csv')
    list_placed_bets = pd.read_csv('list_placed_bets.csv')
    list_matched_bets = pd.read_csv('list_matched_bets.csv')
    return (list_betters,
            list_events,
            list_placed_bets,
            list_matched_bets)


def get_available_bets(list_placed_bets, list_matched_bets, event):
    list_placed_bets = list_placed_bets[list_placed_bets['event'] == event]
    list_placed_bets = calc_stakes_left(list_placed_bets, list_matched_bets)
    mask = ((list_placed_bets['left_to_back'] > 0)
            | (list_placed_bets['left_to_lay'] > 0))
    available_bets = list_placed_bets[mask].sort_values(
        by='implied_probability', ascending=False)
    return available_bets


def calc_stakes_left(list_placed_bets, list_matched_bets):
    list_left_to_back = []
    list_left_to_lay = []
    for index, bet in list_placed_bets.iterrows():
        left_to_back = 0.0
        left_to_lay = 0.0
        mask = list_matched_bets['lay_bet'] == index
        matched_sum = list_matched_bets["lay_stake"][mask].sum()
        mask = list_matched_bets['back_bet'] == index
        matched_sum = matched_sum + list_matched_bets["back_stake"][mask].sum()
        stakes_left = bet['stake'] - matched_sum
        if bet['lay']:
            odds = 1 / (1 - bet['implied_probability'])
            left_to_back = stakes_left * (odds - 1)
        else:
            odds = 1 / bet['implied_probability']
            left_to_lay = stakes_left * (odds - 1)
        list_left_to_back.append(left_to_back)
        list_left_to_lay.append(left_to_lay)
    list_placed_bets['left_to_back'] = list_left_to_back
    list_placed_bets['left_to_lay'] = list_left_to_lay
    return list_placed_bets


# def match_bets(list_placed_bets, list_matched_bets):
#     list_matched_stakes = get_list_matched_stakes(list_placed_bets,
#                                                   list_matched_bets)
#     list_placed_bets = list_placed_bets.merge(list_matched_stakes,
#                                               left_index=True,
#                                               right_index=True)
#     for index, bet in list_placed_bets.iterrows():
#         if bet['stake'] > bet['matched_stakes']:
#             get_available_bets(list_placed_bets, bet['event'])
#             # find_match(bet, list_available_bets)


# def get_list_matched_stakes(list_placed_bets, list_matched_bets):
#     columns = ['matched_stakes']
#     index = list_placed_bets.index

#     list_matched_stakes = pd.DataFrame(0.0, index=index, columns=columns)
#     list_matched_stakes.index.name = 'ref_placed_bet'
#     for index, bet in list_placed_bets.iterrows():
#         if bet['lay']:
#             mask = list_matched_bets['lay_bet'] == index
#             matched_sum = list_matched_bets["lay_stake"][mask].sum()
#             list_matched_stakes.iat[index, 0] = matched_sum
#         else:
#             mask = list_matched_bets['back_bet'] == index
#             matched_sum = list_matched_bets["back_stake"][mask].sum()
#             list_matched_stakes.iat[index, 0] = matched_sum
#     return list_matched_stakes


# def find_match(bet, list_available_bets):
#     if bet['lay']:
#         mask = ((list_available_bets['event'] == bet['event'])
#                 & (list_available_bets['implied_probability']
#                    >= bet['implied_probability']))
#         df = list_available_bets[mask].sort_values(by='implied_probability',
#                                                    ascending=False)
#         print(df)
#     else:
#         mask = ((list_available_bets['event'] == bet['event'])
#                 & (list_available_bets['implied_probability']
#                    <= bet['implied_probability']))
#         df = list_available_bets[mask].sort_values(by='implied_probability',
#                                                    ascending=False)
#         print(df)

#     # print(list_available_bets[mask])


if __name__ == '__main__':
    main()
