# SCServo Control Table Editor

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

A Python tool for reading and writing SCServo control table values with interactive menu and multi-servo support.

## Features

- **Interactive menu system** for easy operation
- **Support for all control table addresses** defined in SCServo protocol
- **Dynamic servo ID selection** (0-255 range)
- **Automatic data size detection** (1-byte or 2-byte registers)
- **Byte order correction** for 2-byte values
- **EEPROM unlock** functionality
- **Error handling** with detailed feedback

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/scservo-control-editor.git
cd scservo-control-editor
```

2. Install required dependencies:
```bash
pip install scservo-sdk
```

## Usage

```bash
python Servo_diagnostic_linux.py
```

### Menu Options:
1. **Read all values** - Displays all control table values for current servo
2. **Read specific address** - Reads a single control table address
3. **Write to address** - Writes a new value to specified address
4. **Change Servo ID** - Switch to work with a different servo (0-255)
5. **Exit** - Cleanly closes the connection

## Configuration

Edit the following variables in the script if needed:
- `DEVICENAME`: Serial port device (default: '/dev/ttyUSB0')
- `BAUDRATE`: Communication speed (default: 1000000)
- `SCS_ID`: Default servo ID (default: 1)

## Supported Servos

This tool is designed to work with SCServo series servos including:
- SCS0009
- SCS0015
- SCS0009
- And other compatible models

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or pull request for any improvements or bug fixes.
