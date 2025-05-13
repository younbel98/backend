from PySide6.QtGui import QEnterEvent
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import QEvent, Qt
import sys
import os

from PySide6.QtWidgets import QWidget
from components.body import *
from components.setting import SettingsData
from components.strings import *
from components.styles import *

lang = SettingsData().lang

class Window(QWidget): 
	def __init__(self, *args, **kwargs): 
		super().__init__() 
		QFontDatabase.addApplicationFont(Fonts.font_family_loction)

		self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

		self.setLayoutDirection(lang.direction)
		self.setObjectName('main-window')
		self.apply_style_sheet()
		
		self.main_layout = QVBoxLayout()
		self.main_layout.setSpacing(0)

		self.title_bar = TitleBar()
		self.main_layout.addWidget(self.title_bar, stretch=0)
		self.title_bar.close_button.clicked.connect(self.close)
		self.title_bar.minimize_button.clicked.connect(self.showMinimized)

		body = Body(self)		
		self.main_layout.addWidget(body, stretch=1)
		
		self.setLayout(self.main_layout)
		self.layout().setContentsMargins(0,0,0,0)		

	def apply_style_sheet(self):
		self.setStyleSheet(f'''
			#main-window {{
				background-color:{Styles.white};
				margin:0px; 
				}}
			QMenu {{
				background-color: {Styles.white};
				border-radius: 0px;
				padding:8px;
				}}
			QLineEdit{{
				background-color: {Styles.primaryLight};
				color: {Styles.black};
				padding: 4px;
				border-radius: {Styles.LineEditBorderRadius};
				border: .5px solid {Styles.darkGrey};
					}}
			QLineEdit:hover, QLineEdit:focus {{
					border: .5px solid {Styles.primary};
							
				}}
			QMenu:item {{
					font-size: 13px;
					color: {Styles.black};
					background-color: {Styles.white};
					border-radius: 0px;
				}}
			QMenu:item:selected{{
					color: {Styles.primary};
					background-color: {Styles.primaryLight};
					border-radius: 0px;
					}}
			QToolTip {{ 
					background-color: {Styles.white}; 
					color: {Styles.darkGrey}; 
					border-radius: 0px;
					font-size: 14px
				}}
			QCheckBox {{
							color: {Styles.darkGrey};
							spacing: 16px;
				}}
				''')


class TitleBar(QFrame):
	def __init__(self):
		super().__init__()
		self.setStyleSheet(f'background-color: {Styles.white};')

		self.main_layout = QHBoxLayout()
		self.main_layout.setSpacing(0)
		self.main_layout.setContentsMargins(0, 0, 0, 0)
		self.main_layout.setAlignment(Qt.AlignmentFlag.AlignLeading)

		self.close_button = TitleBarButton(
			iconName=Icons().close,
			hoverIcon=Icons().close_white,
			color=Styles.white,
			hoverColor=Styles.red
		)
		self.main_layout.addWidget(self.close_button)

		self.minimize_button = TitleBarButton(
			iconName=Icons().minimize,
			hoverIcon=Icons().minimize,
			color=Styles.white,
			hoverColor=Styles.background
		)
		self.main_layout.addWidget(self.minimize_button)

		self.setLayout(self.main_layout)
		

class TitleBarButton(QFrame):
	clicked = Signal()
	def __init__(self, iconName:str, hoverIcon:str, color:str, hoverColor:str):
		super().__init__()
		self.icon_name = iconName
		self.hover_icon = hoverIcon

		self.main_layout = QVBoxLayout()
		self.main_layout.setSpacing(0)
		self.main_layout.setContentsMargins(0, 0, 0, 0)


		self.label = QLabel()
		self.label.setObjectName('close-button')
		self.label.setCursor(Qt.CursorShape.PointingHandCursor)
		self.label.setStyleSheet(f'''#close-button {{
								  background-color: {color};
								  padding: 6px;
								  padding-left: 12px;
								  padding-right: 12px;
									 }}
								  #close-button:hover {{
								  background-color: {hoverColor};
								 }}
												''')
		
		icon = QIcon(iconName)
		pixmap = icon.pixmap(QSize(21, 21))
		self.label.setPixmap(pixmap)
		self.main_layout.addWidget(self.label)

		self.setLayout(self.main_layout)

	def mousePressEvent(self, event):
		self.clicked.emit()
		QFrame.mousePressEvent(self, event)

	def enterEvent(self, event: QEnterEvent):
		super().enterEvent(event)
		icon = QIcon(self.hover_icon)
		pixmap = icon.pixmap(QSize(21, 21))
		self.label.setPixmap(pixmap)


	def leaveEvent(self, event: QEvent):
		super().leaveEvent(event)
		icon = QIcon(self.icon_name)
		pixmap = icon.pixmap(QSize(21, 21))
		self.label.setPixmap(pixmap)
	



os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
app = QApplication(sys.argv)
translator = QTranslator(app)
path = QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
translator.load('qt_%s' % lang.code, path)
app.installTranslator(translator)
main_window = Window()
main_window.showMaximized()
sys.exit(app.exec())