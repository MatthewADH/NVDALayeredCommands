# layers/layer.py
# A part of the Layered Commands NVDA addon
# Layer class to be inherited by layers, contains gesture map and help message
# Copyright (C) Matthew Duffell-Hoffman
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from pathlib import Path

import scriptHandler
from scriptHandler import script
import ui


class Layer():
	def __init__(self, name, gestureMap, handler, helpFile=None):
		self._name = name
		self._gestureMap = gestureMap
		self._handler = handler
		self._helpFile = helpFile
		self._gestureMap["kb:/"] = self.script_helpMessage
		self._gestureMap["kb:/+shift"] = self.script_helpMessage
		try:
			
			helpPath = Path(__file__).parent / helpFile
			with open(helpPath, 'r') as file:
				self._helpMessage= file.read()
		except Exception as e:
			self._helpMessage = None

	def getName(self):
		return self._name

	def getGestureMap(self):
		return self._gestureMap

	@script(description="Displays the help window for the layer if available")
	def script_helpMessage(self, gesture):
		if self._helpMessage:
			ui.browseableMessage(
				self._helpMessage,
				# Translators: title for layer helpdialog.
				_("Layer Help"),
				closeButton=True,
				isHtml = True
			)
			scriptHandler.executeScript(self._handler.script_close, gesture)
		else:
			# Translators: Announced when help window is requested but unavailible 
			ui.message("no help message availible")