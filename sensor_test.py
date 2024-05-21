from conftest import wait
<<<<<<< HEAD
=======
from conftest import SensorInfo
>>>>>>> lecture19
import time
import requests
import logging


log = logging.getLogger(__name__)


def test_sanity(get_sensor_info, get_sensor_reading, set_sensor_name, set_sensor_reading_interval, sensor_reboot, reset_sensor_to_factory, sensor_update_firmware, get_sensor_methods):
    set_sensor_name("new-name")
<<<<<<< HEAD
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
=======
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
>>>>>>> lecture19
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
<<<<<<< HEAD
    log.info("Get original sensor info")
    sensor_info_before_reboot = get_sensor_info()

    log.info("Reboot sensor")
    reboot_response = sensor_reboot()
    assert reboot_response == "rebooting", "Sensor did not return proper text in response to reboot request"

    log.info("Wait for sensor to come back online")
    sensor_info_after_reboot = wait(
        func=get_sensor_info,
        condition=lambda x: isinstance(x, dict),
        tries=10,
        timeout=1,
    )

    log.info("Validate that info from Step 1 is equal to info from Step 4")
    assert sensor_info_before_reboot == sensor_info_after_reboot, "Sensor info after reboot doesn't match sensor info before reboot"
=======
    
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


>>>>>>> lecture19

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
<<<<<<< HEAD
    assert sensor_info.get("name") == "new_name"
=======
    assert sensor_info.name == "new_name"
>>>>>>> lecture19


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
<<<<<<< HEAD
    assert sensor_info['reading_interval'] == interval, f"Expected interval {interval}, got {sensor_info['reading_interval']}"
=======
    assert sensor_info.reading_interval == interval, f"Expected interval {interval}, got {sensor_info.reading_interval}"
>>>>>>> lecture19

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
        log.info("Get original sensor firmware version")

<<<<<<< HEAD
        original_firmware_version = get_sensor_info()["firmware_version"]
=======
        original_firmware_version = get_sensor_info().firmware_version
>>>>>>> lecture19

        max_firmware_version = 15

        while original_firmware_version < max_firmware_version - 1:
            log.info("Request firmware update")
            sensor_update_firmware()

            log.info("Get current sensor firmware version")
<<<<<<< HEAD
            current_firmware_version = get_sensor_info()['firmware_version']
=======
            current_firmware_version = get_sensor_info().firmware_version
>>>>>>> lecture19

            log.info("Validate that current firmware version is +1 to original firmware version")
            assert current_firmware_version == original_firmware_version + 1, (
                f"Expected firmware version {original_firmware_version + 1}, got {current_firmware_version}"
            )
            # Update the original firmware version for the next iteration
            original_firmware_version = current_firmware_version

        log.info("Update sensor to max firmware version")
        sensor_update_firmware()

        log.info("Validate that sensor is at max firmware version")
        current_firmware_version = get_sensor_info()['firmware_version']
        assert current_firmware_version == max_firmware_version, (
            f"Expected firmware version {max_firmware_version}, got {current_firmware_version}"
        )

        log.info("Request another firmware update")
        sensor_update_firmware()

        log.info("Validate that sensor doesn't update and responds appropriately")
        current_firmware_version_after_update = get_sensor_info()['firmware_version']
        assert current_firmware_version_after_update == max_firmware_version, (
            f"Expected firmware version {max_firmware_version}, got {current_firmware_version_after_update}"
        )

        log.info(" Validate that sensor firmware version doesn't change if it's at maximum value")
        assert current_firmware_version_after_update == max_firmware_version, (
            f"Expected firmware version {max_firmware_version}, got {current_firmware_version_after_update}"
        )

        log.info("All firmware update tests passed successfully!")

    except requests.exceptions.RequestException as e:
        log.info(f"Error: {e}")
