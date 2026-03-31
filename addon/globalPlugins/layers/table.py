# layers/table.py
# A part of the Layered Commands NVDA addon
# Copyright (C) Matthew Duffell-Hoffman
# This file is covered by the GNU General Public License.

import api
import config
import controlTypes
from documentBase import _Movement, _Axis
import scriptHandler
from scriptHandler import script
import speech
import ui

from .layer import Layer

class TableLayer(Layer):
	def __init__(self, handler, obj):
		name = "table"
		self._obj = obj
		helpFile = "table.help.html"
		gestureMap = {
			"kb:downarrow": obj.script_nextRow,
			"kb:uparrow": obj.script_previousRow,
			"kb:rightarrow": obj.script_nextColumn,
			"kb:leftarrow": obj.script_previousColumn,
			"kb:numpad2": obj.script_nextRow,
			"kb:numpad8": obj.script_previousRow,
			"kb:numpad6": obj.script_nextColumn,
			"kb:numpad4": obj.script_previousColumn,
			"kb:pageup": obj.script_firstRow,
			"kb:pagedown": obj.script_lastRow,
			"kb:home": obj.script_firstColumn,
			"kb:end": obj.script_lastColumn,
			"kb:numpad9": obj.script_firstRow,
			"kb:numpad3": obj.script_lastRow,
			"kb:numpad7": obj.script_firstColumn,
			"kb:numpad1": obj.script_lastColumn,
			"kb:control+uparrow": obj.script_firstRow,
			"kb:control+downarrow": obj.script_lastRow,
			"kb:control+leftarrow": obj.script_firstColumn,
			"kb:control+rightarrow": obj.script_lastColumn,
			"kb:nvda+rightarrow": obj.script_sayAllRow,
			"kb:downarrow+nvda": obj.script_sayAllColumn,
			"kb:leftarrow+nvda": obj.script_speakRow,
			"kb:nvda+uparrow": obj.script_speakColumn,
			"kb:pageup+shift": obj.script_sayAllRow,
			"kb:pagedown+shift": obj.script_sayAllColumn,
			"kb:numpad9+shift": obj.script_sayAllRow,
			"kb:numpad3+shift": obj.script_sayAllColumn,
			"kb:shift+uparrow": obj.script_speakRow,
			"kb:numpad5+shift": obj.script_speakColumn,
			"kb:numpad5": self.script_sayCurrentCell,
			"kb:control+home": self.script_firstCell,
			"kb:control+numpad7": self.script_firstCell,
			"kb:control+end": self.script_lastCell,
			"kb:control+numpad1": self.script_lastCell,

		}
		if hasattr(obj, "script_nextTable"):
			gestureMap["kb:control+enter"] = obj.script_nextTable
			gestureMap["kb:control+numpadenter"] = obj.script_nextTable
		else:
			gestureMap["kb:control+enter"] = self.script_nextTableNotSupported
			gestureMap["kb:control+numpadenter"] = self.script_nextTableNotSupported
		if hasattr(obj, "script_previousTable"):
			gestureMap["kb:control+enter+shift"] = obj.script_previousTable
			gestureMap["kb:control+numpadenter+shift"] = obj.script_previousTable
		else:
			gestureMap["kb:control+enter+shift"] = self.script_previousTableNotSupported
			gestureMap["kb:control+numpadenter+shift"] = self.script_previousTableNotSupported

		super().__init__(name, gestureMap, handler, helpFile)

	@script()
	def script_sayCurrentCell(self, gesture):
		formatConfig = config.conf["documentFormatting"].copy()
		formatConfig["reportTables"] = True
		cell = self._obj._getTableCellCoordsCached(self._obj.selection)
		info = self._obj._getTableCellAt(cell.tableID, self._obj.selection, cell.row, cell.col)
		speech.speakTextInfo(info, formatConfig=formatConfig, reason=controlTypes.OutputReason.QUERY)

	@script()
	def script_nextTableNotSupported(self, gesture):
		ui.message("next table is not supported in this context")

	@script()
	def script_previousTableNotSupported(self, gesture):
		ui.message("previous table is not supported in this context")

	@script()
	def script_firstCell(self, gesture):
		ui.message("first cell")
		curMode = speech.getState().speechMode
		speech.setSpeechMode(speech.SpeechMode.off)
		speech.cancelSpeech()
		self._obj._tableMovementScriptHelper(axis=_Axis.ROW, movement=_Movement.FIRST)
		speech.setSpeechMode(curMode )
		self._obj._tableMovementScriptHelper(axis=_Axis.COLUMN, movement=_Movement.FIRST)

	@script()
	def script_lastCell(self, gesture):
		ui.message("last cell")
		curMode = speech.getState().speechMode
		speech.setSpeechMode(speech.SpeechMode.off)
		speech.cancelSpeech()
		self._obj._tableMovementScriptHelper(axis=_Axis.ROW, movement=_Movement.LAST)
		speech.setSpeechMode(curMode )
		self._obj._tableMovementScriptHelper(axis=_Axis.COLUMN, movement=_Movement.LAST)
