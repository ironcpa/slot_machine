import net_slot_machine
# import slot_ui

'''
machine = slot_machine.create_sample_machine()
window = slot_ui.SlotMachineWidget(machine.reel_heights,
                                   machine.paylines)
                                   '''


if __name__ == '__main__':
    '''
    how to make thin client?
     - create net-machine module
     - net-machine module provide belows
      - interface functions to consumers(client code)
      - import local-machine to use exiting data and functions
    '''
    result = net_slot_machine.spin(100)
    print(result)

    results = net_slot_machine.spins(100, 5)
    print(results)
