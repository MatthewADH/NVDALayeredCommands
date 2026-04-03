# layers/volume/system.py
# A part of the Layered Commands NVDA addon
# Layer for controlling system volume
# Copyright (C) Matthew Duffell-Hoffman
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from scriptHandler import script
import ui

from comtypes import CLSCTX_ALL
from pycaw.api.endpointvolume import IAudioEndpointVolume
from pycaw.utils import AudioUtilities

from ..layer import Layer

class SystemLayer(Layer):
	def __init__(self, handler):
		name = "volume-system"
		helpFile = "volume\\system.help.html"
		gestureMap = {
			"kb:uparrow": self.script_up,
			"kb:downarrow": self.script_down,
			"kb:pageup": self.script_pageUp,
			"kb:pagedown": self.script_pageDown,
			"kb:numpad9": self.script_pageUp,
			"kb:numpad3": self.script_pageDown,
			"kb:home": self.script_home,
			"kb:numpad7": self.script_home,
			"kb:end": self.script_end,
			"kb:numpad1": self.script_end,
		}
		super().__init__(name, gestureMap, handler, helpFile)

	@script(description="Increases system  volume by 2%")
	def script_up(self, gesture):
		targetVolume = self.getVolume() + 2
		self.setVolume(targetVolume)
		ui.message(f"{self.getVolume()}%")

	@script(description="Decreases system  volume by 2% to a minimum of 10%")
	def script_down(self, gesture):
		targetVolume = self.getVolume() - 2
		self.setVolume(targetVolume)
		ui.message(f"{self.getVolume()}%")

	@script(description="Increases system  volume by 10%")
	def script_pageUp(self, gesture):
		targetVolume = self.getVolume() + 10
		self.setVolume(targetVolume)
		ui.message(f"{self.getVolume()}%")

	@script(description="Decreases system  volume by 10% to a minimum of 10%")
	def script_pageDown(self, gesture):
		targetVolume = self.getVolume() - 10
		self.setVolume(targetVolume)
		ui.message(f"{self.getVolume()}%")

	@script(description="Sets system  volume to 10%")
	def script_home(self, gesture):
		targetVolume = 10
		self.setVolume(targetVolume)
		ui.message(f"{targetVolume}%")

	@script(description="Sets system  volume to 100%")
	def script_end(self, gesture):
		targetVolume = 100
		self.setVolume(targetVolume)
		ui.message(f"{targetVolume} percent")

	def getVolume(self):
		volume = self.getVolumeInterface().GetMasterVolumeLevelScalar()
		return round(volume * 100)

	def setVolume(self, target):
		if target < 10: 
			target = 10
		elif target > 100:
			target = 100
		self.getVolumeInterface().SetMasterVolumeLevelScalar(target / 100, None)

	def getVolumeInterface(self):
		device = AudioUtilities.GetSpeakers()
		endpoint = device.Activate(
			IAudioEndpointVolume._iid_,
			CLSCTX_ALL,
			None
		)
		return endpoint.QueryInterface(IAudioEndpointVolume)