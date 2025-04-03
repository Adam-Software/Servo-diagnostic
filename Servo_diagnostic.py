#!/usr/bin/env python
#
# *********     SCServo Control Table Editor      *********
#
# This script allows reading and writing all control table addresses

import os
import sys
from scservo_sdk import *  # Uses SCServo SDK library

# Control table address (extended)
CT_ADDRESS = {
    "P_VERSION_L": 3,
    "P_ID": 5,
    "P_BAUD_RATE": 6,
    "P_RETURN_DELAY_TIME": 7,
    "P_RETURN_LEVEL": 8,
    "P_MIN_ANGLE_LIMIT_L": 9,
    "P_MAX_ANGLE_LIMIT_L": 11,
    "P_LIMIT_TEMPERATURE": 13,
    "P_MAX_LIMIT_VOLTAGE": 14,
    "P_MIN_LIMIT_VOLTAGE": 15,
    "P_MAX_TORQUE_L": 16,
    "P_ALARM_LED": 19,
    "P_ALARM_SHUTDOWN": 20,
    "P_COMPLIANCE_P": 21,
    "D_COMPLIANCE_D": 22,
    "I_COMPLIANCE_I": 23,
    "P_PUNCH_L": 24,
    "P_CW_DEAD": 26,
    "P_CCW_DEAD": 27,
    "P_PROTECT_CURRENT": 28,
    "P_OVERCURRENT_PROTECTION": 31,
    "P_OVERLOAD_CURRENT": 32,
    "P_ROTATION_RUN": 35,
    "P_ANGLE_MODE": 36,
    "P_TORQUE_ENABLE": 40,
    "P_LED": 41,
    "P_GOAL_POSITION_L": 42,
    "P_GOAL_TIME_L": 44,
    "P_GOAL_SPEED_L": 46,
    "P_LOCK": 48,
    "P_PRESENT_POSITION_L": 56,
    "P_PRESENT_SPEED_L": 58,
    "P_PRESENT_LOAD_L": 60,
    "P_PRESENT_VOLTAGE": 62,
    "P_PRESENT_TEMPERATURE": 63,
    "P_REGISTERED_INSTRUCTION": 64,
    "P_MOVING": 66
}

# Default settings
SCS_ID = 1  # Default SCServo ID
BAUDRATE = 1000000  # SCServo default baudrate : 1000000
DEVICENAME = 'COM3'
protocol_end = 1  # SCServo bit end(STS/SMS=0, SCS=1)

# Global swap bytes setting
swap_bytes_enabled = False


def swap_bytes(value):
    """Swap bytes in 2-byte value"""
    return ((value & 0xFF) << 8) | ((value >> 8) & 0xFF)


# Initialize PortHandler
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler
packetHandler = PacketHandler(protocol_end)


def setup_connection():
    if not portHandler.openPort():
        print("Failed to open the port")
        return False
    if not portHandler.setBaudRate(BAUDRATE):
        print("Failed to change the baudrate")
        return False
    return True


def read_all_values(servo_id):
    results = {}
    for name, addr in CT_ADDRESS.items():
        # 1-byte registers
        if addr in [3, 4, 5, 6, 7, 8, 13, 14, 15, 19, 20, 21, 22, 23, 31, 35, 36, 40, 41, 48, 62, 63, 64, 66]:
            value, comm_result, error = packetHandler.read1ByteTxRx(portHandler, servo_id, addr)
        else:  # 2-byte registers
            value, comm_result, error = packetHandler.read2ByteTxRx(portHandler, servo_id, addr)
            if swap_bytes_enabled:
                value = swap_bytes(value)

        if comm_result == COMM_SUCCESS and error == 0:
            results[name] = value
        else:
            results[name] = "Error"
    return results


