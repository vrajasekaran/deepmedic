# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'model_config_create.ui',
# licensing of 'model_config_create.ui' applies.
#
# Created: Mon Sep  2 14:10:18 2019
#      by: pyside2-uic  running on PySide2 5.13.0
#
# WARNING! All changes made in this file will be lost!

import os
from PySide2 import QtCore, QtWidgets, QtGui

LABEL_COL = 0
INPUT_COL = 2
INFO_COL = INPUT_COL - 1
SEARCH_COL = INPUT_COL + 1
LINE_WIDTH = SEARCH_COL - LABEL_COL + 1
SAVE_BUTTON_SIZE = 3
NORMAL_SPAN = 2
SEARCH_SPAN = 1


class UiConfig(object):

    def add_widget(self, widget, row, col, row_span=1, col_span=1):
        self.gridLayout.addWidget(widget, row, col, row_span, col_span)

    def add_title(self, name, text, widget_num):
        self.add_widget(self.create_label(name, text, title=True), widget_num, LABEL_COL, col_span=2)
        self.add_widget(self.create_line(name), widget_num + 1, LABEL_COL, col_span=LINE_WIDTH)
        return widget_num + 2

    def create_info_button(self, name, info=None, default=None):
        info_button = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(os.path.join("deepmedic", "gui", "icons", "info.svg")),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        info_button.setPixmap(icon.pixmap(QtCore.QSize(12, 12)))
        info_button.setObjectName(name + '_info')
        tooltip_text = '<html><head/><body><p>'
        if info:
            tooltip_text += info
        if default is not None:
            if info:
                tooltip_text += '\n'
            tooltip_text += '(default: ' + str(default) + ')'
        tooltip_text += '</p></body></html>'
        info_button.setToolTip(tooltip_text.replace('\n', '</p><p>'))
        info_button.setEnabled(False)  # make icon more gray
        return info_button

    def create_line(self, name):
        line = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        line.setObjectName(name + '_line')
        return line

    def create_label(self, name, text=None, title=False):
        if not text:
            text = name

        widget = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        if title:
            widget.setStyleSheet("font: 12pt \"Ubuntu\";")
            widget.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
            text = '<b>' + text + '</b>'
        widget.setObjectName(name + '_label')

        widget.setText(text)
        return widget

    def create_lineedit(self, name):
        widget = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        widget.setObjectName(name + '_lineedit')
        return widget

    def create_checkbox(self, name, check=False):
        widget = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        widget.setText("")
        widget.setObjectName(name + '_checkbox')
        if check:
            widget.setChecked(True)
        return widget

    def create_combobox(self, name, options):
        widget = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        widget.setObjectName(name + '_combobox')
        widget.addItem("")
        if options:
            for option in options:
                widget.addItem(str(option))
        return widget

    def create_button(self, name, text):
        widget = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        widget.setObjectName(name + '_button')
        widget.setText(text)
        return widget

    def create_widget(self, name, widget_type, options=None, default=None):
        widget = None
        if widget_type == 'lineedit':
            widget = self.create_lineedit(name)
        elif widget_type == 'checkbox':
            widget = self.create_checkbox(name, check=default)
        elif widget_type == 'combobox':
            widget = self.create_combobox(name, options)
        elif widget_type == 'button':
            widget = self.create_button(name, options)
        return widget

    def add_conv_w(self, name, widget_num, options, info=None, default=None):
        self.add_input_field(name, 'combobox', widget_num, INPUT_COL,
                             info=info, default=default, options=options.keys(), col_span=NORMAL_SPAN)
        elem_num = 1
        sub_char = '├'
        for elem in options.values():
            widget_num += 1
            if elem_num == len(options):
                sub_char = '└'
            self.add_grid_row(name + '_' + elem.name, widget_num, elem,
                              text=sub_char + '── ' + elem.description)
            elem_num += 1

        return widget_num

    def add_input_field(self, name, widget_type, row, col=INPUT_COL,
                        info=None, default=None, options=None, info_col=INFO_COL, col_span=NORMAL_SPAN):
        self.add_widget(self.create_widget(name, widget_type, options=options, default=default),
                        row, col, col_span=col_span)
        if info or default:
            self.gridLayout.addWidget(self.create_info_button(name, info, default), row, info_col)

    def add_dictionary(self, name, text, widget_num, elem_dict, info=None, prefix=''):
        self.add_widget(self.create_label(name, text), widget_num, LABEL_COL)
        if info:
            self.gridLayout.addWidget(self.create_info_button(name, info), widget_num, INFO_COL)
        widget_num += 1
        elem_num = 1
        sub_char = '├'
        prefix_char = '│'
        for elem_name, elem in elem_dict.items():
            if elem_num == len(elem_dict):
                sub_char = '└'
                prefix_char = '  '
            widget_num = self.add_grid_row(name + '_' + elem_name, widget_num, elem,
                                           text=prefix + sub_char + '── ' + elem.description,
                                           prefix=prefix + prefix_char + ' '*6)
            elem_num += 1

        return widget_num

    def add_search_button(self, name, widget_num):
        self.add_widget(self.create_button(name, 'Search'), widget_num, SEARCH_COL)

    def add_grid_row(self, name, widget_num, elem, widget_type=None, text=None, options=None, info=None, default=None,
                     prefix=''):

        if widget_type is None:
            widget_type = elem.widget_type
        if text is None:
            text = elem.description
        if options is None:
            options = elem.options
        if info is None:
            info = elem.info
        if default is None:
            default = elem.default

        col_span = NORMAL_SPAN

        if widget_type == 'multiple':
            widget_num = self.add_dictionary(name, text, widget_num, options, info, prefix=prefix)
        else:
            self.add_widget(self.create_label(name, text), widget_num, LABEL_COL)

            if elem.elem_type in ['File', 'Folder', 'Files']:
                self.add_search_button(name, widget_num)
                col_span = SEARCH_SPAN

            if widget_type == 'conv_w':
                widget_num = self.add_conv_w(name, widget_num, options, info=info, default=default)
            else:
                self.add_input_field(name, widget_type, widget_num, INPUT_COL,
                                     info=info, default=default, options=options, col_span=col_span)

        return widget_num + 1

    def setup_ui(self, model_config_create, Config, window_type=''):
        model_config_create.setObjectName("model_config_create")
        model_config_create.resize(600, 440)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(model_config_create.sizePolicy().hasHeightForWidth())
        model_config_create.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(model_config_create)
        self.centralwidget.setObjectName("centralwidget")
        self.centralLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.centralLayout.setSpacing(0)
        self.centralLayout.setContentsMargins(0, 0, 0, 0)
        self.centralLayout.setObjectName("centralLayout")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, -785, 584, 1179))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")

        widget_num = 0
        for section in Config.config_data.get_sorted_sections():
            if not section.advanced:
                widget_num = self.add_title(section.name, section.text, widget_num)
                for elem in section.get_sorted_elems():
                    if not elem.advanced:
                        # print('\t ' + elem.name)
                        widget_num = self.add_grid_row(section.name + '_' + elem.name, widget_num, elem)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, widget_num, 0, 1, 3)
        self.save_button = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.save_button.setObjectName("save_button")
        self.save_button.setText('Save Configuration File')
        self.gridLayout.addWidget(self.save_button, widget_num + 1, 0, 1, SAVE_BUTTON_SIZE)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.centralLayout.addWidget(self.scrollArea, 0, 0, 1, 1)
        model_config_create.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(model_config_create)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        model_config_create.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(model_config_create)
        self.statusbar.setObjectName("statusbar")
        model_config_create.setStatusBar(self.statusbar)
        self.action_open = QtWidgets.QAction(model_config_create)
        self.action_open.setObjectName("action_open")
        self.action_save_as = QtWidgets.QAction(model_config_create)
        self.action_save_as.setObjectName("action_save_as")
        self.action_clear_all = QtWidgets.QAction(model_config_create)
        self.action_clear_all.setObjectName("action_clear_all")
        self.action_close = QtWidgets.QAction(model_config_create)
        self.action_close.setObjectName("action_close")
        self.action_save = QtWidgets.QAction(model_config_create)
        self.action_save.setObjectName("action_save")
        self.action_load = QtWidgets.QAction(model_config_create)
        self.action_load.setObjectName("action_load")
        self.menuFile.addAction(self.action_open)
        self.menuFile.addAction(self.action_load)
        self.menuFile.addAction(self.action_save)
        self.menuFile.addAction(self.action_save_as)
        self.menuFile.addAction(self.action_close)
        self.menuEdit.addAction(self.action_clear_all)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())

        self.retranslate_ui(model_config_create, window_type)
        QtCore.QMetaObject.connectSlotsByName(model_config_create)

    def retranslate_ui(self, model_config_create, window_type=''):
        model_config_create.setWindowTitle(QtWidgets.QApplication.translate("model_config_create", "Create " + window_type + " Config", None, -1))
        self.menuFile.setTitle(QtWidgets.QApplication.translate("model_config_create", "&File", None, -1))
        self.menuEdit.setTitle(QtWidgets.QApplication.translate("model_config_create", "&Edit", None, -1))
        self.action_open.setText(QtWidgets.QApplication.translate("model_config_create", "&Open...", None, -1))
        self.action_open.setToolTip(QtWidgets.QApplication.translate("model_config_create", "Open", None, -1))
        self.action_open.setShortcut(QtWidgets.QApplication.translate("model_config_create", "Ctrl+O", None, -1))
        self.action_save_as.setText(QtWidgets.QApplication.translate("model_config_create", "Save &As...", None, -1))
        self.action_save_as.setShortcut(QtWidgets.QApplication.translate("model_config_create", "Ctrl+Shift+S", None, -1))
        self.action_clear_all.setText(QtWidgets.QApplication.translate("model_config_create", "&Clear All Fields", None, -1))
        self.action_clear_all.setShortcut(QtWidgets.QApplication.translate("model_config_create", "Ctrl+N", None, -1))
        self.action_close.setText(QtWidgets.QApplication.translate("model_config_create", "&Close Window", None, -1))
        self.action_save.setText(QtWidgets.QApplication.translate("model_config_create", "&Save", None, -1))
        self.action_save.setShortcut(QtWidgets.QApplication.translate("model_config_create", "Ctrl+S", None, -1))
        self.action_load.setText(QtWidgets.QApplication.translate("model_config_create", "&Load...", None, -1))
        self.action_load.setShortcut(QtWidgets.QApplication.translate("model_config_create", "Ctrl+L", None, -1))

