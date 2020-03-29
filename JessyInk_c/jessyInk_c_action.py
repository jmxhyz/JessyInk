#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
		self.OptionParser.add_option('--actiontype', action = 'store', type = 'string', dest = 'actiontype', default = 'none')
		self.OptionParser.add_option('--jumpslide', action = 'store', type = 'string', dest = 'jumpslide', default = 0)
		self.OptionParser.add_option('--jumpeffect', action = 'store', type = 'string', dest = 'jumpeffect', default = 0)

		inkex.NSS["jessyink"] = "https://launchpad.net/jessyink"

	def effect(self):
		# Check version.
		scriptNodes = self.document.xpath("//svg:script[@jessyink:version='1.5.6']", namespaces=inkex.NSS)

		if len(scriptNodes) != 1:
			inkex.errormsg(_(u"JessyInk_c 还未安装到这个SVG文件，或者版本不同. 请使用 “扩展” 菜单下 “JessyInk_c” 的 “安装/升级...” 命令进行JessyInk_c 的安装。\n\n"))

		if len(self.selected) == 0:
			inkex.errormsg(_(u"进行设置前，请先选择一个对象。\n"))

		for id, node in list(self.selected.items()):
			if (self.options.actiontype == "none"):
				# Remove possible action.
				if "onmousedown" in node.attrib:
					del node.attrib["onmousedown"]
				if "onclick" in node.attrib:
					del node.attrib["onclick"]
				if "ondblclick" in node.attrib:
					del node.attrib["ondblclick"]
			if (self.options.actiontype == "drag"):
				node.set("onmousedown","mydrag(evt)")
			if (self.options.actiontype == "jump"):
				node.set("onclick","jumpto(" + self.options.jumpslide + "," + self.options.jumpeffect + ")")
			if (self.options.actiontype == "fold"):
				if "transform" in node.attrib:
					#inkex.errormsg(_(','.join(dir(node))))
					#inkex.errormsg(_(node.__getattribute__('transform')))
					#inkex.errormsg(_(','.join(node.attrib.values())))
					#return
					s_matrix = ''.join(node.attrib.values())
					if "matrix" in s_matrix:
						node.set("onclick","this.style.transform='scale(1,1)'")
						node.set("ondblclick","this.style.transform=''")
						return
				#else:
				node.set("onmousedown","mydrag(evt, 1)")

# Create effect instance
effect = JessyInk_Effects()
effect.affect()