def read_address(servo_id, address_name):
    if address_name not in CT_ADDRESS:
        print("Invalid address name")
        return None

    addr = CT_ADDRESS[address_name]

    if addr in [3, 4, 5, 6, 7, 8, 13, 14, 15, 19, 20, 21, 22, 23, 31, 35, 36, 40, 41, 48, 62, 63, 64, 66]:
        value, comm_result, error = packetHandler.read1ByteTxRx(portHandler, servo_id, addr)
    else:
        value, comm_result, error = packetHandler.read2ByteTxRx(portHandler, servo_id, addr)
        if swap_bytes_enabled:
            value = swap_bytes(value)

    if comm_result != COMM_SUCCESS:
        print("Communication error:", packetHandler.getTxRxResult(comm_result))
        return None
    elif error != 0:
        print("Error:", packetHandler.getRxPacketError(error))
        return None

    return value


def write_address(servo_id, address_name, value):
    if address_name not in CT_ADDRESS:
        print("Invalid address name")
        return False

    addr = CT_ADDRESS[address_name]

    if addr in [3, 4, 5, 6, 7, 8, 13, 14, 15, 19, 20, 21, 22, 23, 31, 35, 36, 40, 41, 48, 62, 63, 64, 66]:
        comm_result, error = packetHandler.write1ByteTxRx(portHandler, servo_id, addr, value)
    else:
        if swap_bytes_enabled:
            value = swap_bytes(value)
        comm_result, error = packetHandler.write2ByteTxRx(portHandler, servo_id, addr, value)

    if comm_result != COMM_SUCCESS:
        print("Communication error:", packetHandler.getTxRxResult(comm_result))
        return False
    elif error != 0:
        print("Error:", packetHandler.getRxPacketError(error))
        return False

    return True


def print_menu():
    print("\nSCServo Control Table Editor")
    print(f"1. Read all values (Byte swap: {'ON' if swap_bytes_enabled else 'OFF'})")
    print("2. Read specific address")
    print("3. Write to address")
    print("4. Change Servo ID")
    print("5. Toggle byte swap (currently " + ("ON" if swap_bytes_enabled else "OFF") + ")")
    print("6. Exit")


def get_servo_id():
    while True:
        try:
            servo_id = int(input("Enter Servo ID (0-255): "))
            if 0 <= servo_id <= 255:
                return servo_id
            print("ID must be between 0 and 255")
        except ValueError:
            print("Please enter a valid number")


def main():
    global swap_bytes_enabled

    if not setup_connection():
        return

    servo_id = SCS_ID
    write_address(servo_id, "P_LOCK", 0)  # Unlock EEPROM

    while True:
        print(f"\nCurrent Servo ID: {servo_id}")
        print_menu()
        try:
            choice = int(input("Select option: "))
        except ValueError:
            print("Invalid input")
            continue

        if choice == 1:
            values = read_all_values(servo_id)
            print("\nCurrent values:")
            for name, value in values.items():
                print(f"{name} (addr {CT_ADDRESS[name]}): {value}")

        elif choice == 2:
            print("\nAvailable addresses:")
            for name in CT_ADDRESS:
                print(name)

            addr_name = input("Enter address name: ")
            value = read_address(servo_id, addr_name)
            if value is not None:
                print(f"{addr_name} (addr {CT_ADDRESS[addr_name]}): {value}")

        elif choice == 3:
            print("\nAvailable addresses:")
            for name in CT_ADDRESS:
                print(name)

            addr_name = input("Enter address name: ")
            try:
                value = int(input("Enter new value: "))
                if write_address(servo_id, addr_name, value):
                    print("Write successful")
                    read_value = read_address(servo_id, addr_name)
                    print(f"New value: {read_value}")
            except ValueError:
                print("Invalid value")

        elif choice == 4:
            servo_id = get_servo_id()
            print(f"Servo ID changed to {servo_id}")

        elif choice == 5:
            swap_bytes_enabled = not swap_bytes_enabled
            print(f"Byte swap {'enabled' if swap_bytes_enabled else 'disabled'}")

        elif choice == 6:
            break

        else:
            print("Invalid option")

    write_address(servo_id, "P_TORQUE_ENABLE", 0)
    portHandler.closePort()


if __name__ == "__main__":
    main()
