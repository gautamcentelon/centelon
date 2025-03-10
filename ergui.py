import flet as ft
import serial
import time

# Full CRC-8 lookup table
crc_lookup_table = [
    0x00, 0x5E, 0xBC, 0xE2, 0x61, 0x3F, 0xDD, 0x83, 0xC2, 0x9C, 0x7E, 0x20, 0xA3, 0xFD, 0x1F, 0x41,
    0x9D, 0xC3, 0x21, 0x7F, 0xFC, 0xA2, 0x40, 0x1E, 0x5F, 0x01, 0xE3, 0xBD, 0x3E, 0x60, 0x82, 0xDC,
    0x23, 0x7D, 0x9F, 0xC1, 0x42, 0x1C, 0xFE, 0xA0, 0xE1, 0xBF, 0x5D, 0x03, 0x80, 0xDE, 0x3C, 0x62,
    0xBE, 0xE0, 0x02, 0x5C, 0xDF, 0x81, 0x63, 0x3D, 0x7C, 0x22, 0xC0, 0x9E, 0x1D, 0x43, 0xA1, 0xFF,
    0x46, 0x18, 0xFA, 0xA4, 0x27, 0x79, 0x9B, 0xC5, 0x84, 0xDA, 0x38, 0x66, 0xE5, 0xBB, 0x59, 0x07,
    0xDB, 0x85, 0x67, 0x39, 0xBA, 0xE4, 0x06, 0x58, 0x19, 0x47, 0xA5, 0xFB, 0x78, 0x26, 0xC4, 0x9A,
    0x65, 0x3B, 0xD9, 0x87, 0x04, 0x5A, 0xB8, 0xE6, 0xA7, 0xF9, 0x1B, 0x45, 0xC6, 0x98, 0x7A, 0x24,
    0xF8, 0xA6, 0x44, 0x1A, 0x99, 0xC7, 0x25, 0x7B, 0x3A, 0x64, 0x86, 0xD8, 0x5B, 0x05, 0xE7, 0xB9,
    0x8C, 0xD2, 0x30, 0x6E, 0xED, 0xB3, 0x51, 0x0F, 0x4E, 0x10, 0xF2, 0xAC, 0x2F, 0x71, 0x93, 0xCD,
    0x11, 0x4F, 0xAD, 0xF3, 0x70, 0x2E, 0xCC, 0x92, 0xD3, 0x8D, 0x6F, 0x31, 0xB2, 0xEC, 0x0E, 0x50,
    0xAF, 0xF1, 0x13, 0x4D, 0xCE, 0x90, 0x72, 0x2C, 0x6D, 0x33, 0xD1, 0x8F, 0x0C, 0x52, 0xB0, 0xEE,
    0x32, 0x6C, 0x8E, 0xD0, 0x53, 0x0D, 0xEF, 0xB1, 0xF0, 0xAE, 0x4C, 0x12, 0x91, 0xCF, 0x2D, 0x73,
    0xCA, 0x94, 0x76, 0x28, 0xAB, 0xF5, 0x17, 0x49, 0x08, 0x56, 0xB4, 0xEA, 0x69, 0x37, 0xD5, 0x8B,
    0x57, 0x09, 0xEB, 0xB5, 0x36, 0x68, 0x8A, 0xD4, 0x95, 0xCB, 0x29, 0x77, 0xF4, 0xAA, 0x48, 0x16,
    0xE9, 0xB7, 0x55, 0x0B, 0x88, 0xD6, 0x34, 0x6A, 0x2B, 0x75, 0x97, 0xC9, 0x4A, 0x14, 0xF6, 0xA8,
    0x74, 0x2A, 0xC8, 0x96, 0x15, 0x4B, 0xA9, 0xF7, 0xB6, 0xE8, 0x0A, 0x54, 0xD7, 0x89, 0x6B, 0x35,
]

# Function to calculate CRC-8
def calc_crc8(data):
    crc = 0x00
    for byte in data:
        crc = crc_lookup_table[crc ^ byte]
    return crc

# Function to send a command
def send_command(serial_port, data):
    crc = calc_crc8(data)
    data.append(crc)
    serial_port.write(bytearray(data))
    return [hex(x) for x in data]

# Flet app
def main(page: ft.Page):
    page.title = "Motor ID Configuration"
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    # Dropdown for direction
    direction_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("left"),
            ft.dropdown.Option("right"),
        ],
        label="Select Direction",
        width=200,
    )

    # Text field for COM port
    com_port_input = ft.TextField(label="COM Port", value="COM7", width=200)

    # Status box
    status_box = ft.TextField(
        value="",
        multiline=True,
        width=500,
        height=300,
        read_only=True,
    )

    # Dynamic direction status
    direction_status = ft.Text(value="No operation performed yet.", size=18, weight="bold")

    # Set motor ID
    def set_motor_id(e):
        if not direction_dropdown.value:
            page.snack_bar = ft.SnackBar(content=ft.Text("Please select a direction!"), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        try:
            serial_port = serial.Serial(
                port=com_port_input.value,
                baudrate=115200,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=1,
            )

            direction_code = 0x01 if direction_dropdown.value == "right" else 0x02
            set_id_command = [0xAA, 0x55, 0x53, direction_code, 0x00, 0x00, 0x00, 0x00, 0x00]

            # Sending command
            for _ in range(5):
                sent_command = send_command(serial_port, set_id_command.copy())
                status_box.value += f"Sent: {sent_command}\n"
                time.sleep(0.1)

            # Query motor ID
            query_command = [0xC8, 0x64, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
            sent_query = send_command(serial_port, query_command)
            status_box.value += f"Query Sent: {sent_query}\n"

            response = serial_port.read(10)
            if response:
                response_data = [hex(x) for x in response]
                status_box.value += f"Response: {response_data}\n"
                calculated_crc = calc_crc8(response[:-1])
                if calculated_crc == response[-1]:
                    status_box.value += "CRC-8 checksum is valid.\n"
                    direction_result = "left" if response[0] == 0x02 else "right" if response[0] == 0x01 else "unknown"
                    direction_status.value = f"Motor ID '{direction_result}' set successfully!"
                    page.snack_bar = ft.SnackBar(content=ft.Text(f"Motor ID '{direction_result}' set successfully!"), bgcolor="green")
                else:
                    status_box.value += "CRC-8 checksum is invalid.\n"
                    page.snack_bar = ft.SnackBar(content=ft.Text("Invalid CRC-8 checksum!"), bgcolor="red")
            else:
                page.snack_bar = ft.SnackBar(content=ft.Text("No response received!"), bgcolor="red")

            page.snack_bar.open = True
            page.update()
            serial_port.close()
        except Exception as ex:
            page.snack_bar = ft.SnackBar(content=ft.Text(f"Error: {str(ex)}"), bgcolor="red")
            page.snack_bar.open = True
            page.update()

    # Reset status box
    def reset_status_box(e):
        status_box.value = ""
        direction_status.value = "No operation performed yet."
        page.update()

    # Layout
    page.add(
        ft.Column(
            [
                direction_status,
                direction_dropdown,
                com_port_input,
                ft.Row(
                    [
                        ft.ElevatedButton("Set Motor ID", on_click=set_motor_id),
                        ft.ElevatedButton("Reset Status Box", on_click=reset_status_box),
                    ],
                    alignment="center",
                ),
                status_box,
            ],
            alignment="center",
            horizontal_alignment="center",
        )
    )

# Run the app
ft.app(target=main)
