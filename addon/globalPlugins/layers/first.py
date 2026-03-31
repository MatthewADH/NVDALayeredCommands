# layers/first.py
# A part of the Layered Commands NVDA addon
# Copyright (C) Matthew Duffell-Hoffman
# This file is covered by the GNU General Public License.

import api
import config
from documentBase import DocumentWithTableNavigation
import globalCommands
import scriptHandler
from scriptHandler import script
import speech
import speechViewer
import textInfos
import ui

from .layer import Layer
from .table import TableLayer

class FirstLayer(Layer):
	def __init__(self, handler):
		name = "first"
		gestureMap = {
			"kb:f11": self.script_screenCurtain,
			"kb:c": self.script_clipboard,
			"kb:d": self.script_ducking,
			"kb:h": self.script_speechHistory,
			"kb:control+n": self.script_toastNotifications,
			"kb:s": self.script_speech,
			"kb:s+shift": self.script_speechMute,
			"kb:t": self.script_table,
			"kb:v": self.script_volume
		}
		helpFile = "first.help.html"
		super().__init__(name, gestureMap, handler, helpFile)

	@script()
	def script_screenCurtain(self, gesture):
		scriptHandler.executeScript(globalCommands.commands.script_toggleScreenCurtain, gesture)
		scriptHandler.executeScript(self._handler.script_close, gesture)

	@script()
	def script_clipboard(self, gesture):
		scriptHandler.executeScript(globalCommands.commands.script_reportClipboardText, gesture)
		scriptHandler.executeScript(self._handler.script_close, gesture)

	@script()
	def script_ducking(self, gesture):
		scriptHandler.executeScript(globalCommands.commands.script_cycleAudioDuckingMode, gesture)
		scriptHandler.executeScript(self._handler.script_close, gesture)

	@script()
	def script_speechHistory(self, gesture):
		scriptHandler.executeScript(globalCommands.commands.script_toggleSpeechViewer, gesture)
		scriptHandler.executeScript(self._handler.script_close, gesture)

	@script()
	def script_toastNotifications(self, gesture):
		if config.conf["presentation"]["reportHelpBalloons"]:
			config.conf["presentation"]["reportHelpBalloons"] = False
			ui.message(_("Report notifications off"))
		else:
			config.conf["presentation"]["reportHelpBalloons"] = True
			ui.message(_("Report notifications on"))
		scriptHandler.executeScript(self._handler.script_close, gesture)

	@script()
	def script_speech(self, gesture):
		curMode = speech.getState().speechMode
		speech.setSpeechMode(speech.SpeechMode.talk)
		speech.cancelSpeech()
		if curMode == speech.SpeechMode.talk:
			newMode = speech.SpeechMode.onDemand
		else:
			newMode = speech.SpeechMode.talk
		# Translators: Announced when user switches to another speech mode.
		# 'mode' is replaced with the translated name of the new mode.
		ui.message(_("Speech mode {mode}").format(mode=newMode.displayString))
		speech.setSpeechMode(newMode)
		scriptHandler.executeScript(self._handler.script_close, gesture)

	@script()
	def script_speechMute(self, gesture):
		curMode = speech.getState().speechMode
		speech.setSpeechMode(speech.SpeechMode.talk)
		speech.cancelSpeech()
		if curMode == speech.SpeechMode.off:
			newMode = speech.SpeechMode.onDemand
		else:
			newMode = speech.SpeechMode.off
		# Translators: Announced when user switches to another speech mode.
		# 'mode' is replaced with the translated name of the new mode.
		ui.message(_("Speech mode {mode}").format(mode=newMode.displayString))
		speech.setSpeechMode(newMode)
		scriptHandler.executeScript(self._handler.script_close, gesture)

	@script()
	def script_table(self, gesture):
		obj = api.getCaretObject()
		if not hasattr(obj, '_maybeGetLayoutTableIds'):
			ui.message('not in a table')
			scriptHandler.executeScript(self._handler.script_close, gesture)
			return
		info = obj.selection
		if info.isCollapsed:
			info = info.copy()
			info.expand(textInfos.UNIT_CHARACTER)
		fields = list(info.getTextWithFields())
		layoutIDs = obj._maybeGetLayoutTableIds(info)
		for field in reversed(fields):
			if not (isinstance(field, textInfos.FieldCommand) and field.command == "controlStart"):
				# Not a control field.
				continue
			attrs = field.field
			tableID = attrs.get("table-id")
			if tableID is None or tableID in layoutIDs:
				continue
			if "table-columnnumber" in attrs and not attrs.get("table-layout"):
				break
		else:
			ui.message('not in a table')
			scriptHandler.executeScript(self._handler.script_close, gesture)
			return
		ui.message('table layer')
		self._handler.activeLayer = TableLayer(self._handler, obj)

	@script()
	def script_volume(self, gesture):
		ui.message("volume")
		self._handler.setActiveLayer("volume")