from conftest import wait
from conftest import SensorInfo
import time
import requests
import logging
import pytest


log = logging.getLogger(__name__)


def test_sanity(get_sensor_info, get_sensor_reading, set_sensor_name, set_sensor_reading_interval, sensor_reboot, reset_sensor_to_factory, sensor_update_firmware, get_sensor_methods):
    set_sensor_name("new-name")
    set_sensor_reading_interval(1)
    sensor_info = get_sensor_info()
    assert sensor_info.name is not None
    assert sensor_info.firmware_version is not None

    sensor_name = sensor_info.name
    assert isinstance(sensor_name, str), "Sensor name is not a string"

    sensor_hid = sensor_info.hid
    assert isinstance(sensor_hid, str), "Sensor hid is not a string"

    sensor_model = sensor_info.model
    assert isinstance(sensor_model, str), "Sensor model is not a string"

    sensor_firmware_version = sensor_info.firmware_version
    assert isinstance(sensor_firmware_version, (int, float)), "Sensor firmware version is not a int"

    sensor_reading_interval = sensor_info.reading_interval
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
    log.info("Get original sensor info")
    sensor_info_before_reboot = get_sensor_info()

    
    log.info("Reboot sensor")
    reboot_response = sensor_reboot()
    assert (
        reboot_response == "rebooting"
    ), "Sensor did not return proper text in response to reboot request"

    
    log.info("Wait for sensor to come back online")
    sensor_info_after_reboot = wait(
        func=get_sensor_info,
        condition=lambda x: isinstance(x, SensorInfo),
        tries=10,
        timeout=1,
    )
    
    if not sensor_info_after_reboot:
        raise AssertionError("Sensor did not turn on after reboot")

    log.info("Validate that info from Step 1 is equal to info from Step 4")
    assert (
            sensor_info_before_reboot == sensor_info_after_reboot
    ), "Sensor information after reboot is the same as pre-reboot information"


def test_set_sensor_name(get_sensor_info, set_sensor_name):
    """
    1. Set sensor name to "new_name".
    2. Get sensor_info.
    3. Validate that current sensor name matches the name set in Step 1.
    """

    log.info("Set sensor name to 'new_name'")
    set_sensor_name("new_name")

    log.info("Get sensor_info")
    sensor_info = get_sensor_info()

    log.info("Validate that current sensor name matches the name set in Step 1")
    assert sensor_info.name == "new_name"



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
    log.info("Set sensor reading interval to 1")
    interval = 1
    set_sensor_reading_interval(interval)

    log.info("Get sensor info")
    sensor_info = get_sensor_info()

    log.info("Validate that sensor reading interval is set to interval from Step 1")
    assert sensor_info.reading_interval == interval, f"Expected interval {interval}, got {sensor_info.reading_interval}"


    log.info("Get sensor reading")
    initial_reading = get_sensor_reading()

    log.info("Wait for interval specified in Step 1")
    time.sleep(interval)

    log.info("Get sensor reading")
    new_reading = get_sensor_reading()

    log.info("Validate that reading from Step 4 doesn't equal reading from Step 6")
    assert initial_reading != new_reading, "Sensor reading did not change after the interval"


# Максимальная версия прошивки сенсора -- 15
def test_update_sensor_firmware(get_sensor_info, sensor_update_firmware):
    """
    1. Get the current sensor firmware version.
    2. Request firmware update.
    3. Get the current sensor firmware version.
    4. Validate that the current firmware version is +1 to the original firmware version.
    5. Repeat steps 1-4 until the sensor reaches max_firmware_version - 1.
    6. Update the sensor to the max firmware version.
    7. Validate that the sensor is at the max firmware version.
    8. Request another firmware update.
    9. Validate that the sensor does not update and responds appropriately.
    10. Validate that the sensor firmware version does not change if it is at the maximum value.
    """
    log.info("Get the current sensor firmware version")
    original_firmware_version = get_sensor_info().firmware_version

    max_firmware_version = 15
    current_sensor_firmware_version = original_firmware_version

    while current_sensor_firmware_version != max_firmware_version:
        expected_firmware_version = current_sensor_firmware_version + 1
        log.info(f"Updating sensor firmware to version {expected_firmware_version}")

        update_sensor_firmware_response = sensor_update_firmware()
        assert update_sensor_firmware_response == "updating", f"Expected 'updating', got {update_sensor_firmware_response}"

        assert wait(
            func=get_sensor_info,
            condition=lambda x: x.firmware_version == expected_firmware_version,
            tries=15,
            timeout=1,
        ), f"Failed to update firmware to version {expected_firmware_version}"

        current_sensor_firmware_version = get_sensor_info().firmware_version

        assert current_sensor_firmware_version == expected_firmware_version, \
            f"Expected firmware version {expected_firmware_version}, got {current_sensor_firmware_version}"



def test_set_invalid_sensor_reading_interval(set_sensor_reading_interval, get_sensor_info):
    """
    Test Steps:
        1. Get original sensor reading interval.
        2. Set interval to < 1.
        3. Validate that sensor responds with an error.
        4. Get current sensor reading interval.
        5. Validate that sensor reading interval didn't change.
    """
    log.info("Get original sensor reading interval")
    original_interval = get_sensor_info().reading_interval

    log.info("Set interval to a value less than 1")
    invalid_interval = 0

    with pytest.raises(ValueError, match="'interval' should be positive"):
        set_sensor_reading_interval(invalid_interval)

    log.info("Get current sensor reading interval")
    current_interval = get_sensor_info().reading_interval

    log.info("Validate that the sensor reading interval remains unchanged")
    assert current_interval == original_interval, "Sensor reading interval should remain unchanged after setting an invalid interval"



def test_set_empty_sensor_name(get_sensor_info, set_sensor_name):
    """
    Test Steps:
        1. Get original sensor name.
        2. Set sensor name to an empty string.
        3. Validate that sensor responds with an error.
        4. Wait for sensor to come back online.
        5. Get current sensor name.
        6. Validate that sensor name didn't change.
    """
    log.info("Get original sensor name")
    original_sensor_info = get_sensor_info()
    original_name = original_sensor_info.name

    log.info("Set sensor name to an empty string")
    with pytest.raises(ValueError, match="'name' should not be empty"):
        set_sensor_name("")

    log.info("Wait for sensor to come back online")
    sensor_info_after_reboot = get_sensor_info()

    log.info("Get current sensor name")
    current_sensor_info = get_sensor_info()

    log.info("Validate that sensor name didn't change")
    assert current_sensor_info.name == original_name, (
        f"Expected name {original_name}, got {current_sensor_info.name}"
    )
