# import slot_data
import re
from slot_data import Symbol, Payline, Paytable, ScatterPaytable, \
                      BetRange, ReelData


# try to find a way to tokenize [xxx] ... before next [xxx] sections
#  - re.split can't get section title
#  - re.findall with section pattern can't get section body
#  - check section title while iterating lines is a better way???
#    - if code is readable, i think it's ok
#    - cuz tokenizing require reading concept to code readers
#      - like map_of_sections = get_tokenize_sections(file)

p_sec_title = r'\[.+\]'
COMMENT = '#'


def is_section_title(line):
    return re.search(p_sec_title, line)


def get_section_data(section, line):
    """return single or list from single line"""
    if section == '[layout]':
        return parse_layout(line)
    elif section == '[symbols]':
        return parse_symbol(line)
    elif section == '[paylines]':
        return parse_payline(line)
    elif section == '[paytables]':
        return parse_paytable(line)
    elif section == '[scatter paytables]':
        return parse_scatter_paytable(line)
    elif section == '[reels]':
        return parse_reels(line)
    elif section == '[bets]':
        return parse_bets(line)


def is_quote(char):
    return char in ('\'', '"')


def tokenize(delimiters, text):
    """
    usage : tokenize(' :', text)
    """

    tokens = []
    collecting = False
    quoting = False
    token = ''

    collecting = text[0] not in delimiters
    for c in text:
        if c in delimiters and not quoting:
            if collecting and token:
                tokens.append(token)
            collecting = True
            token = ''
        else:
            if quoting:
                if is_quote(c):
                    quoting = False
            else:
                if is_quote(c):
                    quoting = True

            if collecting and not is_quote(c):
                token += c
    if collecting and token:
        tokens.append(token)

    return tokens


def parse_layout(line):
    return tuple(int(e) for e in line.split())


def parse_symbol(line):
    # split = (t.replace("'", "") for t in re.findall(r"[\w\-]+|'.*?'", line))
    # return Symbol2(*split)
    id, code, desc, type, buckspoint = tokenize(' :', line)
    return Symbol(int(id), code, desc, type)


def parse_payline(line):
    return Payline(*(int(e) for e in tokenize(' :', line)))


def parse_paytable(line):
    tokens = tokenize(' :', line)

    paytables = []

    symbol = tokens[0]
    payouts = tokens[1:]
    for i, e in enumerate(payouts):
        match = i+1
        paytables.append(Paytable(symbol, match, int(e)))

    return paytables


def parse_scatter_paytable(line):
    symbol, count, type, reward = tokenize(' :', line)
    return ScatterPaytable(symbol, int(count), type, int(reward))


def parse_reels(line):
    return tokenize(' :\t', line)


def parse_bets(line):
    return BetRange(*(int(e) for e in tokenize(' :\t', line)))


def parse_reeldata(reel_data):
    reeldatas = {}
    cur_reel_name = ''
    row_checker = 0
    for e in reel_data:
        if e[0] == 'reelname':
            cur_reel_name = e[1]
            reeldatas[cur_reel_name] = ReelData(cur_reel_name)
            row_checker = 0
        else:
            row = e.pop(0)
            if row == row_checker:
                print('>>> invalid row')
            symbol_pairs = zip(e[::2], e[1::2])

            for reel, d in enumerate(symbol_pairs):
                symbol = d[0]
                weight = int(d[1])
                if symbol != '-':
                    reeldatas[cur_reel_name].add_symbol(reel, symbol, weight)

            row_checker += 1

    return reeldatas


def get_machine(file):
    machine_data = {}

    line_no = 0
    section = ''
    section_data = []
    is_collecting = False

    with open(file, 'rt') as f:
        for l in f:
            line = l.strip()
            line_no += 1

            # print(line_no, line)

            if not line:
                continue
            if line.startswith(COMMENT):
                continue

            if is_section_title(line):
                if is_collecting:
                    # save prev section data
                    # machine_data[section] = content
                    machine_data[section] = section_data

                # start new section collect
                section = line
                section_data = []
                is_collecting = True
            else:
                if is_collecting:
                    # content += line
                    parsed = get_section_data(section, line)
                    if section != '[reels]' and type(parsed) is list:
                        for e in parsed:
                            section_data.append(e)
                    else:
                        section_data.append(parsed)
                else:
                    print('>>> unparsed:', line)

    if section and len(section_data) > 0:
        machine_data[section] = section_data

    '''
    for k, v in machine_data.items():
        print(k)
        print('\t', v[:20])
    '''

    reel_section_data = parse_reeldata(machine_data['[reels]'])
    machine_data['[reels]'] = reel_section_data

    return machine_data


if __name__ == '__main__':
    # get_machine('machines/template.txt')
    get_machine('machines/diamond_rush.opt')
