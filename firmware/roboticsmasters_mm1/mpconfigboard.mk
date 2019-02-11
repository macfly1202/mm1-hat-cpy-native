LD_FILE = boards/samd21x18-bootloader-external-flash-crystalless.ld
USB_VID = 0x0005
USB_PID = 0x0005
USB_PRODUCT = "MM1 HAT"
USB_MANUFACTURER = "RoboticsMasters"

SPI_FLASH_FILESYSTEM = 1
EXTERNAL_FLASH_DEVICE_COUNT = 1
EXTERNAL_FLASH_DEVICES = "ST26VF016B"
LONGINT_IMPL = MPZ

CHIP_VARIANT = SAMD21G18A
CHIP_FAMILY = samd21

CFLAGS_INLINE_LIMIT = 55

# Include these Python libraries in firmware.
FROZEN_MPY_DIRS += $(TOP)/frozen/Adafruit_CircuitPython_BusDevice
FROZEN_MPY_DIRS += $(TOP)/frozen/Adafruit_CircuitPython_Crickit
FROZEN_MPY_DIRS += $(TOP)/frozen/Adafruit_CircuitPython_Motor
FROZEN_MPY_DIRS += $(TOP)/frozen/Adafruit_CircuitPython_NeoPixel
FROZEN_MPY_DIRS += $(TOP)/frozen/Adafruit_CircuitPython_seesaw
