#!/usr/bin/env python3

import subprocess
import os
import time

try:
    while True:
        subprocess.run(["free", "-h"])
        time.sleep(1)

except KeyboardInterrupt:
    print("\nPrograma finalizado.")
