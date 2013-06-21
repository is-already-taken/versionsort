import unittest
from versionsort import VersionSort

class DefaultWidgetSizeTestCase(unittest.TestCase):
	unsorted_versions = [
		'1.0-12', '1.1-2', '1.1-24', '0.9-563', '1.1.1-5', '1.3-2', '1.3-9'
	]

	expect_sorted_versions = [
		'1.3-9', '1.3-2', '1.1.1-5', '1.1-24', '1.1-2', '1.0-12', '0.9-563'
	]


	def generate_lines(self, string, version_list):
		lines = []
		for version in version_list:
			lines.append(string.format(version))

		return lines
		

	def assertions(self, sorted_lines, expected_sorted_lines):
		self.assertEqual(len(sorted_lines), len(expected_sorted_lines), 'Count does not equal, actual value \'{0}\' expected value \'{1}\''.format(len(sorted_lines),  len(expected_sorted_lines)))

		index = 0
		for expected_line in expected_sorted_lines:
			self.assertEqual(sorted_lines[index], expected_line, 'Should be sorted correctly: actual value \'{0}\' expected value \'{1}\''.format(sorted_lines[index], expected_line))
			index += 1

		
	
	def setUp(self):
		self.sorter = VersionSort()




	def testDefaultSortSignature(self):
		unsorted_lines = self.generate_lines('version strings may be {0} contained in between too', self.unsorted_versions)
		sorted_lines_expect = self.generate_lines('version strings may be {0} contained in between too', self.expect_sorted_versions)

	 	sorted_lines = self.sorter.sort(lines=unsorted_lines, reverse=True)

		self.assertions(sorted_lines, sorted_lines_expect)


	def testSepAndFieldNum(self):
		unsorted_lines = self.generate_lines('version;is;at;{0};field;four;separated;by;semicolon', self.unsorted_versions)
		sorted_lines_expect = self.generate_lines('version;is;at;{0};field;four;separated;by;semicolon', self.expect_sorted_versions)

	 	sorted_lines = self.sorter.sort(lines=unsorted_lines, field_sep=";", field_num=4, reverse=True)

		self.assertions(sorted_lines, sorted_lines_expect)



	def testReverse(self):
		unsorted_lines = self.generate_lines('string_with/any_char/{0}', self.unsorted_versions)
		sorted_lines_expect = self.generate_lines('string_with/any_char/{0}', self.expect_sorted_versions)
		sorted_lines_expect.reverse()

	 	sorted_lines = self.sorter.sort(lines=unsorted_lines, reverse=False)

		self.assertions(sorted_lines, sorted_lines_expect)


	def testCustomMatcher(self):
		unsorted_lines = self.generate_lines('string_with/any_char/{0}', self.unsorted_versions)
		sorted_lines_expect = self.generate_lines('string_with/any_char/{0}', self.expect_sorted_versions)

	 	sorted_lines = self.sorter.sort(lines=unsorted_lines, version_field_matcher='^.*/([^/]+)$', reverse=True)

		self.assertions(sorted_lines, sorted_lines_expect)

