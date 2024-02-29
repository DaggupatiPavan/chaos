import subprocess
import re
import mysql.connector
import sys

def parse_apachebench_output(output):
    result = {}

    result['Concurrency_Level  '] = int(re.search(r'Concurrency Level:\s+(\d+)', output).group(1))
    result['Time_taken_for_tests '] = float(re.search(r'Time taken for tests:\s+([\d.]+)\s+seconds', output).group(1))
    result['Complete_requests '] = int(re.search(r'Complete requests:\s+(\d+)', output).group(1))
    result['Failed_requests '] = int(re.search(r'Failed requests:\s+(\d+)', output).group(1))
    result['Keep_Alive_requests  '] = int(re.search(r'Keep-Alive requests:\s+(\d+)', output).group(1))
    result['Total_transferred  '] = int(re.search(r'Total transferred:\s+(\d+) bytes', output).group(1))
    result['HTML_transferred '] = int(re.search(r'HTML transferred:\s+(\d+) bytes', output).group(1))
    result['Requests_per_second'] = float(re.search(r'Requests per second:\s+([\d.]+)\s+\[#/sec\] \(mean\)', output).group(1))
    result['Time_per_request_ms_mean'] = float(re.search(r'Time per request:\s+([\d.]+)\s+\[ms\] \(mean\)', output).group(1))
    result['Time_per_request_ms_mean_all_concurrent'] = float(re.search(r'Time per request:\s+([\d.]+)\s+\[ms\] \(mean, across all concurrent requests\)', output).group(1))
    result['Transfer_rate_Kbytes_sec_received '] = float(re.search(r'Transfer rate:\s+([\d.]+)\s+\[Kbytes/sec\] received', output).group(1))

    return result

def insert_into_mysql(data):
    # Connect to MySQL database
    db = mysql.connector.connect(
        host="10.63.34.188",
        user="root",
        password="root",
        database="intel"
    )
    cursor = db.cursor()

    # Insert data into MySQL table
    insert_query = """
        INSERT INTO traffic_test (
            Concurrency_Level  ,
            Time_taken_for_tests ,
            Complete_requests ,
            Failed_requests ,
            Keep_Alive_requests  ,
            Total_transferred  ,
            HTML_transferred ,
            Requests_per_second,
            Time_per_request_ms_mean,
            Time_per_request_ms_mean_all_concurrent,
            Transfer_rate_Kbytes_sec_received 
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, data)

    # Commit changes and close connection
    db.commit()
    db.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 program.py 'docker run ...'")
        sys.exit(1)

    apachebench_command = sys.argv[1]

    # Run ApacheBench command
    output = subprocess.check_output(apachebench_command, shell=True, text=True)

    # Parse and insert data into MySQL
    data = parse_apachebench_output(output)
    insert_into_mysql(data)

    print("Data inserted into MySQL successfully!")
