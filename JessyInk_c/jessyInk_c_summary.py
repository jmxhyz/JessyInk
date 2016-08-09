#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2008, 2009, 2010, 2011 Hannes Hochreiner
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.

# These lines are only needed if you don't put the script directly into
# the installation directory
import sys
# Unix
sys.path.append('/usr/share/inkscape/extensions')
# OS X
sys.path.append('/Applications/Inkscape.app/Contents/Resources/extensions')
# Windows
sys.path.append('C:\Program Files\Inkscape\share\extensions')

# We will use the inkex module with the predefined Effect base class.
import inkex
import gettext
_ = gettext.gettext

def propStrToList(str):
	list = []
	propList = str.split(";")
	for prop in propList:
		if not (len(prop) == 0):
			list.append(prop.strip())
	return list

def propListToDict(list):
	dictio = {}

	for prop in list:
		keyValue = prop.split(":")

		if len(keyValue) == 2:
			dictio[keyValue[0].strip()] = keyValue[1].strip()

	return dictio

class JessyInk_Summary(inkex.Effect):
	def __init__(self):
		# Call the base class constructor.
		inkex.Effect.__init__(self)

		self.OptionParser.add_option('--tab', action = 'store', type = 'string', dest = 'what')

		inkex.NSS["jessyink"] = "https://launchpad.net/jessyink"

	def effect(self):
		# Check version.
		scriptNodes = self.document.xpath("//svg:script[@jessyink:version='1.5.6']", namespaces=inkex.NSS)

		if len(scriptNodes) != 1:
			inkex.errormsg(_(u"JessyInk_c 还未安装到这个SVG文件，或者版本不同. 请使用 “扩展” 菜单下 “JessyInk_c” 的 “安装/升级...” 命令进行JessyInk_c 的安装。\n\n"))

		# Find the script node, if present
		for node in self.document.xpath("//svg:script[@id='JessyInk']", namespaces=inkex.NSS):
			if node.get("{" + inkex.NSS["jessyink"] + "}version"):
				inkex.errormsg(_(u"安装的 JessyInk_c 版本是 {0}。").format(node.get("{" + inkex.NSS["jessyink"] + "}version")))
			else:
				inkex.errormsg(_(u"JessyInk_c 已安装。"))
	
		slides = []
		masterSlide = None 

		for node in self.document.xpath("//svg:g[@inkscape:groupmode='layer']", namespaces=inkex.NSS):
			if node.get("{" + inkex.NSS["jessyink"] + "}masterSlide"):
				masterSlide = node
			else:
				slides.append(node)

		if masterSlide is not None:
			inkex.errormsg(_(u"\n幻灯片母板:"))
			self.describeNode(masterSlide, "\t", u"<幻灯片（层）序号>", str(len(slides)), u"<幻灯片（层）名字>")

		slideCounter = 1

		for slide in slides:
			inkex.errormsg(_(u"\n幻灯片 {0!s}:").format(slideCounter))
			self.describeNode(slide, "\t", str(slideCounter), str(len(slides)), slide.get("{" + inkex.NSS["inkscape"] + "}label"))
			slideCounter += 1

	def describeNode(self, node, prefix, slideNumber, numberOfSlides, slideTitle):
		if sys.version_info.major < 3:
			inkex.errormsg(_(u"{0}幻灯片（层）名: {1}").format(prefix, node.get("{" + inkex.NSS["inkscape"] + "}label")))
		else:
			inkex.errormsg(_("{0}幻灯片（层）名: {1}").format(prefix, node.get("{" + inkex.NSS["inkscape"] + "}label")))
		
		# Display information about transitions.
		transitionInAttribute = node.get("{" + inkex.NSS["jessyink"] + "}transitionIn")
		if transitionInAttribute:
			transInDict = propListToDict(propStrToList(transitionInAttribute))

			if (transInDict["name"] != "appear") and "length" in transInDict:
				inkex.errormsg(_(u"{0}进场特效: {1} ({2!s} s)").format(prefix, transInDict["name"], int(transInDict["length"]) / 1000.0))
			else:
				inkex.errormsg(_(u"{0}进场特效: {1}").format(prefix, transInDict["name"]))

		transitionOutAttribute = node.get("{" + inkex.NSS["jessyink"] + "}transitionOut")
		if transitionOutAttribute:
			transOutDict = propListToDict(propStrToList(transitionOutAttribute))

			if (transOutDict["name"] != "appear") and "length" in transOutDict:
				inkex.errormsg(_(u"{0}退场特效: {1} ({2!s} s)").format(prefix, transOutDict["name"], int(transOutDict["length"]) / 1000.0))
			else:
				inkex.errormsg(_(u"{0}退场特效: {1}").format(prefix, transOutDict["name"]))

		# Display information about auto-texts.
		autoTexts = {"slideNumber" : slideNumber, "numberOfSlides" : numberOfSlides, "slideTitle" : slideTitle}
		autoTextNodes = node.xpath(".//*[@jessyink:autoText]", namespaces=inkex.NSS)
		
		if (len(autoTextNodes) > 0):
			inkex.errormsg(_(u"\n{0}自动文字:").format(prefix))
			
			for atNode in autoTextNodes:
				inkex.errormsg(_(u"{0}\t\"{1}\" (对象 id \"{2}\") 将被替换为 \"{3}\".").format(prefix, atNode.text, atNode.getparent().get("id"), autoTexts[atNode.get("{" + inkex.NSS["jessyink"] + "}autoText")]))

		# Collect information about effects.
		effects = {}

		for effectNode in node.xpath(".//*[@jessyink:effectIn]", namespaces=inkex.NSS):
			dictio = propListToDict(propStrToList(effectNode.get("{" + inkex.NSS["jessyink"] + "}effectIn")))
			dictio["direction"] = "in"
			dictio["id"] = effectNode.get("id")
			dictio["type"] = "effect"

			if dictio["order"] not in effects:
				effects[dictio["order"]] = []

			effects[dictio["order"]].append(dictio)

		for effectNode in node.xpath(".//*[@jessyink:effectOut]", namespaces=inkex.NSS):
			dictio = propListToDict(propStrToList(effectNode.get("{" + inkex.NSS["jessyink"] + "}effectOut")))
			dictio["direction"] = "out"
			dictio["id"] = effectNode.get("id")
			dictio["type"] = "effect"

			if dictio["order"] not in effects:
				effects[dictio["order"]] = []

			effects[dictio["order"]].append(dictio)

		for viewNode in node.xpath(".//*[@jessyink:view]", namespaces=inkex.NSS):
			dictio = propListToDict(propStrToList(viewNode.get("{" + inkex.NSS["jessyink"] + "}view")))
			dictio["id"] = viewNode.get("id")
			dictio["type"] = "view"

			if dictio["order"] not in effects:
				effects[dictio["order"]] = []

			effects[dictio["order"]].append(dictio)

		order = sorted(effects.keys())
		orderNumber = 0

		# Display information about effects.
		for orderItem in order:
			tmpStr = ""

			if orderNumber == 0:
				tmpStr += _(u"\n{0}初始特效 (次序 {1}):").format(prefix, effects[orderItem][0]["order"])
			else:
				tmpStr += _(u"\n{0}特效 {1!s} (次序 {2}):").format(prefix, orderNumber, effects[orderItem][0]["order"])
		
			for item in effects[orderItem]:
				if item["type"] == "view":
					tmpStr += _(u"{0}\t视域将绑定到对象 \"{1}\"").format(prefix, item["id"])
				else:
					tmpStr += _(u"{0}\t对象 \"{1}\"").format(prefix, item["id"])
	
					if item["direction"] == "in":
						tmpStr += _(u" 显示用")
					elif item["direction"] == "out":
						tmpStr += _(u" 消失用")
	
				if item["name"] != "appear":
					tmpStr += _(u" 特效 \"{0}\"").format(item["name"])
					
				if "length" in item:
					tmpStr += _(u" 持续 {0!s} s").format(int(item["length"]) / 1000.0)

				inkex.errormsg(tmpStr + ".\n")

			orderNumber += 1

# Create effect instance
effect = JessyInk_Summary()
effect.affect()
