# layers/volume/nvda.py
# A part of the Layered Commands NVDA addon
# Copyright (C) Matthew Duffell-Hoffman
# This file is covered by the GNU General Public License.

from scriptHandler import script
from synthDriverHandler import getSynth
import ui

from ..layer import Layer

class NVDALayer(Layer):
	def __init__(self, handler):
		name = "volume-nvda"
		helpFile = "volume\\nvda.help.html"
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
			"kb:numpad1": self.script_end
		}
		super().__init__(name, gestureMap, handler, helpFile)

	@script()
	def script_up(self, gesture):
		targetVolume = self.getVolume() + 2
		targetVolume = self.clamp(targetVolume, 10, 100)
		self.setVolume(targetVolume)
		ui.message(f"{targetVolume} percent")

	@script()
	def script_down(self, gesture):
		targetVolume = self.getVolume() - 2
		targetVolume = self.clamp(targetVolume, 10, 100)
		self.setVolume(targetVolume)
		ui.message(f"{targetVolume} percent")

	@script()
	def script_pageUp(self, gesture):
		targetVolume = self.getVolume() + 10
		targetVolume = self.clamp(targetVolume, 10, 100)
		self.setVolume(targetVolume)
		ui.message(f"{targetVolume} percent")

	@script()
	def script_pageDown(self, gesture):
		targetVolume = self.getVolume() - 10
		targetVolume = self.clamp(targetVolume, 10, 100)
		self.setVolume(targetVolume)
		ui.message(f"{targetVolume} percent")

	@script()
	def script_home(self, gesture):
		targetVolume = 10
		self.setVolume(targetVolume)
		ui.message(f"{targetVolume} percent")

	@script()
	def script_end(self, gesture):
		targetVolume = 100
		self.setVolume(targetVolume)
		ui.message(f"{targetVolume} percent")

	def getVolume(self):
		return getSynth()._get_volume()

	def setVolume(self, target):
		getSynth()._set_volume(target)

	def clamp(self, num, min, max):
		if num < min: return min
		if num > max: return max
		return num