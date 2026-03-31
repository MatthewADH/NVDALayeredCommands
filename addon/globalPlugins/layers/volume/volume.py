# layers/volume/volume.py
# A part of the Layered Commands NVDA addon
# Copyright (C) Matthew Duffell-Hoffman
# This file is covered by the GNU General Public License.

from comtypes import CLSCTX_ALL
from pycaw.api.endpointvolume import IAudioEndpointVolume
from pycaw.utils import AudioUtilities
from scriptHandler import script
import ui

from ..layer import Layer

class VolumeLayer(Layer):
	def __init__(self, handler):
		name = "volume"
		helpFile = "volume\\volume.help.html"
		gestureMap = {
			"kb:b": self.script_balance,
			"kb:c": self.script_card,
			"kb:n": self.script_nvda,
			"kb:s": self.script_system,
			"kb:m": self.script_mute
		}
		super().__init__(name, gestureMap, handler, helpFile)

	@script()
	def script_balance(self, gesture):
		ui.message("balance")
		self._handler.setActiveLayer("volume-balance")

	@script()
	def script_card(self, gesture):
		ui.message("sound card")
		self._handler.setActiveLayer("volume-card")

	@script()
	def script_nvda(self, gesture):
		ui.message("NVDA")
		self._handler.setActiveLayer("volume-nvda")

	@script()
	def script_system(self, gesture):
		ui.message("system")
		self._handler.setActiveLayer("volume-system")

	@script()
	def script_mute(self, gesture):
		device = AudioUtilities.GetSpeakers()
		endpoint = device.Activate(
			IAudioEndpointVolume._iid_,
			CLSCTX_ALL,
			None
		)
		volume = endpoint.QueryInterface(IAudioEndpointVolume)

		if volume.GetMute():
			volume.SetMute(0, None)
			ui.message(_("Unmuted"))
		else:
			volume.SetMute(1, None)

