#!/usr/bin/python
# -*- coding: utf-8 -*-

import hid  # `pip install hidapi`
import sys


USB_VID = 0x054c
USB_PID = 0x0c5e

HID_REPORT_BDADDR      = 0x04
HID_REPORT_CALIBRATION = 0x10


def dump(buf):
	for i in range(0, len(buf)):
		if i % 16 == 0:
			if i != 0:
				print("")
			sys.stdout.write("    ")
		sys.stdout.write("%02x " % buf[i])
	print("")
	print("")


h = hid.device()
try:
	h.open(USB_VID, USB_PID)
except IOError as ex:
	print("ERROR: Failed to connect to controller")
	print("Is one connected? You may need to run this program as root.")
	exit(1)

print("Manufacturer:     %s" % h.get_manufacturer_string())
print("Product:          %s" % h.get_product_string())

# get controller's BDADDR
res = h.get_feature_report(HID_REPORT_BDADDR, 16)
if not res:
	print("ERROR: Failed to read BDADDR report")
	exit(1)
else:
	bdaddr = list(reversed(res[1:7]))
	print("BDADDR:           %s" % ':'.join('%02x' % b for b in bdaddr))

# get controller's calibration data
print("Calibration data:")
for i in range(0, 2):
	res = h.get_feature_report(HID_REPORT_CALIBRATION, 49)
	if not res:
		print("ERROR: Failed to read calibration report")
		exit(1)
	else:
		dump(res)

