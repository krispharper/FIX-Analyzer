import wpf
import clr

clr.AddReference('System.Data')
from System.Data import *

from System.Windows.Controls import *
from System.Windows.Data import Binding
from System.Windows.Input import Cursors, Mouse
from System.Windows.Media import SolidColorBrush, Colors
from System.Windows import Application, Window, Thickness
from System.Collections.Generic import *

import FixParser

class MainWindow(Window):
	def __init__(self):
		wpf.LoadComponent(self, 'MainWindow.xaml')

	def QuitMenuItem_Click(self, sender, e):
		Application().Quit()

	def TextBox_TextChanged(self, sender, e):
		Mouse.OverrideCursor = Cursors.Wait
		while self.stack.Children.Count > 1:
			self.stack.Children.RemoveAt(1)

		messages = FixParser.get_messages_from_text(self.text_box.Text)
		for msg in messages:
			tag_list = List[FixParser.FixTag]()
			for tag in msg:
				tag_list.Add(tag)

			message_grid = self.new_grid()
			self.add_grid_column(message_grid, "TagName")
			self.add_grid_column(message_grid, "Tag")
			self.add_grid_column(message_grid, "Value")
			self.add_grid_column(message_grid, "ValueName")

			message_grid.ItemsSource = tag_list
			self.stack.AddChild(message_grid)

		Mouse.OverrideCursor = None

	def new_grid(self):
		grid = DataGrid()
		grid.Margin = Thickness(10.0)
		grid.AlternationCount = 2
		grid.AlternatingRowBackground = SolidColorBrush(Colors.LightGray)
		return grid

	def add_grid_column(self, grid, name):
		column = DataGridTextColumn()
		column.Header = name
		column.Binding = Binding(name)
		grid.Columns.Add(column)


if __name__ == '__main__':
	Application().Run(MainWindow())