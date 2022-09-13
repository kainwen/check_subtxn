Check SubTransaction OverFlow
===========

## Usage

```
usage: check_subtxn_overflow.py [-h] --dbname DBNAME --host HOST --port PORT
                                --user USER --sudo_gdb SUDO_GDB

Find If SubTnx Overflow

optional arguments:
  -h, --help           show this help message and exit
  --dbname DBNAME      database name to connect
  --host HOST          hostname to connect
  --port PORT          port to connect
  --user USER          username to connect with
  --sudo_gdb SUDO_GDB  if gdb attach pid need sudo
  --pid PID            if provided, it will directly gdb to this process          
```

## A practical example

1 build a scenario with subtransaction overflow

```sql
CREATE OR REPLACE FUNCTION transaction_test2()
RETURNS void AS $$
DECLARE
    i int;
BEGIN
        for i in 0..1000
        LOOP
                BEGIN
                        CREATE TEMP TABLE tmptab(c int) DISTRIBUTED BY (c);
                        DROP TABLE tmptab;
                EXCEPTION
                        WHEN others THEN
                                NULL;
                END;
        END LOOP;
END;
$$
LANGUAGE plpgsql;

BEGIN;
SELECT transaction_test2();
```

Keep the above session alive.

2 run the python script:

```
gpadmin@zlv-ubuntu:~/check_subtxn$ python2 check_subtxn_overflow.py --dbname postgres --host localhost --port 6000 --user gpadmin --sudo_gdb true
2022-09-13 11:30:45.946057
============================================
pid index: 149
pid of overflowed trx: 7597
number of subtrx: 64
session id of the trx: 25
roleId of the pid: 10
```
