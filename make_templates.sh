# Usage: for i in $(seq 1 25); do bash make_templates.sh $i; done

echo "from aocd.models import Puzzle" >> day$1.py
echo "from collections import defaultdict" >> day$1.py
echo "import logging" >> day$1.py
echo "import re" >> day$1.py
echo "import sys" >> day$1.py
echo "" >> day$1.py
echo "logging.basicConfig(level=logging.DEBUG)" >> day$1.py
echo "" >> day$1.py
echo "p = Puzzle(year=2023, day=$1)" >> day$1.py
echo "" >> day$1.py
echo "TEST = False" >> day$1.py
echo "if TEST:" >> day$1.py
echo "    lines = p.examples[0].input_data.splitlines()" >> day$1.py
echo "else:" >> day$1.py
echo "    lines = p.input_data.splitlines()" >> day$1.py
echo "" >> day$1.py
echo "#..." >> day$1.py
echo "" >> day$1.py
echo "# if not TEST:" >> day$1.py
echo "#     p.answer_a = 10" >> day$1.py
