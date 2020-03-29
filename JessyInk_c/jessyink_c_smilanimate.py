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
		self.OptionParser.add_option("--tab", action="store", type="string", dest="tab", default="Options")

		self.OptionParser.add_option('--smilbegin', type = 'string', dest = 'smilbegin') #action = 'store',
		self.OptionParser.add_option('--smilend',  type = 'string', dest = 'smilend') #action = 'store',
		self.OptionParser.add_option('--smilDuration', action = 'store', type = 'string', dest = 'smilDuration')
		self.OptionParser.add_option('--smilrepeatCount', type = 'string', dest = 'smilrepeatCount') #action = 'store', 
		self.OptionParser.add_option('--smiltype', action = 'store', type = 'string', dest = 'smiltype')
		self.OptionParser.add_option('--Gswitch', type = 'inkbool', dest = 'Gswitch') # action = 'store',
		#transForm
		self.OptionParser.add_option('--transfrom', type = 'string', dest = 'transfrom') #action = 'store',
		self.OptionParser.add_option('--transto',   type = 'string', dest = 'transto') #action = 'store',
		self.OptionParser.add_option('--transformtype', action = 'store', type = 'string', dest = 'transformtype')
		#Motion
		self.OptionParser.add_option('--pathid', action = 'store', type = 'string', dest = 'pathid')
		self.OptionParser.add_option('--Mrotate', type = 'inkbool', dest = 'Mrotate') #action = 'store', 
		#animate
		self.OptionParser.add_option('--attrib', type = 'string', dest = 'attrib') #action = 'store', 
		self.OptionParser.add_option('--attfrom', type = 'string', dest = 'attfrom') #action = 'store', 
		self.OptionParser.add_option('--attto',   type = 'string', dest = 'attto') #action = 'store', 
		
		self.OptionParser.add_option('--actiontype', action = 'store', type = 'string', dest = 'actiontype', default='')

		inkex.NSS["jessyink"] = "https://launchpad.net/jessyink"
		inkex.NSS["xlink"] = "http://www.w3.org/1999/xlink"

	def effect(self):
		# Check version.
		#scriptNodes = self.document.xpath("//svg:script[@jessyink:version='1.5.6']", namespaces=inkex.NSS)
		#if len(scriptNodes) != 1:
		#	inkex.errormsg(_(u"JessyInk_c 还未安装到这个SVG文件，或者版本不同. 请使用 “扩展” 菜单下 “JessyInk_c” 的 “安装/升级...” 命令进行JessyInk_c 的安装。\n\n"))

		if len(self.selected) == 0:
			inkex.errormsg(_(u"进行设置前，请先选择一个对象。\n"))
		p_id = self.options.pathid
		p_id_flag = False
		dur = self.options.smilDuration #+ "s"
		bgin= self.options.smilbegin #+ "s"
		bend= self.options.smilend #+ "s"
		#print len(self.selected)
		#if (len(self.selected) > 1) and  (self.options.smiltype == "animateMotion"):
		#	for id, node in list(self.selected.items()):
		#		#print id, "  ", node
		#		inkex.errormsg(_("" + str(id) + "," + str(node)))
		#		if node.tag == inkex.addNS("path", "svg"):
		#			p_id = id
		#			p_id_flag = True
		#			break


		for id, node in list(self.selected.items()):
			# Globel switch
			if self.options.Gswitch:
				# Remove possible action.
				if "onmouseout" in node.attrib:
					del node.attrib["onmouseout"]
				if "onmouseover" in node.attrib:
					del node.attrib["onmouseover"]
				node.set("onmouseout","this.ownerSVGElement.pauseAnimations()")
				node.set("onmouseover","this.ownerSVGElement.unpauseAnimations()")
			
			if (self.options.smiltype == "animateMotion"):
				if len(p_id) < 1:
					inkex.errormsg(_(u"需要填写运动轨迹路径的ID。\n"))
					break
				# Create new animateMotion node.
				animateElm = inkex.etree.Element(inkex.addNS("animateMotion", "svg"))
				animateElm.set("dur", dur)
				animateElm.set("begin", bgin)
				if (bend == '0' or bend == '0s'):
					pass
				else:
					animateElm.set("end", bend)
				animateElm.set("repeatCount", self.options.smilrepeatCount)
				if self.options.Mrotate:
					animateElm.set("rotate", "auto")
				#else:
				#	animateElm.set("rotate", "0")
				animateElm.set("fill", "freeze")
				pathElm = inkex.etree.Element(inkex.addNS("mpath", "animateMotion"))
				pathElm.set("{" + inkex.NSS["xlink"] + "}href", "#" + p_id)
				animateElm.append(pathElm)
				#animateElm.set("accumulate", "sum")
				animateElm.set("additive", "sum")
				# Remove old animateMotion.
				#for nmm in node.getchildren():
				#	if nmm.tag == inkex.addNS('animateMotion','svg'):
				#		node.remove(nmm)
				node.append(animateElm)
			
			if (self.options.smiltype == "animateTransform"):
				# Create new animateTransform node.
				animateElm = inkex.etree.Element(inkex.addNS("animateTransform", "svg"))
				animateElm.set("attributeName", "transform")
				animateElm.set("dur", dur)
				animateElm.set("begin", bgin)
				if (bend == '0' or bend == '0s'):
					pass
				else:
					animateElm.set("end", bend)
				animateElm.set("repeatCount", self.options.smilrepeatCount)
				animateElm.set("fill", "freeze")
				
				if (self.options.transformtype == "rotate"):
					#x = float(node.attrib["x"])
					#y = float(node.attrib["y"])
					#w = float(node.attrib["width"])
					#h = float(node.attrib["height"])
					#cx = x + w/2
					#cy = y + h/2
					animateElm.set("type", "rotate")
					#animateElm.set("note", "translate-tx-ty8scale-sx-sy8rotate-angle-cx-cy8skewX8skewY-angle")
					#animateElm.set("values", "0 %.5f %.5f; 360 %.5f %.5f" % (cx, cy, cx, cy))
					animateElm.set("values", "%s; %s" % (self.options.transfrom, self.options.transto))
				if (self.options.transformtype == "translate"):
					animateElm.set("type", "translate")
					animateElm.set("values", "%s; %s" % (self.options.transfrom, self.options.transto))
					#animateElm.set("from", self.options.transfrom)
					#animateElm.set("to", self.options.transto)
				if (self.options.transformtype == "scale"):
					animateElm.set("type", "scale")
					animateElm.set("from", self.options.transfrom)
					animateElm.set("to", self.options.transto)
				if (self.options.transformtype == "skewX"):
					x = float(node.attrib["x"])
					y = float(node.attrib["y"])
					animateElm.set("origin", "%.5f %.5f" % (x, y))
					animateElm.set("type", "skewX")
					animateElm.set("from", self.options.transfrom)
					animateElm.set("to", self.options.transto)
				if (self.options.transformtype == "skewY"):
					animateElm.set("type", "skewY")
					animateElm.set("from", self.options.transfrom)
					animateElm.set("to", self.options.transto)
				#animateElm.set("accumulate", "sum")
				animateElm.set("additive", "sum")
				# Remove old animateTransform.
				#for nmm in node.getchildren():
				#	if nmm.tag == inkex.addNS('animateTransform','svg'):
				#		node.remove(nmm)
				node.append(animateElm)
				
				
			if (self.options.smiltype == "animate"):
				# Create new animateTransform node.
				animateElm = inkex.etree.Element(inkex.addNS("animate", "svg"))
				animateElm.set("fill", "freeze")
				animateElm.set("dur", dur)
				animateElm.set("begin", bgin)
				if (bend == '0' or bend == '0s'):
					pass
				else:
					animateElm.set("end", bend)
				animateElm.set("repeatCount", self.options.smilrepeatCount)
				#animateElm.set("attributeType", "XML")
				animateElm.set("attributeName", self.options.attrib)
				animateElm.set("from", self.options.attfrom)
				animateElm.set("to", self.options.attto)
				#animateElm.set("by", self.options.distance)
				#animateElm.set("accumulate", "sum")
				animateElm.set("additive", "sum")
				node.append(animateElm)
				
				
			#  OLD ==============
			if (self.options.actiontype == "rotate"):
				# Create new animateTransform node.
				animateElm = inkex.etree.Element(inkex.addNS("animateTransform", "svg"))
				#animateElm.text = "t"
				x = float(node.attrib["x"])
				y = float(node.attrib["y"])
				w = float(node.attrib["width"])
				h = float(node.attrib["height"])
				cx = x + w/2
				cy = y + h/2
				animateElm.set("attributeName", "transform")
				animateElm.set("attributeType", "XML")
				animateElm.set("type", "rotate")
				animateElm.set("note", "translate-tx-ty8scale-sx-sy8rotate-angle-cx-cy8skewX8skewY-angle")
				animateElm.set("values", "0 %.5f %.5f; 360 %.5f %.5f" % (cx, cy, cx, cy))
				animateElm.set("begin", "mousedown")
				#animateElm.set("end", "mouseout")
				animateElm.set("begin_b", "0s")
				animateElm.set("dur", dur)
				animateElm.set("repeatCount", "indefinite")
				#animateElm.set("accumulate", "sum")
				animateElm.set("additive", "sum")
				# Remove old animateTransform.
				#for nmm in node.getchildren():
				#	if nmm.tag == inkex.addNS('animateTransform','svg'):
				#		node.remove(nmm)
				node.append(animateElm)

			if (self.options.actiontype == "move"):
				# Create new animateTransform node.
				animateElm = inkex.etree.Element(inkex.addNS("animate", "svg"))
				animateElm.set("attributeName", "x")
				#animateElm.set("from", "0")
				#animateElm.set("to", "95")
				animateElm.set("by", self.options.distance)
				animateElm.set("fill", "freeze")
				animateElm.set("attributeType", "XML")
				animateElm.set("begin", "mousedown")
				#animateElm.set("end", "mouseout")
				animateElm.set("begin_b", "0s")
				animateElm.set("dur", dur)
				animateElm.set("repeatCount", "indefinite")
				node.append(animateElm)
				# Create new animateTransform node.
				animateElm = inkex.etree.Element(inkex.addNS("animate", "svg"))
				animateElm.set("attributeName", "y")
				#animateElm.set("from", "0")
				#animateElm.set("to", "95")
				animateElm.set("by", self.options.distance)
				animateElm.set("fill", "freeze")
				animateElm.set("attributeType", "XML")
				animateElm.set("begin", "mousedown")
				#animateElm.set("end", "mouseout")
				animateElm.set("begin_b", "0s")
				animateElm.set("dur", dur)
				animateElm.set("repeatCount", "indefinite")
				#animateElm.set("accumulate", "sum")
				animateElm.set("additive", "sum")
				node.append(animateElm)
			#	node.set("onclick","jumpto(" + self.options.jumpslide + "," + self.options.jumpeffect + ")")

				#if node.tag == inkex.addNS("path", "svg") and p_id_flag == True:
					#p_id_flag = False
					#continue
			if (self.options.actiontype == "path"):
				if len(p_id) < 1:
					inkex.errormsg(_(u"需要填写运动轨迹路径的ID。\n"))
					break
				# Create new animateMotion node.
				animateElm = inkex.etree.Element(inkex.addNS("animateMotion", "svg"))
				animateElm.set("dur", "0s")
				animateElm.set("begin", "0s")
				animateElm.set("rotate", "auto")
				animateElm.set("fill", "remove")
				pathElm = inkex.etree.Element(inkex.addNS("mpath", "animateMotion"))
				pathElm.set("{" + inkex.NSS["xlink"] + "}href", "#" + p_id)
				animateElm.append(pathElm)
				node.append(animateElm)

				animateElm = inkex.etree.Element(inkex.addNS("animateMotion", "svg"))
				animateElm.set("dur", dur)
				animateElm.set("repeatCount", "indefinite")
				animateElm.set("rotate", "auto")
				animateElm.set("begin", "mousedown")
				animateElm.set("fill", "freeze")
				#animateElm.set("accumulate", "sum")
				#animateElm.set("additive", "sum")
				#animateElm.set("end", "mouseout")
				pathElm = inkex.etree.Element(inkex.addNS("mpath", "animateMotion"))
				pathElm.set("{" + inkex.NSS["xlink"] + "}href", "#" + p_id)
				animateElm.append(pathElm)
				node.append(animateElm)
				#http://edutechwiki.unige.ch/en/SVG-SMIL_animation_tutorial

# Create effect instance
effect = JessyInk_Effects()
effect.affect()
