from flask import Flask, request
import slot_machine

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


def restfulresult(spin_results):
    print('debug: len of results', len(spin_results))
    if len(spin_results) > 1:
        return "{'aaa': 123, 'bbb': 456}"
    else:
        return "{'aaa': 123}"


if __name__ == '__main__':
    app.run()
