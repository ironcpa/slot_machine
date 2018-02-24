import json


data = {
    'id': 9999,
    'name': 'aaa',
    'sub_data': [
        {'date': '2015-03-11', 'item': 'subdata1'},
        {'date': '2015-03-11', 'item': 'subdata1'},
    ],
    'reels': [
        [1, 2, 3, 4, 5],
        [1, 2, 3, 4, 5]
    ]
}

print('debug:', data['reels'])
print('debug:', data['reels'][0])

# dict to json string
json_str = json.dumps(data)

print(json_str)
print(type(json_str))


dict_slot = {
        'reel_heights': [3, 3, 3, 3, 3],
        'symboldefs': [
            {'code': 'W', 'is_wild': True},
            {'code': 'A', 'is_wild': False},
            {'code': 'B', 'is_wild': False},
            {'code': 'C', 'is_wild': False},
            {'code': 'D', 'is_wild': False},
            {'code': 'E', 'is_wild': False},
            {'code': 'S', 'is_wild': False},
        ],
        'paytables': [
            {'symbol': 'A', 'match': 4, 'payout': 50},
            {'symbol': 'A', 'match': 3, 'payout': 20},
            {'symbol': 'B', 'match': 5, 'payout': 80},
            {'symbol': 'B', 'match': 3, 'payout': 40},
            {'symbol': 'B', 'match': 2, 'payout': 10},
            {'symbol': 'C', 'match': 5, 'payout': 30},
            {'symbol': 'C', 'match': 4, 'payout': 20},
            {'symbol': 'C', 'match': 3, 'payout': 10},
            {'symbol': 'D', 'match': 5, 'payout': 20},
            {'symbol': 'D', 'match': 4, 'payout': 10},
            {'symbol': 'D', 'match': 3, 'payout': 5},
            {'symbol': 'E', 'match': 5, 'payout': 20},
            {'symbol': 'E', 'match': 4, 'payout': 10},
            {'symbol': 'E', 'match': 3, 'payout': 5},
        ],
        'scatter_paytables': [
            {'symbol': 'S', 'match': 3, 'type': 'freespin', 'reward': 3}
        ],
        'paylines': [
            [0, 0, 0, 0, 0],
            [2, 2, 2, 2, 2],
            [0, 1, 1, 1, 2],
            [2, 1, 1, 1, 0],
            [0, 0, 0, 1, 2],
            [2, 1, 0, 0, 0],
            [0, 0, 1, 2, 2],
            [2, 2, 1, 0, 0],
        ],
        'reels': [
            ['W', 'A', 'B', 'C', 'D', 'E', 'S'],
            ['W', 'A', 'B', 'C', 'D', 'E'],
            ['W', 'A', 'B', 'C', 'D', 'E', 'S'],
            ['W', 'A', 'B', 'C', 'D', 'E'],
            ['W', 'A', 'B', 'C', 'D', 'E', 'S']
        ],
        'free_reels': [
            ['S', 'W', 'A', 'B', 'C', 'D', 'E'],
            ['S', 'W', 'A', 'B', 'C', 'D', 'E'],
            ['S', 'W', 'A', 'B', 'C', 'D', 'E'],
            ['S', 'W', 'A', 'B', 'C', 'D', 'E'],
            ['S', 'W', 'A', 'B', 'C', 'D', 'E']
        ]
}
