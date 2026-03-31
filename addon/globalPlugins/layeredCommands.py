# layeredCommands.py
# A part of the Layered Commands NVDA addon
# Copyright (C) Matthew Duffell-Hoffman
# This file is covered by the GNU General Public License.

import globalPluginHandler
import globalCommands
from scriptHandler import script
import tones
import ui

from . import layers

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self):
		super().__init__()
		self.activeLayer = None
		self.layers = {}
		self.addLayer(layers.FirstLayer)
		self.addLayer(layers.VolumeLayer)
		self.addLayer(layers.volume.BalanceLayer)
		self.addLayer(layers.volume.CardLayer)
		self.addLayer(layers.volume.NVDALayer)
		self.addLayer(layers.volume.SystemLayer)

	def addLayer(self, cls):
		layer = cls(self)
		self.layers[layer.getName()] = layer

	def setActiveLayer(self, name):
		self.activeLayer = self.layers[name]

	def getScript(self, gesture):
		"""Retrieve the script bound to a given gesture.
		@param gesture: The input gesture in question.
		@type gesture: L{inputCore.InputGesture}
		@return: The script function or C{None} if none was found.
		@rtype: script function
		"""
		if self.activeLayer == None:
			return super().getScript(gesture)

		for identifier in gesture.normalizedIdentifiers:
			try:
				# Convert to instance method.
				return self.activeLayer.getGestureMap()[identifier]
			except KeyError:
				continue
			except AttributeError:
				log.exception(
					f"Base class may not have been initialized.\nMRO={self.__class__.__mro__}"
					if not hasattr(self, "activeLayer._gestureMap")
					else None,
				)
				return None
		else:
			return self.script_close

	@script(
		description=_("Activates Layered Command mode"),
		category=globalCommands.SCRCAT_INPUT,
		gesture="kb:NVDA+alt+space"
	)
	def script_layeredCommand(self, gesture):
		tones.beep(550, 50)
		self.activeLayer = self.layers["first"]

	@script()
	def script_close(self, gesture):
		tones.beep(300, 50)
		self.activeLayer = None