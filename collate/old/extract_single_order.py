import datetime
import random
import numpy as np
import operator

def get_order_data(row, granularity):
    # Part 1
    order_id = row['order_id']
    site = row['order_site_name']
    created = row['order_created_at']
    completed = None
    for tag in ["first", "second", "third", "fourth", "fifth"]:
        this_time = row['failed_or_complete_datetime_%s' % tag]
        if this_time is not np.nan:
            completed = this_time
        else:
            break
    if site == 'HOVER India':
        return None
    try:
        created_time = datetime.datetime.strptime(created.split(".")[0], "%Y-%m-%d %H:%M:%S")
        completed_time = datetime.datetime.strptime(completed.split(".")[0], "%Y-%m-%d %H:%M:%S")
    except:
        return None
    new_created_min = created_time.minute - (created_time.minute % granularity)
    new_completed_min = completed_time.minute - (completed_time.minute % granularity)
    created_time = created_time.replace(minute=new_created_min, second=0)
    completed_time = completed_time.replace(minute=new_completed_min, second=0)
    tat = completed_time - created_time
    tat_sec = tat.total_seconds()
    tat_in_intervals = int(tat_sec / (60 * granularity))
    interval_states = [None for _ in range(tat_in_intervals + 1)]
    
    # Part 2
    order_events = pubtasks[pubtasks["order_id"] == int(order_id)]
    events = []
    for index, row in order_events.iterrows():
        # Ignore image events
        if row['transition_type'] != 'order':
            continue
        # Extract state change info
        from_state = row['from_state']
        to_state = row['to_state']
        timestamp = row['transition_created_at']
        transition_time = datetime.datetime.strptime(timestamp.split(".")[0], "%Y-%m-%d %H:%M:%S")
        events.append([transition_time, from_state, to_state])
    sorted_events = sorted(events, key=operator.itemgetter(0), reverse=True)
    for e in sorted_events:
        event_time = e[0]
        from_state = e[1]
        to_state = e[2]
        new_event_min = event_time.minute - (event_time.minute % granularity)
        event_time = event_time.replace(minute=new_event_min, second=0)
        elapsed_time = event_time - created_time
        interval = int(elapsed_time.total_seconds() / (60 * granularity))
        curr_interval = interval
        while curr_interval < len(interval_states) and interval_states[curr_interval] is None:
            interval_states[curr_interval] = to_state
            curr_interval += 1
    order_data = {}
    order_data['order_id'] = order_id
    order_data['minute_granularity'] = granularity 
    order_data['created_time'] = created_time
    order_data['completed_time'] = completed_time
    order_data['num_intervals'] = len(interval_states)
    order_data['interval_states'] = interval_states
    return order_data

if __name__ == '__main__':
    order_id = sys.argv[1]
    granularity = int(sys.argv[2])
    f = open("rows/%s.json" % order_id)
    row = json.load(f)
    f.close()

    order_data = get_order_data(row, granularity)
    out_f = open("orders/%s.json" % order_data['order_id'])
    json.dump(out_f, order_data)
    out_f.close()
