from conftest import wait
import time
import requests

def test_sanity(get_sensor_info, get_sensor_reading, set_sensor_name, set_sensor_reading_interval, sensor_reboot, reset_sensor_to_factory, sensor_update_firmware, get_sensor_methods):
    set_sensor_name("new-name")
    set_sensor_reading_interval("new-interval")
    sensor_info = get_sensor_info()

    sensor_name = sensor_info.get("name")
    assert isinstance(sensor_name, str), "Sensor name is not a string"

    sensor_hid = sensor_info.get("hid")
    assert isinstance(sensor_hid, str), "Sensor hid is not a string"

    sensor_model = sensor_info.get("model")
    assert isinstance(sensor_model, str), "Sensor model is not a string"

    sensor_firmware_version = sensor_info.get("firmware_version")
    assert isinstance(sensor_firmware_version, (int, float)), "Sensor firmware version is not a int"

    sensor_reading_interval = sensor_info.get("reading_interval")
    assert isinstance(sensor_reading_interval, int), "Sensor reading interval is not a string"

    sensor_reading = get_sensor_reading()
    assert isinstance(sensor_reading, float), "Sensor doesn't seem to register temperature"

    print("Sanity test passed")
  
def test_reboot(get_sensor_info, sensor_reboot):
    """
    Steps:
        1. Get original sensor info.
        2. Reboot sensor.
        3. Wait for sensor to come back online.
        4. Get current sensor info.
        5. Validate that info from Step 1 is equal to info from Step 4.
    """
    print("Get original sensor info")
    sensor_info_before_reboot = get_sensor_info()

    print("Reboot sensor")
    reboot_response = sensor_reboot()
    assert reboot_response == "rebooting", "Sensor did not return proper text in response to reboot request"

    print("Wait for sensor to come back online")
    sensor_info_after_reboot = wait(
        func=get_sensor_info,
        condition=lambda x: isinstance(x, dict),
        tries=10,
        timeout=1,
    )

    print("Validate that info from Step 1 is equal to info from Step 4")
    assert sensor_info_before_reboot == sensor_info_after_reboot, "Sensor info after reboot doesn't match sensor info before reboot"

def test_set_sensor_name(get_sensor_info, set_sensor_name):
    """
    1. Set sensor name to "new_name".
    2. Get sensor_info.
    3. Validate that current sensor name matches the name set in Step 1.
    """

    print("Set sensor name to 'new_name'")
    set_sensor_name("new_name")

    print("Get sensor_info")
    sensor_info = get_sensor_info()

    print("Validate that current sensor name matches the name set in Step 1")
    assert sensor_info.get("name") == "new_name"


def test_set_sensor_reading_interval(
    get_sensor_info, set_sensor_reading_interval, get_sensor_reading
):
    """
    1. Set sensor reading interval to 1.
    2. Get sensor info.
    3. Validate that sensor reading interval is set to interval from Step 1.
    4. Get sensor reading.
    5. Wait for interval specified in Step 1.
    6. Get sensor reading.
    7. Validate that reading from Step 4 doesn't equal reading from Step 6.
    """
    print("Set sensor reading interval to 1")
    interval = 1
    set_sensor_reading_interval(interval)

    print("Get sensor info")
    sensor_info = get_sensor_info()

    print("Validate that sensor reading interval is set to interval from Step 1")
    assert sensor_info['reading_interval'] == interval, f"Expected interval {interval}, got {sensor_info['reading_interval']}"

    print("Get sensor reading")
    initial_reading = get_sensor_reading()

    print("Wait for interval specified in Step 1")
    time.sleep(interval)

    print("Get sensor reading")
    new_reading = get_sensor_reading()

    print("Validate that reading from Step 4 doesn't equal reading from Step 6")
    assert initial_reading != new_reading, "Sensor reading did not change after the interval"


# Максимальная версия прошивки сенсора -- 15
def test_update_sensor_firmware(get_sensor_info, sensor_update_firmware):
    """
    1. Get original sensor firmware version.
    2. Request firmware update.
    3. Get current sensor firmware version.
    4. Validate that current firmware version is +1 to original firmware version.
    5. Repeat steps 1-4 until sensor is at max_firmware_version - 1.
    6. Update sensor to max firmware version.
    7. Validate that sensor is at max firmware version.
    8. Request another firmware update.
    9. Validate that sensor doesn't update and responds appropriately.
    10. Validate that sensor firmware version doesn't change if it's at maximum value.
    """
    try:
        print("Get original sensor firmware version")

        original_firmware_version = get_sensor_info()["firmware_version"]

        max_firmware_version = 15

        while original_firmware_version < max_firmware_version - 1:
            print("Request firmware update")
            sensor_update_firmware()

            print("Get current sensor firmware version")
            current_firmware_version = get_sensor_info()['firmware_version']

            print("Validate that current firmware version is +1 to original firmware version")
            assert current_firmware_version == original_firmware_version + 1, (
                f"Expected firmware version {original_firmware_version + 1}, got {current_firmware_version}"
            )
            # Update the original firmware version for the next iteration
            original_firmware_version = current_firmware_version

        print("Update sensor to max firmware version")
        sensor_update_firmware()

        print("Validate that sensor is at max firmware version")
        current_firmware_version = get_sensor_info()['firmware_version']
        assert current_firmware_version == max_firmware_version, (
            f"Expected firmware version {max_firmware_version}, got {current_firmware_version}"
        )

        print("Request another firmware update")
        sensor_update_firmware()

        print("Validate that sensor doesn't update and responds appropriately")
        current_firmware_version_after_update = get_sensor_info()['firmware_version']
        assert current_firmware_version_after_update == max_firmware_version, (
            f"Expected firmware version {max_firmware_version}, got {current_firmware_version_after_update}"
        )

        print(" Validate that sensor firmware version doesn't change if it's at maximum value")
        assert current_firmware_version_after_update == max_firmware_version, (
            f"Expected firmware version {max_firmware_version}, got {current_firmware_version_after_update}"
        )

        print("All firmware update tests passed successfully!")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")