import unittest
from versionsort import VersionSort

class DefaultWidgetSizeTestCase(unittest.TestCase):
	unsorted_lines = [
		'string_with/any_char/1.0-12',
		'string_with/any_char/1.1-2',
		'string_with/any_char/1.1-24',
		'string_with/any_char/0.9-563',
		'string_with/any_char/1.1.1-5',
		'string_with/any_char/1.3-2',
		'string_with/any_char/1.3-9'
	]

	expect_sorted_lines = [
		'string_with/any_char/1.3-9',
		'string_with/any_char/1.3-2',
		'string_with/any_char/1.1.1-5',
		'string_with/any_char/1.1-24',
		'string_with/any_char/1.1-2',
		'string_with/any_char/1.0-12',
		'string_with/any_char/0.9-563'
	]

	def setUp(self):
		self.sorter = VersionSort()

	def runTest(self):
		sorted_lines = self.sorter.sort(self.unsorted_lines, '^.*/([^/]+)$', '-')

		self.assertEqual(len(sorted_lines), len(self.expect_sorted_lines), 'Count does not equal, actual value \'{0}\' expected value \'{1}\''.format(len(sorted_lines),  len(self.expect_sorted_lines)))

		index = 0
		for expected_line in self.expect_sorted_lines:
			self.assertEqual(sorted_lines[index], expected_line, 'Should be sorted correctly: actual value \'{0}\' expected value \'{1}\''.format(sorted_lines[index], expected_line))
			index += 1



