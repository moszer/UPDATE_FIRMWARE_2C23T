# 2c23t Firmware Update Tool

This program is designed to help you update the firmware for the 2c23t device. It addresses issues related to failed firmware updates by controlling the data transfer speed, ensuring a more reliable update process.

## Features

- **Reliable Firmware Updates**: Prevents update failures by slowing down the data transfer process.
- **Chunked File Transfer**: Transfers the firmware file in small chunks (4096 bytes) with a 100ms delay between each chunk.
- **Progress Monitoring**: Displays the update progress in a progress bar and logs the hexadecimal data being transferred in real-time.

## Installation

### Step 1: Install Python and Required Libraries

Ensure that Python is installed on your system. Then, install the necessary libraries using the following command:

```bash
pip install PyQt5
