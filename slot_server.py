from flask import Flask, request
import slot_machine
import json

app = Flask(__name__)
machine = slot_machine.create_sample_machine()


@app.route('/spin')
def spin():
    coin_in = int(request.args.get('coin_in'))
    times = int(request.args.get('times'))
    print('debug: times={}'.format(times))
    # planned_stop = request.args.get('stops')

    results = []
    for _ in range(times):
        results.append(slot_machine.spin(machine, coin_in))
    return restfulresult(results)


def to_json(spin_result):
    result_dict = {}

    result_dict['spin_type'] = spin_result.spin_type
    result_dict['coin_in'] = spin_result.coin_in
    result_dict['stop_pos'] = spin_result.stop_pos
    result_dict['symbols'] = spin_result.symbols
    result_dict['line_results'] = spin_result.line_results
    result_dict['scatter_results'] = spin_result.scatter_results

    lr_dicts = []
    for lr in spin_result.line_results:
        ld = {}
        ld['.line_id'] = lr.line_id
        ld['.coin_out'] = lr.coin_out
        lr_dicts.append(ld)
    result_dict['line_results'] = lr_dicts

    sr_dicts = []
    for sr in spin_result.scatter_results:
        scatter_result_dict = {}
        scatter_result_dict['symbol'] = sr.symbol
        scatter_result_dict['count'] = sr.count
        scatter_result_dict['coin_out'] = sr.coin_out
        scatter_result_dict['freespins'] = sr.freespins
        for cr in sr.child_results:
            scatter_result_dict['child_results'] = to_json(cr)
        sr_dicts.append(scatter_result_dict)

    result_dict['scatter_results'] = sr_dicts

    return result_dict


def restfulresult(spin_results):
    results = []
    for r in spin_results:
        results.append(to_json(r))

    rdict = {'results': results}
    return json.dumps(rdict)

    '''
    print('debug: len of results', len(spin_results))
    if len(spin_results) > 1:
        return "{'aaa': 123, 'bbb': 456}"
    else:
        return "{'aaa': 123}"
    '''


if __name__ == '__main__':
    app.run()
