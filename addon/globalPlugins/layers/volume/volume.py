# layers/volume/volume.py
# A part of the Layered Commands NVDA addon
# Layer to redirect to volume control layers
# Copyright (C) Matthew Duffell-Hoffman
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

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

	@script(description="Activates the sound splitting layer")
	def script_balance(self, gesture):
		# Translators: Announced when sound splitting layer is activated
		ui.message(_("balance"))
		self._handler.setActiveLayer("volume-balance")

	@script(description="Activates the sound card layer")
	def script_card(self, gesture):
		# Translators: Announced when sound card layer is activated
		ui.message(_("sound card"))
		self._handler.setActiveLayer("volume-card")

	@script(description="Activates the NVDA volume  layer")
	def script_nvda(self, gesture):
		# Translators: Announced when NVDA layer is activated
		ui.message(_("NVDA"))
		self._handler.setActiveLayer("volume-nvda")

	@script(description="Activates the system volume layer")
	def script_system(self, gesture):
		# Translators: Announced when sound splitting layer is activated
		ui.message(_("system"))
		self._handler.setActiveLayer("volume-system")

	@script(description="Toggles system mute")
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
			# Translators: Announced when system is unmuted
			ui.message(_("Unmuted"))
		else:
			volume.SetMute(1, None)