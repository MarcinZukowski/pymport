# pymport

Python import helper library.

I wrote it when I got tired of various Python tools not working, and giving me just
a `No module named something` error, especially when installing a particular module
is more complex than just pip.

## How it works

Example error, without pymport:

    Traceback (most recent call last):
      File "./test.py", line 5, in <module>
        import prettytable
    ImportError: No module named prettytable

with pymport:

    === PYMPORT ===: Try: sudo pip2.6 install PrettyTable
    Traceback (most recent call last):
      File "./test.py", line 5, in <module>
        import prettytable
    ImportError: No module named prettytable

An example of a more informative hint:

    === PYMPORT ===:
            Try:
                sudo pip2.7 install snowflake-connector-python prettytable
            You might also need to install
                python27-python-devel

    Traceback (most recent call last):
      File "./test.py", line 7, in <module>
        import snowflake.connector
    ImportError: No module named snowflake.connector


## Usage

Just add

    import pymport

at the beginning of your file, before other `import` commands.

