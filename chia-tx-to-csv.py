#!/usr/bin/env python3

'''
Program usage:

chia wallet get_transactions --no-paginate --sort-by-height | python chia-tx-to-csv.py [output.csv]

chia wallet get_transactions --no-paginate --sort-by-height | python chia-tx-to-csv.py > /path/to/output.csv
'''

import datetime as dt # For parsing and reformatting the date strings
import sys
from typing import Optional



def chia_tx_to_csv(tx_output: str, csv_out: Optional[str] = None) -> Optional[str]:
    '''
    Convert a Chia transaction output to a CSV file.
    '''
    lines = tx_output.split('\n')
    # Group 5 lines together at a time
    output = 'Koinly Date,Amount,Currency,Label,TxHash,Fee,ToAddress,FromAddress,TxType\n'
    for i in range(0, len(lines), 6):
        # Get the next 6 lines
        tx = lines[i:i+6]
        if len(tx) < 5:
            break
        # Split 5 lines into the 5 columns
        tx_conf = tx[1].split(': ')[-1] == 'Confirmed'
        if not tx_conf:
            continue
        tx_id = tx[0].split(' ')[-1]
        tx_currency = 'XCH'
        tx_label = \
            'Mining' if 'received' in tx[2] else \
            'Mining (Block Reward)' if 'rewarded' in tx[2] else \
            'Transfer' if 'sent' in tx[2] else \
            'Unknown'
        tx_amount = tx[2].split(': ')[-1].split(' ')[0]
        if tx_label == 'Transfer' and tx_amount != '0':
            tx_amount = '-' + tx_amount
        tx_from_addr = ''
        tx_to_addr = tx[3].split(': ')[-1]
        tx_date = tx[4].split(': ')[-1]
        # Convert date to Koinly date format (MM/DD/YY HH:MM)
        # tx_date = dt.datetime.strptime(tx_date, '%Y-%m-%d %H:%M:%S').strftime('%m/%d/%y %H:%M')
        tx_fee = 0
        tx_type = 0

        if tx_label == 'Mining':
            tx_from_addr = tx_to_addr
            tx_to_addr = ''
        elif tx_label == 'Transfer':
            # tx_to_addr and tx_from_addr is already correctly set
            pass
        elif tx_label == 'Mining (Block Reward)':
            # tx_to_addr and tx_from_addr is already correctly set
            pass

        if 'e-' in tx_amount.lower():
            # Convert to decimal number if in scientific notation
            tx_amount = f'{float(tx_amount):.10f}'

        # Write to the CSV file
        output += f'{tx_date},{tx_amount},{tx_currency},{tx_label},{tx_id},{tx_fee},{tx_to_addr},{tx_from_addr},{tx_type}\n'
    if csv_out is not None:
        with open(csv_out, 'w') as f:
            f.write(output)
    else:
        return output



def main():
    # Read from piped std input
    # tx_output = sys.argv[1]
    tx_output = sys.stdin.read()
    if len(sys.argv) > 1:
        out_csv = sys.argv[1]
    else:
        out_csv = None
    output = chia_tx_to_csv(tx_output, out_csv) # `output` is None if the output is written to a file, or output is a str if there is not file name provided
    if output is not None:
        print(output)



if __name__ == '__main__':
    main()


