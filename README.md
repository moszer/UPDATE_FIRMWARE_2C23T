# 2C23T Firmware Update Tool

A small PyQt5 desktop utility for flashing firmware onto the **2C23T gateway** by copying
the `.bin` image to the device **slowly and in fixed-size chunks**, with a live progress
bar and a hex dump of every byte going across.

## Why it exists

The 2C23T exposes its bootloader as a mounted volume, so "updating the firmware" is really
just copying a file onto it. A normal copy writes as fast as the OS can push bytes — and on
this device that reliably **fails or bricks the update**.

This tool throttles the write instead:

| | |
| --- | --- |
| Chunk size | **4096 bytes** (`64 * 64`) |
| Delay between chunks | **100 ms** |
| Effective rate | ~40 KB/s |

Slow enough that the device keeps up with the write, and slow enough that you can watch it
happen. The copy runs on a `QThread`, so the UI stays responsive and can be watched the
whole way through.

## Features

- **Throttled chunked transfer** — the whole point; prevents the failed-update problem
- **Progress bar** — percentage of the image written
- **Live hex log** — every chunk printed as hex bytes as it's transferred, so a stalled or
  corrupt write is visible immediately rather than at the end
- **Background thread** — the window never freezes mid-flash

## Requirements

- **Python 3.9.11** recommended — [download](https://www.python.org/downloads/release/python-3911/)
- PyQt5

```bash
pip install PyQt5
```

## Usage

```bash
python update_2c23t.py
```

1. **Select File** — pick the firmware image (`.bin`)
2. **Select Destination** — pick the mounted 2C23T volume (or any target directory)
3. **Copy File** — the transfer starts; watch the progress bar and hex log
4. Wait for **"File copy completed!"** — do not unplug the device before this appears

A firmware image is included in the repo for convenience:

```
F2C23T-GW-EN_V2.0.1.bin
```

## How it works

`SlowFileCopyThread` (a `QThread`) opens both files in binary mode and loops:

```python
buffer_size = 64 * 64   # 4096 bytes
delay = 0.1             # 100 ms

buffer = src.read(buffer_size)
dst.write(buffer)
self.progress.emit(int(copied_size / total_size * 100))
self.hex_log.emit(' '.join(f'{byte:02x}' for byte in buffer))
time.sleep(delay)
```

Progress and hex output reach the UI through Qt signals (`progress`, `hex_log`), which is
why the main window keeps repainting while a multi-minute flash is in progress.

To change the transfer rate, edit `buffer_size` and `delay` in `SlowFileCopyThread.run()`.

## Notes

- The tool is a **throttled file copy**, not a serial/DFU protocol implementation — it
  works for any device whose bootloader accepts a firmware image as a plain file write.
- `.bin` is offered as a filter in the file picker, but any file type can be selected.
- Tested on macOS with PyQt5.
