import subprocess
import sys
from datetime import datetime
import argparse
from pygresql.pg import DB


def create_session(user="gpadmin", database="postgres", host="localhost", port=5432):
    db = DB(dbname=database, user=user, host=host, port=port)
    pid = db.query("select pg_backend_pid()").getresult()[0][0]
    return (pid, db)

# gdb -iex "set pagination off" -q -ex cont -p $PID
def gdb(pid, sudo=False):
    cmd = ["/usr/bin/gdb", "-q", "-x", "./g", "-batch", "-p", str(pid)]
    if sudo:
        cmd.insert(0, "sudo")
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    [out, err] = proc.communicate()
    proc.wait()
    smart_print(out.split("\n"))

def hit(line):
    return line.startswith("=========")

def smart_print(out):
    hit_time = 0
    for line in out:
        if hit(line):
            hit_time += 1
        if hit_time == 1:
            print line


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find If SubTnx Overflow')
    parser.add_argument('--dbname', type=str, help='database name to connect', required=True)
    parser.add_argument('--host', type=str, help='hostname to connect', required=True)
    parser.add_argument('--port', type=int, help='port to connect', required=True)
    parser.add_argument('--user', type=str, help='username to connect with', required=True)
    parser.add_argument('--sudo_gdb', type=bool, help='if gdb attach pid need sudo', required=True)
    parser.add_argument('--pid', type=int, help='user specify the pid to attach')
    
    args = parser.parse_args()
    
    print datetime.now()

    if args.pid:
        gdb(args.pid, args.sudo_gdb)
        sys.exit(0)

    pid, db = create_session(user=args.user, database=args.dbname, host=args.host, port=args.port)
    gdb(pid, args.sudo_gdb)
    db.close()
