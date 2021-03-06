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

class JessyInk_MasterSlide(inkex.Effect):
	def __init__(self):
		# Call the base class constructor.
		inkex.Effect.__init__(self)

		self.OptionParser.add_option('--tab', action = 'store', type = 'string', dest = 'what')
		self.OptionParser.add_option('--layerName', action = 'store', type = 'string', dest = 'layerName', default = '')

		inkex.NSS["jessyink"] = "https://launchpad.net/jessyink"

	def effect(self):
		# Check version.
		scriptNodes = self.document.xpath("//svg:script[@jessyink:version='1.5.6']", namespaces=inkex.NSS)

		if len(scriptNodes) != 1:
			inkex.errormsg(_(u"JessyInk_c 还未安装到这个SVG文件，或者版本不同. 请使用 “扩展” 菜单下 “JessyInk_c” 的 “安装/升级...” 命令进行JessyInk_c 的安装。\n\n"))

		# Remove old master slide property
		for node in self.document.xpath("//*[@jessyink:masterSlide='masterSlide']", namespaces=inkex.NSS):
			del node.attrib["{" + inkex.NSS["jessyink"] + "}masterSlide"]

		# Set new master slide.
		if self.options.layerName != "":
			nodes = self.document.xpath("//*[@inkscape:groupmode='layer' and @inkscape:label='" + self.options.layerName + "']", namespaces=inkex.NSS)
			if len(nodes) == 0:
				inkex.errormsg(_(u"含有幻灯片母板的SVG层没找到。\n"))
			elif len(nodes) > 1:
				inkex.errormsg(_(u"多个SVG层含有这个名字。无法移除幻灯片母板\n"))
			else:
				nodes[0].set("{" + inkex.NSS["jessyink"] + "}masterSlide","masterSlide")

# Create effect instance
effect = JessyInk_MasterSlide()
effect.affect()

