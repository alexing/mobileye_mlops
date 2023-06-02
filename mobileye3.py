"""
Your monthly phone bill has just arrived, and it's unexpectedly large. You decide to verify the amount by recalculating the bill based on your phone call logs and the phone company's charges.
The logs are given as a string S consisting of N lines separated by end-of-line characters (ASCII code 10). Each line describes one phone call using the following format:
"hh:mm:ss,nnn-nnn-nnn", where "hh:mm:ss"  denotes the duration of the call (in "hh" hours, "mm" minutes, and "ss" seconds) and "nnn-nnn-nnn" denotes the 9-digit phone number of the recipient (with no leading zeros).
Each call is billed separately. The billing rules are as follows:
    - If the call was shorter than 5 minutes, then you pay 3 cents for every started second of the call (e.g. for duration "00:01:07" you pay 67 * 3 = 201 cents).
    - If the call was at least 5 minutes long, then you pay 150 cents for every started minute of the call (e.g. for duration "00:05:00" you pay 5 * 150 = 750 cents and for duration "00:05:01" you pay 6 * 150 = 900 cents).
    - All calls to the phone number that has the longest total duration of calls are free. In the case of a tie, if more than one phone number shares the longest total duration, the promotion is applied only to the phone number whose numerical value is the smallest among these phone numbers.
Write a function:
    def solution(S)
that, given a string S describing phone call logs, returns the amount of money you have to pay in cents.
For example, given string S with N = 3 lines:
  "00:01:07,400-234-090
   00:05:01,701-080-080
   00:05:00,400-234-090"
the function should return 900 (the total duration for number 400-234-090 is 6 minutes 7 seconds, and the total duration for number 701-080-080 is 5 minutes 1 second; therefore, the free promotion applies to the former phone number).
Assume that:
    - N is an integer within the range [1...100];
    - every phone number follows the format "nnn-nnn-nnn"strictly; there are no leading zeros;
    - the duration of every call follows the format "hh:mm:ss" strictly (00 ≤ hh> ≤ 99, 00 ≤ mm, ss ≤ 59);
    - each line follows the format "hh:mm:ss,nnn-nnn-nnn" strictly; there are no empty lines and spaces.
In your solution, focus on correctness. The performance of your solution will not be the focus of the assessment.
"""


def solution(S: str) -> int:
    log_entries = S.split()

    # get all durations in seconds
    seconds_by_phone_numbers = {}
    for log_entry in log_entries:
        time, phone_number = log_entry.split(',')
        seconds = int(time[0:2]) * 3600 + int(time[3:5]) * 60 + int(time[6:8])
        if phone_number in seconds_by_phone_numbers:
            seconds_by_phone_numbers[phone_number] += seconds
        else:
            seconds_by_phone_numbers[phone_number] = seconds

    # find the number that's not billed (the one with the most seconds)
    max_seconds = 0
    max_phone_number_numerical_value = 0
    max_phone_number = ""
    for phone_number, seconds in seconds_by_phone_numbers.items():
        phone_number_numerical_value = int(phone_number.replace('-', ''))
        if seconds > max_seconds:
            max_phone_number = phone_number
            max_phone_number_numerical_value = phone_number_numerical_value
            max_seconds = seconds
        if seconds == max_seconds and phone_number_numerical_value < max_phone_number_numerical_value:
            max_phone_number = phone_number
            max_phone_number_numerical_value = phone_number_numerical_value

    # evaluate phone bill cost
    # - If the call was shorter than 5 minutes, then you pay 3 cents for every started second of the call
    # - If the call was at least 5 minutes long, then you pay 150 cents for every STARTED minute of the call
    # - All calls to the phone number that has the longest total duration of calls are free.
    total_phone_bill_cost = 0
    for phone_number, seconds in seconds_by_phone_numbers.items():
        if phone_number == max_phone_number:
            continue
        if seconds < 300:
            total_phone_bill_cost += seconds * 3
        else:
            total_phone_bill_cost += (seconds // 60) * 150
            if seconds % 60:
                total_phone_bill_cost += 150

    return total_phone_bill_cost


if __name__ == "__main__":
    S = """00:01:07,400-234-090
        00:05:01,701-080-080
        00:05:00,400-234-090
        """
    assert solution(S) == 900
