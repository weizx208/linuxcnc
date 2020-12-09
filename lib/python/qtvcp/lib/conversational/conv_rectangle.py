'''
conv_rectangle.py

Copyright (C) 2020  Phillip A Carter

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''

import math
from PyQt5.QtCore import Qt 
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QRadioButton, QButtonGroup 
from PyQt5.QtGui import QPixmap 

def preview(P, W):
    xLB = yLR = xLT = yLL = 0
    if W.xlEntry.text() and W.ylEntry.text():
        try:
            if float(W.xlEntry.text()) <= 0 or float(W.ylEntry.text()) <= 0:
                msg  = 'A positive X Length is required\n\n'
                msg += 'and\n\n'
                msg += 'A positive Y Length is required\n'
                P.dialog_error('RECTANGLE', msg)
                return
        except:
            msg = 'Invalid X Length or Y Length\n'
            P.dialog_error('RECTANGLE', msg)
            return
        if W.r1Entry.text():
            radius1 = float(W.r1Entry.text())
        else:
            radius1 = 0.0
        if W.r2Entry.text():
            radius2 = float(W.r2Entry.text())
        else:
            radius2 = 0.0
        if W.r3Entry.text():
            radius3 = float(W.r3Entry.text())
        else:
            radius3 = 0.0
        if W.r4Entry.text():
            radius4 = float(W.r4Entry.text())
        else:
            radius4 = 0.0
        if radius1 + radius2 > float(W.xlEntry.text()):
            msg  = 'Radius 1 plus Radius 2 ({})\n\n'.format(radius1 + radius2)
            msg += 'can not be greater than {}\n'.format(float(W.xlEntry.text()))
            P.dialog_error('RECTANGLE', msg)
            return
        if radius1 + radius3 > float(W.ylEntry.text()):
            msg  = 'Radius 1 plus Radius 3 ({})\n\n'.format(radius1 + radius3)
            msg += 'can not be greater than {}\n'.format(float(W.ylEntry.text()))
            P.dialog_error('RECTANGLE', msg)
            return
        if radius2 + radius4 > float(W.ylEntry.text()):
            msg  = 'Radius 2 plus Radius 4 ({})\n\n'.format(radius2 + radius4)
            msg += 'can not be greater than {}\n'.format(float(W.ylEntry.text()))
            P.dialog_error('RECTANGLE', msg)
            return
        if radius3 > float(W.xlEntry.text()) / 2 or radius4 > float(W.xlEntry.text()) / 2:
            msg  = 'Neither Radius 3 nor Radius 4\n\n'
            msg += 'can be greater than {}\n'.format(float(W.xlEntry.text()) / 2)
            P.dialog_error('RECTANGLE', msg)
            return
        if W.xlEntry.text():
            xLB = float(W.xlEntry.text()) - (radius3 + radius4)
            xLT = float(W.xlEntry.text()) - (radius1 + radius2)
            xC = float(W.xlEntry.text()) / 2
        if W.ylEntry.text():
            yLR = float(W.ylEntry.text()) - (radius2 + radius4)
            yLL = float(W.ylEntry.text()) - (radius1 + radius3)
            yC = float(W.ylEntry.text()) / 2
        if xLB >= 0 and yLR >= 0 and xLT >= 0 and yLL >= 0:
            blLength = math.sqrt(xC ** 2 + (yC * 2) ** 2)
            blAngle = math.atan((yC * 2) / xC)
            if W.angEntry.text():
                angle = math.radians(float(W.angEntry.text()))
            else:
                angle = 0.0
            if W.liEntry.text():
                leadInOffset = math.sin(math.radians(45)) * float(W.liEntry.text())
            else:
                leadInOffset = 0
            if W.loEntry.text():
                leadOutOffset = math.sin(math.radians(45)) * float(W.loEntry.text())
            else:
                leadOutOffset = 0
            right = math.radians(0)
            up = math.radians(90)
            left = math.radians(180)
            down = math.radians(270)
#            kOffset = hal.get_value('plasmac_run.kerf-width-f') * W.kOffset.isChecked() / 2
            kOffset = float(W.kerf_width.text()) * W.kOffset.isChecked() / 2
            if not W.xsEntry.text():
                W.xsEntry.setText('{:0.3f}'.format(P.xOrigin))
            if W.center.isChecked():
                if W.cExt.isChecked():
                    xS = float(W.xsEntry.text()) + ((yC - radius2) * math.cos(angle + up)) + (xC * math.cos(angle + right))
                else:
                    xS = float(W.xsEntry.text()) + yC * math.cos(angle + up)
            else:
                if W.cExt.isChecked():
                    xS = (float(W.xsEntry.text()) + kOffset) + (float(W.xlEntry.text()) * math.cos(angle + up)) + (float(W.xlEntry.text()) * math.cos(angle + right))
                else:
                    xS = (float(W.xsEntry.text()) - kOffset) + (blLength * math.cos(angle + right + blAngle))

            if not W.ysEntry.text():
                W.ysEntry.setText('{:0.3f}'.format(P.yOrigin))
            if W.center.isChecked():
                if W.cExt.isChecked():
                    yS = float(W.ysEntry.text()) + (yC - radius2 * math.sin(angle + up)) + (xC * math.sin(angle + right))
                else:
                    yS = float(W.ysEntry.text()) + yC * math.sin(angle + up)
            else:
                if W.cExt.isChecked():
                    yS = (float(W.ysEntry.text()) + kOffset) + ((float(W.ylEntry.text()) - radius2) * math.sin(angle + up)) + (float(W.xlEntry.text()) * math.sin(angle + right))
                else:
                    yS = (float(W.ysEntry.text()) - kOffset) + (blLength * math.sin(angle + right + blAngle))
            outTmp = open(P.fTmp, 'w')
            outNgc = open(P.fNgc, 'w')
            inWiz = open(P.fNgcBkp, 'r')
            for line in inWiz:
                if '(new conversational file)' in line:
                    outNgc.write('\n{} (preamble)\n'.format(P.preAmble))
                    outNgc.write('f#<_hal[plasmac.cut-feed-rate]>\n')
                    break
                elif '(postamble)' in line:
                    break
                elif 'm2' in line.lower() or 'm30' in line.lower():
                    break
                outNgc.write(line)
            outTmp.write('\n(wizard rectangle)\n')
            if W.cExt.isChecked():
                if leadInOffset > 0:
                    xlCentre = xS + (leadInOffset * math.cos(angle + right))
                    ylCentre = yS + (leadInOffset * math.sin(angle + right))
                    xlStart = xlCentre + (leadInOffset * math.cos(angle + up))
                    ylStart = ylCentre + (leadInOffset * math.sin(angle + up))
                    outTmp.write('g0 x{:.6f} y{:.6f}\n'.format(xlStart, ylStart))
                    if W.kOffset.isChecked():
                        outTmp.write('g41.1 d#<_hal[qtplasmac.kerf_width-f]>\n')
                    outTmp.write('m3 $0 s1\n')
                    outTmp.write('g3 x{:.6f} y{:.6f} i{:.6f} j{:.6f}\n'.format(xS, yS , xlCentre - xlStart, ylCentre - ylStart))
                else:
                    outTmp.write('g0 x{:.6f} y{:.6f}\n'.format(xS, yS))
                    outTmp.write('m3 $0 s1\n')
                x1 = xS + yLR * math.cos(angle + down)
                y1 = yS + yLR * math.sin(angle + down)
                outTmp.write('g1 x{:.6f} y{:.6f}\n'.format(x1, y1))
                if radius4 > 0:
                    if W.r4Button.text().startswith('iRadius'):
                        xrCentre = x1 + (radius4 * math.cos(angle + down))
                        yrCentre = y1 + (radius4 * math.sin(angle + down))
                        xrEnd = xrCentre + (radius4 * math.cos(angle + left))
                        yrEnd = yrCentre + (radius4 * math.sin(angle + left))
                        outTmp.write('g3 x{:.6f} y{:.6f} i{:.6f} j{:.6f}\n'.format(xrEnd, yrEnd, xrCentre - x1, yrCentre - y1))
                    else:
                        xrCentre = x1 + (radius4 * math.cos(angle + left))
                        yrCentre = y1 + (radius4 * math.sin(angle + left))
                        xrEnd = xrCentre + (radius4 * math.cos(angle + down))
                        yrEnd = yrCentre + (radius4 * math.sin(angle + down))
                    if W.r4Button.text().startswith('Radius'):
                        outTmp.write('g2 x{:.6f} y{:.6f} i{:.6f} j{:.6f}\n'.format(xrEnd, yrEnd, xrCentre - x1, yrCentre - y1))
                    else:
                        outTmp.write('g1 x{:.6f} y{:.6f}\n'.format(xrEnd, yrEnd))
                    x2 = xrEnd + xLB * math.cos(angle + left)
                    y2 = yrEnd + xLB * math.sin(angle + left)
                else:
                    x2 = x1 + xLB * math.cos(angle + left)
                    y2 = y1 + xLB * math.sin(angle + left)
                outTmp.write('g1 x{:.6f} y{:.6f}\n'.format(x2, y2))
                if radius3 > 0:
                    if W.r3Button.text().startswith('iRadius'):
                        xrCentre = x2 + (radius3 * math.cos(angle + left))
                        yrCentre = y2 + (radius3 * math.sin(angle + left))
                        xrEnd = xrCentre + (radius3 * math.cos(angle + up))
                        yrEnd = yrCentre + (radius3 * math.sin(angle + up))
                        outTmp.write('g3 x{:.6f} y{:.6f} i{:.6f} j{:.6f}\n'.format(xrEnd, yrEnd, xrCentre - x2, yrCentre - y2))
                    else:
                        xrCentre = x2 + (radius3 * math.cos(angle + up))
                        yrCentre = y2 + (radius3 * math.sin(angle + up))
                        xrEnd = xrCentre + (radius3 * math.cos(angle + left))
                        yrEnd = yrCentre + (radius3 * math.sin(angle + left))
                    if W.r3Button.text().startswith('Radius'):
                        outTmp.write('g2 x{:.6f} y{:.6f} i{:.6f} j{:.6f}\n'.format(xrEnd, yrEnd, xrCentre - x2, yrCentre - y2))
                    else:
                        outTmp.write('g1 x{:.6f} y{:.6f}\n'.format(xrEnd, yrEnd))
                    x3 = xrEnd + yLL * math.cos(angle + up)
                    y3 = yrEnd + yLL * math.sin(angle + up)
                else:
                    x3 = x2 + yLL * math.cos(angle + up)
                    y3 = y2 + yLL * math.sin(angle + up)
                outTmp.write('g1 x{:.6f} y{:.6f}\n'.format(x3, y3))
                if radius1 > 0:
                    if W.r1Button.text().startswith('iRadius'):
                        xrCentre = x3 + (radius1 * math.cos(angle + up))
                        yrCentre = y3 + (radius1 * math.sin(angle + up))
                        xrEnd = xrCentre + (radius1 * math.cos(angle + right))
                        yrEnd = yrCentre + (radius1 * math.sin(angle + right))
                        outTmp.write('g3 x{:.6f} y{:.6f} i{:.6f} j{:.6f}\n'.format(xrEnd, yrEnd, xrCentre - x3, yrCentre - y3))
                    else:
                        xrCentre = x3 + (radius1 * math.cos(angle + right))
                        yrCentre = y3 + (radius1 * math.sin(angle + right))
                        xrEnd = xrCentre + (radius1 * math.cos(angle + up))
                        yrEnd = yrCentre + (radius1 * math.sin(angle + up))
                    if W.r1Button.text().startswith('Radius'):
                        outTmp.write('g2 x{:.6f} y{:.6f} i{:.6f} j{:.6f}\n'.format(xrEnd, yrEnd, xrCentre - x3, yrCentre - y3))
                    else:
                        outTmp.write('g1 x{:.6f} y{:.6f}\n'.format(xrEnd, yrEnd))
                    x4 = xrEnd + xLT * math.cos(angle + right)
                    y4 = yrEnd + xLT * math.sin(angle + right)
                else:
                    x4 = x3 + xLT * math.cos(angle + right)
                    y4 = y3 + xLT * math.sin(angle + right)
                outTmp.write('g1 x{:.6f} y{:.6f}\n'.format(x4, y4))
                if radius2 > 0:
                    if W.r2Button.text().startswith('iRadius'):
                        xrCentre = x4 + (radius2 * math.cos(angle + right))
                        yrCentre = y4 + (radius2 * math.sin(angle + right))
                        xrEnd = xrCentre + (radius2 * math.cos(angle + down))
                        yrEnd = yrCentre + (radius2 * math.sin(angle + down))
                        outTmp.write('g3 x{:.6f} y{:.6f} i{:.6f} j{:.6f}\n'.format(xrEnd, yrEnd, xrCentre - x4, yrCentre - y4))
                    else:
                        xrCentre = x4 + (radius2 * math.cos(angle + down))
                        yrCentre = y4 + (radius2 * math.sin(angle + down))
                        xrEnd = xrCentre + (radius2 * math.cos(angle + right))
                        yrEnd = yrCentre + (radius2 * math.sin(angle + right))
                    if W.r2Button.text().startswith('Radius'):
                        outTmp.write('g2 x{:.6f} y{:.6f} i{:.6f} j{:.6f}\n'.format(xrEnd, yrEnd, xrCentre - x4, yrCentre - y4))
                    else:
                        outTmp.write('g1 x{:.6f} y{:.6f}\n'.format(xrEnd, yrEnd))
            else:
                if leadInOffset > 0:
                    xlCentre = xS + (leadInOffset * math.cos(angle + down))
                    ylCentre = yS + (leadInOffset * math.sin(angle + down))
                    xlStart = xlCentre + (leadInOffset * math.cos(angle + right))
                    ylStart = ylCentre + (leadInOffset * math.sin(angle + right))
                    outTmp.write('g0 x{:.6f} y{:.6f}\n'.format(xlStart, ylStart))
                    if W.kOffset.isChecked():
                        outTmp.write('g41.1 d#<_hal[qtplasmac.kerf_width-f]>\n')
                    outTmp.write('m3 $0 s1\n')
                    outTmp.write('g3 x{:.6f} y{:.6f} i{:.6f} j{:.6f}\n'.format(xS, yS , xlCentre - xlStart, ylCentre - ylStart))
                else:
                    outTmp.write('g0 x{:.6f} y{:.6f}\n'.format(xS, yS))
                    outTmp.write('m3 $0 s1\n')
                x1 = xS + (xLT / 2) * math.cos(angle + left)
                y1 = yS + (xLT / 2) * math.sin(angle + left)
                outTmp.write('g1 x{:.6f} y{:.6f}\n'.format(x1, y1))
                if radius1 > 0:
                    if W.r1Button.text().startswith('iRadius'):
                        xrCentre = x1 + (radius1 * math.cos(angle + left))
                        yrCentre = y1 + (radius1 * math.sin(angle + left))
                        xrEnd = xrCentre + (radius1 * math.cos(angle + down))
                        yrEnd = yrCentre + (radius1 * math.sin(angle + down))
                        outTmp.write('g2 x{:.6f} y{:.6f} i{:.6f} j{:.6f}\n'.format(xrEnd, yrEnd, xrCentre - x1, yrCentre - y1))
                    else:
                        xrCentre = x1 + (radius1 * math.cos(angle + down))
                        yrCentre = y1 + (radius1 * math.sin(angle + down))
                        xrEnd = xrCentre + (radius1 * math.cos(angle + left))
                        yrEnd = yrCentre + (radius1 * math.sin(angle + left))
                    if W.r1Button.text().startswith('Radius'):
                        outTmp.write('g3 x{:.6f} y{:.6f} i{:.6f} j{:.6f}\n'.format(xrEnd, yrEnd, xrCentre - x1, yrCentre - y1))
                    else:
                        outTmp.write('g1 x{:.6f} y{:.6f}\n'.format(xrEnd, yrEnd))
                    x2 = xrEnd + yLL * math.cos(angle + down)
                    y2 = yrEnd + yLL * math.sin(angle + down)
                else:
                    x2 = x1 + yLL * math.cos(angle + down)
                    y2 = y1 + yLL * math.sin(angle + down)
                outTmp.write('g1 x{:.6f} y{:.6f}\n'.format(x2, y2))
                if radius3 > 0:
                    if W.r3Button.text().startswith('iRadius'):
                        xrCentre = x3 + (radius3 * math.cos(angle + down))
                        yrCentre = y3 + (radius3 * math.sin(angle + down))
                        xrEnd = xrCentre + (radius3 * math.cos(angle + right))
                        yrEnd = yrCentre + (radius3 * math.sin(angle + right))
                        outTmp.write('g2 x{:.6f} y{:.6f} i{:.6f} j{:.6f}\n'.format(xrEnd, yrEnd, xrCentre - x2, yrCentre - y2))
                    else:
                        xrCentre = x2 + (radius3 * math.cos(angle + right))
                        yrCentre = y2 + (radius3 * math.sin(angle + right))
                        xrEnd = xrCentre + (radius3 * math.cos(angle + down))
                        yrEnd = yrCentre + (radius3 * math.sin(angle + down))
                    if W.r3Button.text().startswith('Radius'):
                        outTmp.write('g3 x{:.6f} y{:.6f} i{:.6f} j{:.6f}\n'.format(xrEnd, yrEnd, xrCentre - x2, yrCentre - y2))
                    else:
                        outTmp.write('g1 x{:.6f} y{:.6f}\n'.format(xrEnd, yrEnd))
                    x3 = xrEnd + xLB * math.cos(angle + right)
                    y3 = yrEnd + xLB * math.sin(angle + right)
                else:
                    x3 = x2 + xLB * math.cos(angle + right)
                    y3 = y2 + xLB * math.sin(angle + right)
                outTmp.write('g1 x{:.6f} y{:.6f}\n'.format(x3, y3))
                if radius4 > 0:
                    if W.r4Button.text().startswith('iRadius'):
                        xrCentre = x3 + (radius4 * math.cos(angle + right))
                        yrCentre = y3 + (radius4 * math.sin(angle + right))
                        xrEnd = xrCentre + (radius4 * math.cos(angle + up))
                        yrEnd = yrCentre + (radius4 * math.sin(angle + up))
                        outTmp.write('g2 x{:.6f} y{:.6f} i{:.6f} j{:.6f}\n'.format(xrEnd, yrEnd, xrCentre - x3, yrCentre - y3))
                    else:
                        xrCentre = x3 + (radius4 * math.cos(angle + up))
                        yrCentre = y3 + (radius4 * math.sin(angle + up))
                        xrEnd = xrCentre + (radius4 * math.cos(angle + right))
                        yrEnd = yrCentre + (radius4 * math.sin(angle + right))
                    if W.r4Button.text().startswith('Radius'):
                        outTmp.write('g3 x{:.6f} y{:.6f} i{:.6f} j{:.6f}\n'.format(xrEnd, yrEnd, xrCentre - x3, yrCentre - y3))
                    else:
                        outTmp.write('g1 x{:.6f} y{:.6f}\n'.format(xrEnd, yrEnd))
                    x4 = xrEnd + yLR * math.cos(angle + up)
                    y4 = yrEnd + yLR * math.sin(angle + up)
                else:
                    x4 = x3 + yLR * math.cos(angle + up)
                    y4 = y3 + yLR * math.sin(angle + up)
                outTmp.write('g1 x{:.6f} y{:.6f}\n'.format(x4, y4))
                if radius2 > 0:
                    if W.r2Button.text().startswith('iRadius'):
                        xrCentre = x4 + (radius2 * math.cos(angle + up))
                        yrCentre = y4 + (radius2 * math.sin(angle + up))
                        xrEnd = xrCentre + (radius2 * math.cos(angle + left))
                        yrEnd = yrCentre + (radius2 * math.sin(angle + left))
                        outTmp.write('g2 x{:.6f} y{:.6f} i{:.6f} j{:.6f}\n'.format(xrEnd, yrEnd, xrCentre - x4, yrCentre - y4))
                    else:
                        xrCentre = x4 + (radius2 * math.cos(angle + left))
                        yrCentre = y4 + (radius2 * math.sin(angle + left))
                        xrEnd = xrCentre + (radius2 * math.cos(angle + up))
                        yrEnd = yrCentre + (radius2 * math.sin(angle + up))
                    if W.r2Button.text().startswith('Radius'):
                        outTmp.write('g3 x{:.6f} y{:.6f} i{:.6f} j{:.6f}\n'.format(xrEnd, yrEnd, xrCentre - x4, yrCentre - y4))
                    else:
                        outTmp.write('g1 x{:.6f} y{:.6f}\n'.format(xrEnd, yrEnd))
            outTmp.write('g1 x{:.6f} y{:.6f}\n'.format(xS, yS))
            if leadOutOffset > 0: # and not (W.cExt.isChecked() and radius2):
                if W.cExt.isChecked() and not radius2:
                    dir = ['g2', down, right]
                elif W.cExt.isChecked() and radius2:
                    dir = ['g3', right, down]
                else:
                    dir = ['g3', down, left]
                xlCentre = xS + (leadOutOffset * math.cos(angle + dir[1]))
                ylCentre = yS + (leadOutOffset * math.sin(angle + dir[1]))
                xlEnd = xlCentre + (leadOutOffset * math.cos(angle + dir[2]))
                ylEnd = ylCentre + (leadOutOffset * math.sin(angle + dir[2]))
                outTmp.write('{} x{:.6f} y{:.6f} i{:.6f} j{:.6f}\n'.format(dir[0], xlEnd, ylEnd , xlCentre - xS, ylCentre - yS))
            outTmp.write('g40\n')
            outTmp.write('m5 $0\n')
            outTmp.close()
            outTmp = open(P.fTmp, 'r')
            for line in outTmp:
                outNgc.write(line)
            outTmp.close()
            outNgc.write('\n{} (postamble)\n'.format(P.postAmble))
            outNgc.write('m2\n')
            outNgc.close()
            W.conv_preview.load(P.fNgc)
            W.conv_preview.set_current_view()
            W.add.setEnabled(True)
    else:
        msg  = 'A positive X Length is required\n\n'
        msg += 'and\n\n'
        msg += 'A positive Y Length is required\n'
        P.dialog_error('RECTANGLE', msg)

def rad_button_pressed(P, W, button, value):
    if button.text()[:3] == 'Rad':
        button.setText('Chamfer {}'.format(value))
    elif button.text()[:3] == 'Cha':
        button.setText('iRadius {}'.format(value))
    else:
        button.setText('Radius {}'.format(value))
    auto_preview(P, W)

def entry_changed(P, W, widget):
    if not W.liEntry.text() or float(W.liEntry.text()) == 0:
        W.kOffset.setChecked(False)
        W.kOffset.setEnabled(False)
    else:
        W.kOffset.setEnabled(True)
    P.conv_entry_changed(widget)

def auto_preview(P, W):
    if W.xlEntry.text() and W.ylEntry.text():
        preview(P, W) 

def add_shape_to_file(P, W):
    P.add_shape_to_file()

def widgets(P, W):
    #widgets
    W.ctLabel = QLabel('Cut Type')
    W.ctGroup = QButtonGroup(W)
    W.cExt = QRadioButton('External')
    W.cExt.setChecked(True)
    W.ctGroup.addButton(W.cExt)
    W.cInt = QRadioButton('Internal')
    W.ctGroup.addButton(W.cInt)
    W.koLabel = QLabel('Offset')
    W.kOffset = QPushButton('Kerf Width')
    W.kOffset.setCheckable(True)
    W.osLabel = QLabel('Offset')
    W.osGroup = QButtonGroup(W)
    W.center = QRadioButton('Center')
    W.osGroup.addButton(W.center)
    W.bLeft = QRadioButton('Btm Left')
    W.osGroup.addButton(W.bLeft)
    W.xsLabel = QLabel('X origin')
    W.xsEntry = QLineEdit(objectName = 'xsEntry')
    W.ysLabel = QLabel('Y origin')
    W.ysEntry = QLineEdit(objectName = 'ysEntry')
    W.liLabel = QLabel('Lead In')
    W.liEntry = QLineEdit(objectName = 'liEntry')
    W.loLabel = QLabel('Lead Out')
    W.loEntry = QLineEdit(objectName = 'loEntry')
    W.xlLabel = QLabel('X length')
    W.xlEntry = QLineEdit()
    W.ylLabel = QLabel('Y length')
    W.ylEntry = QLineEdit()
    W.angLabel = QLabel('Angle')
    W.angEntry = QLineEdit()
    W.angEntry.setText('0')
    W.r1Button = QPushButton('Radius 1')
    W.r1Entry = QLineEdit()
    W.r2Button = QPushButton('Radius 2')
    W.r2Entry = QLineEdit()
    W.r3Button = QPushButton('Radius 3')
    W.r3Entry = QLineEdit()
    W.r4Button = QPushButton('Radius 4')
    W.r4Entry = QLineEdit()
    W.preview = QPushButton('Preview')
    W.add = QPushButton('Add')
    W.add.setEnabled(False)
    W.undo = QPushButton('Undo')
    W.lDesc = QLabel('Creating Rectangle')
    W.iLabel = QLabel()
    pixmap = QPixmap('{}conv_rectangle_l.png'.format(P.IMAGES)).scaledToWidth(240)
    W.iLabel.setPixmap(pixmap)
    #alignment and size
    rightAlign = ['ctLabel', 'koLabel', 'osLabel', 'xsLabel', 'xsEntry', 'ysLabel', \
                  'ysEntry', 'liLabel', 'liEntry', 'loLabel', 'loEntry', 'xlLabel', \
                  'xlEntry', 'ylLabel', 'ylEntry', 'angLabel', 'angEntry', 'r1Entry', \
                  'r2Entry', 'r3Entry', 'r4Entry']
    centerAlign = ['lDesc']
    rButton = ['cExt', 'cInt', 'center', 'bLeft']
    pButton = ['preview', 'add', 'undo', 'kOffset', \
               'r1Button', 'r2Button', 'r3Button', 'r4Button']
    for w in rightAlign:
        W[w].setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        W[w].setFixedWidth(80)
        W[w].setFixedHeight(24)
    for w in centerAlign:
        W[w].setAlignment(Qt.AlignCenter | Qt.AlignBottom)
        W[w].setFixedWidth(240)
        W[w].setFixedHeight(24)
    for w in rButton:
        W[w].setFixedWidth(80)
        W[w].setFixedHeight(24)
    for w in pButton:
        W[w].setFixedWidth(80)
        W[w].setFixedHeight(24)
    #starting parameters
    if P.oSaved:
        W.center.setChecked(True)
    else:
        W.bLeft.setChecked(True)
    W.liEntry.setText('{}'.format(P.leadIn))
    W.loEntry.setText('{}'.format(P.leadOut))
    W.xsEntry.setText('{}'.format(P.xSaved))
    W.ysEntry.setText('{}'.format(P.ySaved))
    W.angEntry.setText('0.0')
    if not W.liEntry.text() or float(W.liEntry.text()) == 0:
        W.kOffset.setChecked(False)
        W.kOffset.setEnabled(False)
    P.conv_undo_shape(None)
    #connections
    W.cExt.toggled.connect(lambda:auto_preview(P, W))
    W.kOffset.toggled.connect(lambda:auto_preview(P, W))
    W.center.toggled.connect(lambda:auto_preview(P, W))
    W.preview.pressed.connect(lambda:preview(P, W))
    W.add.pressed.connect(lambda:add_shape_to_file(P, W))
    W.undo.pressed.connect(lambda:P.conv_undo_shape('add'))
    entries = ['xsEntry', 'ysEntry', 'liEntry', 'loEntry', 'xlEntry', 'ylEntry', \
               'angEntry', 'r1Entry', 'r2Entry', 'r3Entry', 'r4Entry', ]
    for entry in entries:
        W[entry].textChanged.connect(lambda:entry_changed(P, W, W.sender()))
        W[entry].editingFinished.connect(lambda:auto_preview(P, W))
    W.r1Button.pressed.connect(lambda:rad_button_pressed(P, W, W.sender(), '1'))
    W.r2Button.pressed.connect(lambda:rad_button_pressed(P, W, W.sender(), '2'))
    W.r3Button.pressed.connect(lambda:rad_button_pressed(P, W, W.sender(), '3'))
    W.r4Button.pressed.connect(lambda:rad_button_pressed(P, W, W.sender(), '4'))
    #add to layout
    W.entries.addWidget(W.ctLabel, 0, 0)
    W.entries.addWidget(W.cExt, 0, 1)
    W.entries.addWidget(W.cInt, 0, 2)
    W.entries.addWidget(W.koLabel, 0, 3)
    W.entries.addWidget(W.kOffset, 0, 4)
    W.entries.addWidget(W.osLabel, 1, 0)
    W.entries.addWidget(W.center, 1, 1)
    W.entries.addWidget(W.bLeft, 1, 2)
    W.entries.addWidget(W.xsLabel, 2, 0)
    W.entries.addWidget(W.xsEntry, 2, 1)
    W.entries.addWidget(W.ysLabel, 3, 0)
    W.entries.addWidget(W.ysEntry, 3, 1)
    W.entries.addWidget(W.liLabel, 4 , 0)
    W.entries.addWidget(W.liEntry, 4, 1)
    W.entries.addWidget(W.loLabel, 5, 0)
    W.entries.addWidget(W.loEntry, 5, 1)
    W.entries.addWidget(W.xlLabel, 6, 0)
    W.entries.addWidget(W.xlEntry, 6, 1)
    W.entries.addWidget(W.ylLabel, 7, 0)
    W.entries.addWidget(W.ylEntry, 7, 1)
    W.entries.addWidget(W.angLabel, 8, 0)
    W.entries.addWidget(W.angEntry, 8, 1)
    W.entries.addWidget(W.r1Button, 9, 0)
    W.entries.addWidget(W.r1Entry, 9, 1)
    W.entries.addWidget(W.r2Button, 9, 2)
    W.entries.addWidget(W.r2Entry, 9, 3)
    W.entries.addWidget(W.r3Button, 10, 0)
    W.entries.addWidget(W.r3Entry, 10, 1)
    W.entries.addWidget(W.r4Button, 10, 2)
    W.entries.addWidget(W.r4Entry, 10, 3)
    for blank in range(1):
        W['{}'.format(blank)] = QLabel('')
        W['{}'.format(blank)].setFixedHeight(24)
        W.entries.addWidget(W['{}'.format(blank)], 11 + blank, 0)
    W.entries.addWidget(W.preview, 12, 0)
    W.entries.addWidget(W.add, 12, 2)
    W.entries.addWidget(W.undo, 12, 4)
    W.entries.addWidget(W.lDesc, 13 , 1, 1, 3)
    W.entries.addWidget(W.iLabel, 2 , 2, 7, 3)
