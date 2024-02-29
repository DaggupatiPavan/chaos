import subprocess
import re
import mysql.connector
import sys

def parse_apachebench_output(output):
    result = {}

    result['concurrency_level'] = int(re.search(r'Concurrency Level:\s+(\d+)', output).group(1))
    result['time_taken'] = float(re.search(r'Time taken for tests:\s+([\d.]+)\s+seconds', output).group(1))
    result['complete_requests'] = int(re.search(r'Complete requests:\s+(\d+)', output).group(1))
    result['failed_requests'] = int(re.search(r'Failed requests:\s+(\d+)', output).group(1))
    result['keep_alive_requests'] = int(re.search(r'Keep-Alive requests:\s+(\d+)', output).group(1))
    result['total_transferred'] = int(re.search(r'Total transferred:\s+(\d+) bytes', output).group(1))
    result['html_transferred'] = int(re.search(r'HTML transferred:\s+(\d+) bytes', output).group(1))
    result['requests_per_second'] = float(re.search(r'Requests per second:\s+([\d.]+)\s+\[#/sec\] \(mean\)', output).group(1))
    result['time_per_request_mean'] = float(re.search(r'Time per request:\s+([\d.]+)\s+\[ms\] \(mean\)', output).group(1))
    result['time_per_request_across_all'] = float(re.search(r'Time per request:\s+([\d.]+)\s+\[ms\] \(mean, across all concurrent requests\)', output).group(1))
    result['transfer_rate'] = float(re.search(r'Transfer rate:\s+([\d.]+)\s+\[Kbytes/sec\] received', output).group(1))

    return result

def insert_into_mysql(data):
    # Connect to MySQL database
    db = mysql.connector.connect(
        host="your_mysql_host",
        user="your_mysql_user",
        password="your_mysql_password",
        database="your_mysql_database"
    )
    cursor = db.cursor()

    # Insert data into MySQL table
    insert_query = """
        INSERT INTO apachebench_results (
            concurrency_level,
            time_taken,
            complete_requests,
            failed_requests,
            keep_alive_requests,
            total_transferred,
            html_transferred,
            requests_per_second,
            time_per_request_mean,
            time_per_request_across_all,
            transfer_rate
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
