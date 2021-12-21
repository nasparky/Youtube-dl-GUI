colourSchema = {
  "darkShade": "#272A31", 
  "darkAccent": "#355889", 
  "mainBrandColour": "#5e8ea7",
  "lightAccent": "#74909a", 
  "lightShade": "#eeede8",
  "dark": "#1a211c",
  "light": "#FFFFFF"}

stylesheet = f"""

QMainWindow > QWidget{{
  background-color: {colourSchema['dark']};
}}

QMainWindow * {{
  font-family: Monospace;
}}

QMenuBar {{
  background-color: {colourSchema['dark']};
  color: {colourSchema['light']};
}}

QTabWidget::pane {{
  background-color: {colourSchema['darkShade']};
}}

QTabWidget>QWidget>QWidget {{
  background-color: {colourSchema['darkShade']};
  color: {colourSchema['light']};
}}

QTabBar::tab {{
  background-color: {colourSchema['darkShade']};
  color: {colourSchema['light']};
  font-family: Monospace;
}}

QLabel {{
  color: {colourSchema['light']};
  font-family: Monospace;
}}

QGroupBox {{
  color: {colourSchema['light']};
}}

QTextEdit {{
  background-color: #000000;
  color: {colourSchema['light']};
}}

QLineEdit {{
  background-color: {colourSchema['darkShade']};
  color: {colourSchema['light']};
}}

QCheckBox {{
  color: {colourSchema['light']};
}}

QTableView {{
  background-color: {colourSchema['darkShade']};
  color: {colourSchema['light']};
}}

QTableView::QTableWidgetItem {{
  background-color: {colourSchema['darkShade']};
  color: {colourSchema['light']};
}}

QHeaderView{{
  background-color: {colourSchema['darkAccent']};
  color: {colourSchema['light']};
}}

QHeaderView::Section{{
  background-color: {colourSchema['darkAccent']};
  color: {colourSchema['light']};
}}

QPushButton {{
  background-color: {colourSchema['mainBrandColour']};
  color: {colourSchema['light']};
}}

QComboBox {{
  background-color: {colourSchema['lightAccent']};
  color: {colourSchema['light']};
}}

QScrollBar {{
  background-color: {colourSchema['darkAccent']};
}}

QProgressBar {{
  background-color: {colourSchema['lightAccent']};
  color: white;
  border: 1px solid white;
  text-align: center;
}}

QProgressBar::chunk {{
  background-color: #006400;
}}
"""