# layers/first.py
# A part of the Layered Commands NVDA addon
# Root layer, basic commands and branches to other layers 
# Copyright (C) Matthew Duffell-Hoffman
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import api
import config
import globalCommands
import scriptHandler
from scriptHandler import script
import speech
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

	@script(description="toggle screen curtain on/off")
	def script_screenCurtain(self, gesture):
		scriptHandler.executeScript(globalCommands.commands.script_toggleScreenCurtain, gesture)
		scriptHandler.executeScript(self._handler.script_close, gesture)

	@script(description="Announce text on clipboard")
	def script_clipboard(self, gesture):
		scriptHandler.executeScript(globalCommands.commands.script_reportClipboardText, gesture)
		scriptHandler.executeScript(self._handler.script_close, gesture)

	@script(description="Cycle audio ducking mode")
	def script_ducking(self, gesture):
		scriptHandler.executeScript(globalCommands.commands.script_cycleAudioDuckingMode, gesture)
		scriptHandler.executeScript(self._handler.script_close, gesture)

	@script(description="Toggle Speech Viewer on/off")
	def script_speechHistory(self, gesture):
		scriptHandler.executeScript(globalCommands.commands.script_toggleSpeechViewer, gesture)
		scriptHandler.executeScript(self._handler.script_close, gesture)

	@script(description="Toggle notification announcements")
	def script_toastNotifications(self, gesture):
		if config.conf["presentation"]["reportHelpBalloons"]:
			config.conf["presentation"]["reportHelpBalloons"] = False
			# Translators: Notification reporting toggled off
			ui.message(_("Report notifications off"))
		else:
			config.conf["presentation"]["reportHelpBalloons"] = True
			# Translators: Notification reporting toggled on
			ui.message(_("Report notifications on"))
		scriptHandler.executeScript(self._handler.script_close, gesture)

	@script(description="Toggle speech mode between talk and on demand")
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

	@script(description="Toggle speech mode between on demand and off")
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

	@script(description="Activate table layer")
	def script_table(self, gesture):
		obj = api.getCaretObject()
		if not hasattr(obj, '_maybeGetLayoutTableIds'):
			# Translators: Announced when table layer attempted to activate while not in a table cell
			ui.message(_("not in a table"))
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
			# Translators: Announced when table layer attempted to activate while not in a table cell
			ui.message(_("not in a table"))
			scriptHandler.executeScript(self._handler.script_close, gesture)
			return
		# Translators: Announced when table layer activated
		ui.message(_("table layer"))
		# Table layer must be instantiated on activation using the spacific table object
		self._handler.activeLayer = TableLayer(self._handler, obj)

	@script(description="Activates the volume layer")
	def script_volume(self, gesture):
		# Translators: Announced on activation of the volume layer
		ui.message(_("volume"))
		self._handler.setActiveLayer("volume")