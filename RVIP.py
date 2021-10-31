from multiprocessing import Process, Pipe
from os import getpid
from datetime import datetime

def local_time(counter):
    return ' (LAMPORT_TIME={}, LOCAL_TIME={})'.format(counter,
                                                    datetime.now())

def calc_recv_timestamp(vrem_met, counter):
    maximum = 1 + max(vrem_met, counter)
    return maximum

def event(pid, counter):
    counter += 1
    print('Something happened in {} !'.\
          format(pid) + local_time(counter))
    return counter

def send_message(pipe, pid, counter):
    counter += 1
    pipe.send(('message', counter))
    print('Message sent from ' + str(pid) + local_time(counter))
    return counter

def recv_message(pipe, pid, counter):
    message, timestamp = pipe.recv()
    counter = calc_recv_timestamp(timestamp, counter)
    print('Message received at ' + str(pid) + local_time(counter))
    return counter

def process(pipe,pipe2):
    pid = getpid()
    counter = 0
    counter = event(pid, counter)
    counter = send_message(pipe, pid, counter)
    counter = event(pid, counter)
    counter = recv_message(pipe2, pid, counter)
    counter = event(pid, counter)

if __name__ == '__main__':
    oneandtwo, twoandone = Pipe()

    process1 = Process(target=process,
                       args=(oneandtwo, twoandone))

    process1.start()

    process1.join()

