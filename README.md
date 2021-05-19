# vendetta

[![Build Status](https://github.com/anatoly-scherbakov/vendetta/workflows/test/badge.svg?branch=master&event=push)](https://github.com/anatoly-scherbakov/vendetta/actions?query=workflow%3Atest)
[![Python Version](https://img.shields.io/pypi/pyversions/vendetta.svg)](https://pypi.org/project/vendetta/)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

Anonymize CSV file(s) by replacing sensitive values with fakes.

## Installation

```bash
pip install vendetta
```


## Example


Suppose you have `orders.csv` dataset with real customer names and order IDs.

```csv
CustomerName,CustomerLastName,OrderID
Darth,Wader,1254
Darth,Wader,1255
,Yoda,1256
Luke,Skywalker,1257
Leia,Skywalker,1258
,Yoda,1259
```

This list contains 4 unique customers. Let's create a configuration file, say, `orders.yaml`:

```yaml
columns:
  CustomerName: first_name
  CustomerLastName: last_name
```

and run:

```shell
vendetta anonymize orders.yaml < orders.csv > anon.csv
```

which gives something like this in `anon.csv`:

```csv
CustomerName,CustomerLastName,OrderID
Elizabeth,Oliver,1254
Elizabeth,Oliver,1255
Karen,Rodriguez,1256
Jonathan,Joseph,1257
Katelyn,Joseph,1258
Karen,Rodriguez,1259
```

- OrderID column was not mentioned in the config, and was left as is
- Using [faker](https://faker.readthedocs.io/), program replaced the first and last names with random first and last names, making the data believable
- If in the source file two cells for the same column had the same value (Vader), the output file will also have identical values in these cells.

Enjoy!

## License

[MIT](https://github.com/anatoly-scherbakov/vendetta/blob/master/LICENSE)


## Credits

This project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [b80221aaae4ac702bea7e66b77b9389d527c1e3c](https://github.com/wemake-services/wemake-python-package/tree/b80221aaae4ac702bea7e66b77b9389d527c1e3c). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/b80221aaae4ac702bea7e66b77b9389d527c1e3c...master) since then.
