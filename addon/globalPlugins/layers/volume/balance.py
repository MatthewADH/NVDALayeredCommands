# layers/volume/balance.py
# A part of the Layered Commands NVDA addon
# Copyright (C) Matthew Duffell-Hoffman
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import audio 
import scriptHandler
from scriptHandler import script
import ui

from ..layer import Layer

class BalanceLayer(Layer):
	def __init__(self, handler):
		name = "volume-balance"
		helpFile = "volume\\balance.help.html"
		gestureMap = {
			"kb:uparrow": self.script_off,
			"kb:leftarrow": self.script_left,
			"kb:rightarrow": self.script_right
		}
		super().__init__(name, gestureMap, handler, helpFile)

	@script()
	def script_off(self, gesture):
		audio._setSoundSplitState(audio.SoundSplitState.NVDA_BOTH_APPS_BOTH)
		ui.message(audio.SoundSplitState.NVDA_BOTH_APPS_BOTH.displayString)
		scriptHandler.executeScript(self._handler.script_close, gesture)

	@script()
	def script_left(self, gesture):
		audio._setSoundSplitState(audio.SoundSplitState.NVDA_LEFT_APPS_RIGHT)
		ui.message(audio.SoundSplitState.NVDA_LEFT_APPS_RIGHT.displayString)
		scriptHandler.executeScript(self._handler.script_close, gesture)

	@script()
	def script_right(self, gesture):
		audio._setSoundSplitState(audio.SoundSplitState.NVDA_RIGHT_APPS_LEFT)
		ui.message(audio.SoundSplitState.NVDA_RIGHT_APPS_LEFT.displayString)
		scriptHandler.executeScript(self._handler.script_close, gesture)