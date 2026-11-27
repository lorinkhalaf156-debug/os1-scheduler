#Read data from file
def read_data(filename):
    processes = []
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Note: {filename} not found. Using default data.\n")
        lines = [
            "group HW29 - algorithm: SRTF #\n",
            "name arrival burst priority #\n",
            "P1 0 4 2\n",
            "P2 3 2 3\n",
            "P3 3 3 2\n",
            "P4 4 5 1\n",
            "P5 6 2 2\n",
            "P6 6 8 2\n"
        ]

    for line in lines:
        line = line.strip()
        if not line or line.startswith('group') or line.startswith('name'):
            continue
        
        parts = line.split()
        if len(parts) >= 3:
            processes.append({
                'name': parts[0],
                'arrival': int(parts[1]),
                'burst': int(parts[2]),
                'priority': int(parts[3]) if len(parts) > 3 else 0
            })
    return processes

# Print metrics table and return averages
def print_metrics(processes, results):
    print(f"{'Process':<10} | {'Arrival':<8} | {'Burst':<7} | {'Completion':<10} | {'Turnaround':<11} | {'Waiting':<8} | {'Response':<8}")
    print("-" * 85)
    
    total_wait = 0
    total_turn = 0
    total_resp = 0
    
    for p in sorted(processes, key=lambda x: x['name']):
        name = p['name']
        comp = results[name]['completion']
        start = results[name]['start_time']
        
        turn = comp - p['arrival']
        wait = turn - p['burst']
        resp = start - p['arrival']
        
        total_wait += wait
        total_turn += turn
        total_resp += resp
        
        print(f"{name:<10} | {p['arrival']:<8} | {p['burst']:<7} | {comp:<10} | {turn:<11} | {wait:<8} | {resp:<8}")
        
    n = len(processes)
    avg_wait = total_wait/n
    avg_turn = total_turn/n
    avg_resp = total_resp/n
    
    print("-" * 85)
    print(f"Average Waiting Time: {avg_wait:.2f}")
    print(f"Average Turnaround Time: {avg_turn:.2f}")
    print(f"Average Response Time: {avg_resp:.2f}\n")
    
    return avg_wait, avg_turn, avg_resp

# FCFS Algorithm
def fcfs(processes):
    print("\n" + "="*30)
    print("    FCFS ALGORITHM")
    print("="*30)
    
    sorted_p = sorted(processes, key=lambda x: (x['arrival'], x['name']))
    time = 0
    results = {}
    gantt = []
    
    for p in sorted_p:
        if time < p['arrival']:
            time = p['arrival']
        
        start_time = time
        time += p['burst']
        
        results[p['name']] = {'completion': time, 'start_time': start_time}
        gantt.append(f"{p['name']} ({start_time}-{time})")
        
    print("Gantt Chart: " + " -> ".join(gantt))
    print("-" * 85)
    return print_metrics(processes, results)

# SRTF Algorithm
def srtf(processes):
    print("\n" + "="*30)
    print("    SRTF ALGORITHM")
    print("="*30)
    
    time = 0
    completed = 0
    n = len(processes)
    
    remaining_burst = {p['name']: p['burst'] for p in processes}
    results = {p['name']: {'completion': 0, 'start_time': -1} for p in processes}
    gantt = []
    
    while completed < n:
        available = [p for p in processes if p['arrival'] <= time and remaining_burst[p['name']] > 0]
        
        if not available:
            time += 1
            continue
            
        current = min(available, key=lambda x: remaining_burst[x['name']])
        name = current['name']
        
        if results[name]['start_time'] == -1:
            results[name]['start_time'] = time
            
        if not gantt or gantt[-1][0] != name:
            gantt.append([name, time])
            
        remaining_burst[name] -= 1
        time += 1
        
        if remaining_burst[name] == 0:
            completed += 1
            results[name]['completion'] = time

    gantt_str = [f"{g[0]} ({g[1]})" for g in gantt]
    gantt_str.append(f"End ({time})")
    
    print("Gantt Chart: " + " -> ".join(gantt_str))
    print("-" * 85)
    return print_metrics(processes, results)

# Main execution
if __name__ == "__main__":
    file_name = "input.txt"
    processes = read_data(file_name)
    
    # Get averages for both algorithms
    fcfs_wait, fcfs_turn, fcfs_resp = fcfs(processes)
    srtf_wait, srtf_turn, srtf_resp = srtf(processes)
    
    # Dynamic Comparison
    print("\n" + "="*40)
    print("    FINAL COMPARISON REPORT")
    print("="*40)
    
    print(f"1. Average Waiting Time:")
    print(f"   - FCFS: {fcfs_wait:.2f}")
    print(f"   - SRTF: {srtf_wait:.2f}")
    if srtf_wait < fcfs_wait:
        print("   => SRTF is BETTER (lower waiting time).")
    elif fcfs_wait < srtf_wait:
        print("   => FCFS is BETTER (lower waiting time).")
    else:
        print("   => Both are EQUAL.")
        
    print(f"\n2. Average Response Time:")
    print(f"   - FCFS: {fcfs_resp:.2f}")
    print(f"   - SRTF: {srtf_resp:.2f}")
    if srtf_resp < fcfs_resp:
        print("   => SRTF is BETTER (lower response time).")
    elif fcfs_resp < srtf_resp:
        print("   => FCFS is BETTER (lower response time).")
    else:
        print("   => Both are EQUAL.")
    print("="*40)
