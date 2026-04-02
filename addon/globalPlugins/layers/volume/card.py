# layers/volume/card.py
# A part of the Layered Commands NVDA addon
# Copyright (C) Matthew Duffell-Hoffman
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import config
from scriptHandler import script
from synthDriverHandler import getSynth, setSynth
import tones
import ui
from utils import mmdevice

from ..layer import Layer

class CardLayer(Layer):
	def __init__(self, handler):
		name = "volume-card"
		helpFile = "volume\\card.help.html"
		gestureMap = {
			"kb:uparrow": self.script_up,
			"kb:downarrow": self.script_down
		}
		super().__init__(name, gestureMap, handler, helpFile)

	@script()
	def script_up(self, gesture):
		self.changeCard(-1)

	@script()
	def script_down(self, gesture):
		self.changeCard(1)

	def changeCard(self, step):
		deviceIds, deviceNames = zip(*mmdevice.getOutputDevices(includeDefault=True))
		selectedOutputDevice = config.conf["audio"]["outputDevice"]
		currentIndex = deviceIds.index(config.conf["audio"]["outputDevice"])
		newIndex = (currentIndex + step) % len(deviceIds)
		newOutputDevice = deviceIds[newIndex]
		if config.conf["audio"]["outputDevice"] != newOutputDevice:
			# Synthesizer must be reload if output device changes
			config.conf["audio"]["outputDevice"] = newOutputDevice
			currentSynth = getSynth()
			if not setSynth(currentSynth.name):
				_synthWarningDialog(currentSynth.name)

			# Reinitialize the tones module to update the audio device
			tones.terminate()
			tones.initialize()
		ui.message(deviceNames[newIndex])