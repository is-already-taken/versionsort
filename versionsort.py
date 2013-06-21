import sys
import string
import re
from operator import itemgetter
from optparse import OptionParser
import types


class VersionSort():

	def extract_versions(self, lines, version_field_matcher=None, build_number_sep=None, field_sep=None, field_num=None):
		max_fields = 0
		array = []

		for line in lines:
			# extract version (N.M.O-B) ... 
			if (type(version_field_matcher) != types.NoneType):
				# ... using matcher
				match = re.search(version_field_matcher, line)
				version = match.group(1)
			elif (type(field_sep) != types.NoneType) and (type(field_num) != types.NoneType):
				# ... using field separator and field index
				fields = re.split(field_sep, line)
				version = fields[field_num - 1]
			else:
				raise Exception("Neither version_field_matcher nor field_sep + field_num specified!")

			# TODO check version by RegExp before continuing


			if (type(build_number_sep) != types.NoneType):
				# get version and build number part (N.M.O, B)
				version_parts = re.split(build_number_sep, version)

				version_nmo = version_parts[0]
				version_build = version_parts[1]

			else:
				# no build number
				version_nmo = version
				version_build = None

			# get version number parts (N, M, O)
			version_nmo_parts = re.split('[^0-9]', version_nmo)

			# remember longest version field count
			length = len(version_nmo_parts)
			if length > max_fields:
				max_fields = length

			# store original line and parts in set and add to array
			if (type(version_build) != types.NoneType):
				tupel = (line, version_nmo_parts, int(version_build))
			else:
				tupel = (line, version_nmo_parts)

			array.append(tupel)

		return array, max_fields

	def sort(self, lines, version_field_matcher='(\d+(:?\.\d+)+(:?-\d+)?)', build_number_sep='-', field_sep=None, field_num=None, reverse=False):
		out_lines = []
		(array, max_fields) = self.extract_versions(lines, version_field_matcher=version_field_matcher, build_number_sep=build_number_sep, field_num=field_num)
		

		for version in array:
			version_parts = version[1]
			build = version[2] if (len(version) == 3) else 0
			version_sum = 0
			length = len(version_parts)

			for i in range(length):
				version_sum = version_sum + (int(version_parts[i]) * (10000 ** (max_fields - i)))

			version_sum = version_sum + build

			tupel = (version[0], version_parts, build, version_sum)
		
			out_lines.append(tupel)


		return map(lambda x: x[0], sorted(out_lines, key=itemgetter(3), reverse=reverse))

class VersionSortCli(VersionSort):

	# defaults	
	matcher = None
	build_separator = None
	field_sep = None
	field_num = None
	reverse = False

	def read_stdin(self):
		lines = []
		for line in sys.stdin:
			line = line.replace("\n", "")
			lines.append(line)

		return lines


	def parse_args(self):
		parser = OptionParser(
			usage = "Usage: %prog [[--field-sep CHAR] [--field-num INDEX] | --matcher REGEX] [--build-sep CHAR, --reverse | -r]",
			description = "Sort version strings contained in lines read from stdin.")

		parser.add_option("--matcher", "-m",
				dest="matcher", metavar="REGEX",
				help="Match version in each line with this matcher. Specify one group around the version string")

		parser.add_option("--field-sep", "-t",
				dest="field_sep", metavar="CHAR",
				help="Field separator char to split string into parts where one may contain the version field")

		parser.add_option("--field-num", "-k",
				dest="field_num", metavar="INDEX",
				help="Field number of field containing the version number")

		parser.add_option("--build-sep", "-u",
				dest="build_separator", metavar="CHAR",
				help="Specify build number separator char")

		parser.add_option("--reverse", "-r",
				dest="reverse", action="store_true", default=False,
				help="Specify build number separator char")

		(options, args) = parser.parse_args()

		if (type(options.matcher) != types.NoneType):
			# Test regular expression
			try:
				re.search(options.matcher, "")
			except Exception as e:
				print "Regular expression of --matcher|-m option is malformed: " + str(e)
				exit(6)

			self.matcher = options.matcher
			

		if (type(options.build_separator) != types.NoneType):
			self.build_separator = options.build_separator

		if (type(options.field_sep) != types.NoneType) and (type(options.matcher) != types.NoneType):
			print "You specified --field-sep|-t and --matcher|-m which are both exclusive. Specify only one of them. Try --help"
			exit(5)

		if (type(options.field_sep) != types.NoneType):
			self.field_sep = options.field_sep

			if (type(options.field_num) == types.NoneType):
				print "You specified --field-sep|-t but not field index (--field-num|-k). Try --help"
				exit(5)

			self.matcher = None

		if (type(options.field_num) != types.NoneType):
			try:
				self.field_num = int(options.field_num)
			except Exception as e:
				print "Argument '"+ options.field_num +"' to --field-num|-k is not a number"
				exit(6)

			if self.field_num <= 0:
				print "The field index argument to --field-num|-k should start at 1" 
				exit(6)

			if (type(options.field_sep) == types.NoneType):
				print "You specified --field-num|-k but not a field separator (--field-sep|-t). Try --help"
				exit(5)

		if (type(options.reverse) != types.NoneType):
			self.reverse = options.reverse


	def run(self):
		self.parse_args()

		unsorted_lines = self.read_stdin()
		sorted_lines = self.sort(unsorted_lines, 
						version_field_matcher = self.matcher, 
						build_number_sep = self.build_separator, field_sep = self.field_sep, 
						field_num = self.field_num,
						reverse = self.reverse)

		for version in sorted_lines:
			print version

if __name__ == "__main__":
	cli = VersionSortCli()
	cli.run()

