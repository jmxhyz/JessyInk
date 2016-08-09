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

class JessyInk_Effects(inkex.Effect):
	def __init__(self):
		# Call the base class constructor.
		inkex.Effect.__init__(self)

		self.OptionParser.add_option('--tab', action = 'store', type = 'string', dest = 'what')
		self.OptionParser.add_option('--effectInOrder', action = 'store', type = 'string', dest = 'effectInOrder', default = 1)
		self.OptionParser.add_option('--effectInDuration', action = 'store', type = 'float', dest = 'effectInDuration', default = 0.8)
		self.OptionParser.add_option('--effectIn', action = 'store', type = 'string', dest = 'effectIn', default = 'none')
		self.OptionParser.add_option('--effectOutOrder', action = 'store', type = 'string', dest = 'effectOutOrder', default = 2)
		self.OptionParser.add_option('--effectOutDuration', action = 'store', type = 'float', dest = 'effectOutDuration', default = 0.8)
		self.OptionParser.add_option('--effectOut', action = 'store', type = 'string', dest = 'effectOut', default = 'none')

		inkex.NSS["jessyink"] = "https://launchpad.net/jessyink"

	def effect(self):
		# Check version.
		scriptNodes = self.document.xpath("//svg:script[@jessyink:version='1.5.6']", namespaces=inkex.NSS)

		if len(scriptNodes) != 1:
			inkex.errormsg(_(u"JessyInk_c 还未安装到这个SVG文件，或者版本不同. 请使用 “扩展” 菜单下 “JessyInk_c” 的 “安装/升级...” 命令进行JessyInk_c 的安装。\n\n"))

		if len(self.selected) == 0:
			inkex.errormsg(_(u"没有选择操作对象。请选择一个要设置演示特效的对象。\n"))

		for id, node in list(self.selected.items()):
			if (self.options.effectIn == "appear") or (self.options.effectIn == "fade") or (self.options.effectIn == "pop") or (self.options.effectIn == "tata"):
				node.set("{" + inkex.NSS["jessyink"] + "}effectIn","name:" + self.options.effectIn  + ";order:" + self.options.effectInOrder + ";length:" + str(int(self.options.effectInDuration * 1000)))
				# Remove possible view argument.
				if "{" + inkex.NSS["jessyink"] + "}view" in node.attrib:
					del node.attrib["{" + inkex.NSS["jessyink"] + "}view"]
			else:
				if "{" + inkex.NSS["jessyink"] + "}effectIn" in node.attrib:
					del node.attrib["{" + inkex.NSS["jessyink"] + "}effectIn"]
		
			if (self.options.effectOut == "appear") or (self.options.effectOut == "fade") or (self.options.effectOut == "pop"):
				node.set("{" + inkex.NSS["jessyink"] + "}effectOut","name:" + self.options.effectOut  + ";order:" + self.options.effectOutOrder + ";length:" + str(int(self.options.effectOutDuration * 1000)))
				# Remove possible view argument.
				if "{" + inkex.NSS["jessyink"] + "}view" in node.attrib:
					del node.attrib["{" + inkex.NSS["jessyink"] + "}view"]
			else:
				if "{" + inkex.NSS["jessyink"] + "}effectOut" in node.attrib:
					del node.attrib["{" + inkex.NSS["jessyink"] + "}effectOut"]

# Create effect instance
effect = JessyInk_Effects()
effect.affect()

