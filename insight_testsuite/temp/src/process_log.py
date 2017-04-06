import os
import sys
from datetime import datetime, timedelta
import bisect
import operator


def feature_1(hosts, host):
    if host in hosts:
        hosts[host] += 1
    else:
        hosts[host] = 1


def feature_2(bandwidths, resource, bytes_size):
    if resource in bandwidths:
        bandwidths[resource] += bytes_size
    else:
        bandwidths[resource] = bytes_size


def feature_3(times, time, time_zone):
    dt_time = datetime.strptime(time[1:] + time_zone[:-1], '%d/%b/%Y:%H:%M:%S%z')
    times.append(dt_time)


def feature_4(blocked_attempts, attempts, log, host, time, time_zone, reply_code):
    time = datetime.strptime(time[1:] + time_zone[:-1], '%d/%b/%Y:%H:%M:%S%z')
    if host in attempts and attempts[host][1]:
        time_plus_5m = attempts[host][0][2] + timedelta(minutes=5)
        if time < time_plus_5m:
            blocked_attempts.append(log)
        else:
            attempts[host][1] = False
    else:
        time_minus_20s = time - timedelta(seconds=20)
        if reply_code == str(401):
            if host in attempts:
                error_times = attempts[host][0]
                error_times.append(time)
                if len(error_times) == 3:
                    if error_times[0] < time_minus_20s:
                        error_times.pop[0]
                    else:
                        attempts[host][1] = True
            else:
                attempts[host] = [[time], False]
        elif host in attempts:
                attempts.pop(host)


def print_most_active(hosts, directory):
    max_log_file = open(directory, 'w')
    for _ in range(0, min(len(hosts), 10)):
        max_key, max_value = max(hosts.items(), key=lambda p: p[1])
        max_log_file.write(max_key + "," + str(max_value) + "\n")
        hosts.pop(max_key)
    max_log_file.close()


def print_most_bandwidth(bandwidths, directory):
    max_bandwidth_file = open(directory, 'w')
    max_bandwidth = []
    iterations = min(len(bandwidths), 10)
    for _ in range(0, iterations):
        max_key, __ = max(bandwidths.items(), key=lambda p: p[1])
        max_bandwidth.append(max_key)
        bandwidths.pop(max_key)
    max_bandwidth.sort()
    for resource in max_bandwidth:
        max_bandwidth_file.write(resource + "\n")
    max_bandwidth_file.close()


def print_busiest_time(times, directory):
    print("working on 3")
    busiest_times_file = open(directory, 'w')
    times.sort()
    most_busiest = []
    min_occurrences = 0
    for i in range(0, len(times)): #for every time in the log
        if i is not len(times) - 1: #if it's not the last one
            time_difference = times[i+1] - times[i]
            iterations = time_difference.seconds
            for j in range(0, iterations): #for every non-event time
                incremented_time = times[i] + timedelta(seconds=j)
                hour_from_time = incremented_time + timedelta(hours=1)
                hour_index = bisect.bisect(times, hour_from_time, i, len(times))
                occurrences = hour_index - i
                if j != 0:
                    occurrences -= 1
                if incremented_time not in most_busiest:
                    if occurrences > min_occurrences:
                        if len(most_busiest) < 10:
                            most_busiest.append([occurrences, incremented_time])
                        else:
                            most_busiest[-1] = [occurrences, incremented_time]
                        most_busiest.sort(key=operator.itemgetter(1, 0))
                        if len(most_busiest) == 10:
                            min_occurrences = most_busiest[9][0]
        elif times[i] not in most_busiest:
            if len(most_busiest) < 10 and (1 > min_occurrences):
                most_busiest.append([1, times[i]])
    for i in range(0, len(most_busiest)):
        busiest_times_file.write("{:%d/%b/%Y:%H:%M:%S %z}".format(most_busiest[i][1]) + "," + str(most_busiest[i][0]) + "\n")
    busiest_times_file.close()
    print("completed 3")


def print_blocked_attempts(blocked_attempts, directory):
    blocked_file = open(directory, 'w')
    for attempt in blocked_attempts:
        blocked_file.write(attempt + "\n")
    blocked_file.close()


if __name__ == '__main__':
    log_file = open(sys.argv[1], 'r', encoding='utf-8')
    hosts = {}
    bandwidths = {}
    times = []
    blocked_attempts = []
    attempts = {}
    for log in log_file:
        print(log)
        log_split = log.split(' ')
        log_split_length = len(log_split)
        host = log_split[0]
        time = log_split[3]
        time_zone = log_split[4]
        resource = log_split[6]
        reply_code = log_split[log_split_length-2]
        bytes_size = log_split[log_split_length-1]
        feature_1(hosts, host)
        feature_2(bandwidths, resource, bytes_size)
        feature_3(times, time, time_zone)
        feature_4(blocked_attempts, attempts, log, host, time, time_zone, reply_code)
    print_most_active(hosts, sys.argv[2])
    print_most_bandwidth(bandwidths, sys.argv[4])
    print_busiest_time(times, sys.argv[3])
    print_blocked_attempts(blocked_attempts, sys.argv[5])
