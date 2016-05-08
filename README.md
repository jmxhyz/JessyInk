# JessyInk
使用Inkscape的插件JessyInk制作SVG格式网页版动画演示。添加了播放面板。可以基于nodejs或者python3进行远程控制。

# 安装
1. 安装Inkscape软件。
2. 将Inkscape自带的jessyInk插件升级为本版jessyink。将本inkscape-extensions内文件复制到Inkscape的插件目录。  
   默认的jessyInk安装目录：  
   Unix： '/usr/share/inkscape/extensions' 或者 '~/.config/inkscape/extensions'  
   OS X： '/Applications/Inkscape.app/Contents/Resources/extensions'  
   Windows： 'C:\Program Files\Inkscape\share\extensions'
3. 安装nodejs或者python3
4. 使用nodejs启动nodejessy下的server.js，或者python3启动pythonjessy下的server.py

# 动画演示制作
1. 使用Inkscape制作SVG动画，使用扩展JessyInk制作演示。
2. 制作完成的SVG演示保存在nodejessy下的public目录内，或者放在pythonjessy下的static目录内。
3. SVG演示文件与一个index.hrml文件相配套。每个index.html文件可以加载3个SVG演示文件。
4. 文件命名规则：例如标题为“演示”，那么可以包括四个文件：  
   演示index.html、演示1.svg、演示2.svg、演示3.svg
5. 其它SVG演示文件，按照上面的命名规则进行配置，复制“演示index.html”并改名。
6. 在浏览器（建议firefox）打开index.html文件，点左上角小三角形，可弹出控制面板（须浏览器允许弹出窗口）。  
   如果是通过启动nodejs或python服务器形式启动，则可以点左上角小方形，弹出二维码，可扫描打开控制面板。
