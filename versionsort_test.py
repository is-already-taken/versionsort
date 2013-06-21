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

	unsorted_lines_2 = [
		'version strings may be 1.0-12 contained in between too',
		'version strings may be 1.1-2 contained in between too',
		'version strings may be 1.1-24 contained in between too',
		'version strings may be 0.9-563 contained in between too',
		'version strings may be 1.1.1-5 contained in between too',
		'version strings may be 1.3-2 contained in between too',
		'version strings may be 1.3-9 contained in between too'
	]

	expect_sorted_lines_2 = [
		'version strings may be 1.3-9 contained in between too',
		'version strings may be 1.3-2 contained in between too',
		'version strings may be 1.1.1-5 contained in between too',
		'version strings may be 1.1-24 contained in between too',
		'version strings may be 1.1-2 contained in between too',
		'version strings may be 1.0-12 contained in between too',
		'version strings may be 0.9-563 contained in between too'
	]


	def assertions(self, sorted_lines, expected_sorted_lines):
		self.assertEqual(len(sorted_lines), len(expected_sorted_lines), 'Count does not equal, actual value \'{0}\' expected value \'{1}\''.format(len(sorted_lines),  len(expected_sorted_lines)))

		index = 0
		for expected_line in expected_sorted_lines:
			self.assertEqual(sorted_lines[index], expected_line, 'Should be sorted correctly: actual value \'{0}\' expected value \'{1}\''.format(sorted_lines[index], expected_line))
			index += 1

		
	
	def setUp(self):
		self.sorter = VersionSort()

	def testDefaultSortSignature(self):
	 	sorted_lines = self.sorter.sort(lines=self.unsorted_lines, reverse=True)
		self.assertions(sorted_lines, self.expect_sorted_lines)

		expect_sorted_lines_2_reverse = []
		expect_sorted_lines_2_reverse.extend(self.expect_sorted_lines_2)
		expect_sorted_lines_2_reverse.reverse()

	 	sorted_lines = self.sorter.sort(lines=self.unsorted_lines_2, version_field_matcher='(\d+(:?\.\d+)+(:?-\d+)?)', reverse=False)
		self.assertions(sorted_lines, expect_sorted_lines_2_reverse)

		


	def testCustomMatcher(self):
		sorted_lines = self.sorter.sort(self.unsorted_lines, '^.*/([^/]+)$', '-', reverse=True)
		self.assertions(sorted_lines, self.expect_sorted_lines)

